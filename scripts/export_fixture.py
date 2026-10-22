"""
Export the tables the static site reads into a JSON file shaped like Supabase REST responses,
for building web/ without a Supabase connection (DATA_FIXTURE=...).

    env=development python manage.py shell < scripts/export_fixture.py
    DATA_FIXTURE=../supabase/export/fixture.json npm run build      # from web/

Rows are limited to what the anon key can see under the RLS policies in supabase/migrations.
"""
import json
import os
from pathlib import Path

from formatter.models import (
    BlogCategory, BlogPost, CodeExample, JobPosting, MCQOption, MCQQuestion,
    ProgrammingLanguage, Tutorial, TutorialCategory,
)

TABLES = {
    BlogCategory: BlogCategory.objects.all(),
    BlogPost: BlogPost.objects.filter(published=True),
    ProgrammingLanguage: ProgrammingLanguage.objects.filter(is_active=True),
    TutorialCategory: TutorialCategory.objects.all(),
    Tutorial: Tutorial.objects.filter(is_published=True),
    CodeExample: CodeExample.objects.filter(tutorial__is_published=True),
    MCQQuestion: MCQQuestion.objects.filter(tutorial__is_published=True),
    MCQOption: MCQOption.objects.all(),
    JobPosting: JobPosting.objects.filter(is_active=True),
}


def value(v):
    if hasattr(v, 'isoformat'):
        return v.isoformat()  # same format as PostgREST: 2025-12-05T10:00:00.123456+00:00
    return v


data = {}
for model, qs in TABLES.items():
    columns = [f.attname for f in model._meta.concrete_fields]
    data[model._meta.db_table] = [{c: value(getattr(obj, c)) for c in columns} for obj in qs.order_by('pk')]

out = Path(os.environ.get('FIXTURE_OUT', 'supabase/export/fixture.json'))
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(data, ensure_ascii=False, indent=1))
print(f'wrote {out}: ' + ', '.join(f'{t} {len(r)}' for t, r in data.items()))
