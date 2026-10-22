#!/usr/bin/env bash
# Copy all Django data into a Supabase Postgres database.
#
# Usage:
#   SUPABASE_DATABASE_URL='postgresql://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres' \
#   SOURCE=production scripts/migrate_to_supabase.sh
#
#   SOURCE=production  read from the current Postgres in .env (DB_HOST, DB_NAME, ...)  [default]
#   SOURCE=local       read from db.sqlite3
#   WITH_LOGS=1        also copy analytics/log tables (page views, visitor logs, lookups, ...)
#
# Use the Supabase *session* pooler (port 5432) or the direct connection, not the
# transaction pooler (6543): migrations need session features.
set -euo pipefail

cd "$(dirname "$0")/.."
: "${SUPABASE_DATABASE_URL:?Set SUPABASE_DATABASE_URL to your Supabase connection string}"
SOURCE="${SOURCE:-production}"
PY="${PYTHON:-venv/bin/python}"
OUT_DIR="${OUT_DIR:-supabase/export}"
mkdir -p "$OUT_DIR"
FIXTURE="$OUT_DIR/data.json"

EXCLUDE=(
  -e contenttypes -e auth.permission -e sessions -e admin.logentry
)
if [[ "${WITH_LOGS:-0}" != "1" ]]; then
  EXCLUDE+=(
    -e formatter.visitorlog -e formatter.pageview -e formatter.networklookuplog
    -e formatter.toolusagelog -e formatter.dummyjsonapilog -e formatter.domainpagevisit
    -e apiutils.capturedrequest
  )
fi

if [[ "$SOURCE" == "local" ]]; then
  SRC_ENV=development
else
  SRC_ENV=production
fi

echo "==> Exporting data from $SOURCE database"
env -u DATABASE_URL env="$SRC_ENV" "$PY" manage.py dumpdata \
  --natural-foreign --indent 2 "${EXCLUDE[@]}" -o "$FIXTURE"

echo "==> Creating schema in Supabase"
env DATABASE_URL="$SUPABASE_DATABASE_URL" env=production "$PY" manage.py migrate --noinput

echo "==> Loading data into Supabase"
env DATABASE_URL="$SUPABASE_DATABASE_URL" env=production "$PY" manage.py loaddata "$FIXTURE"

echo "==> Resetting ID sequences and applying RLS policies"
env DATABASE_URL="$SUPABASE_DATABASE_URL" env=production "$PY" manage.py shell -c "
from io import StringIO
from pathlib import Path
from django.core.management import call_command
from django.db import connection
buf = StringIO()
call_command('sqlsequencereset', 'formatter', 'apiutils', 'auth', stdout=buf, no_color=True)
with connection.cursor() as cur:
    cur.execute(buf.getvalue())
    for f in sorted(Path('supabase/migrations').glob('*.sql')):
        if f.name.endswith('_django_schema.sql'):
            continue  # manage.py migrate above already created the tables
        print('applying', f)
        cur.execute(f.read_text())
"

echo "==> Done. Row counts in Supabase:"
env DATABASE_URL="$SUPABASE_DATABASE_URL" env=production "$PY" manage.py shell -c "
from django.apps import apps
for m in apps.get_app_config('formatter').get_models():
    print(f'{m._meta.db_table:40} {m.objects.count()}')
"
