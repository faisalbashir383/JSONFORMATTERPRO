-- Make content easy to add from the Supabase Table Editor.
--
-- Django filled these in from Python (model field defaults, auto_now/auto_now_add and the
-- models' save() methods), so the tables created from the Django schema have no database
-- defaults. This adds the same behaviour in the database:
--   * column defaults matching the Django models (timestamps, counters, booleans, text)
--   * slug generated from the title/name when left empty (Django's slugify)
--   * blog posts: published_at set on first publish, reading_time from the word count,
--     meta_description falls back to the excerpt
--   * tutorials and jobs: meta_title / meta_description filled in like Django's save()
--   * updated_at refreshed on every update

create extension if not exists unaccent with schema extensions;

-- Django's slugify(): ASCII-fold, drop anything but letters/digits/spaces/hyphens, lowercase,
-- collapse whitespace and hyphens into one hyphen, trim leading/trailing hyphens and underscores.
create or replace function public.slugify(value text) returns text
language sql immutable set search_path = '' as $$
  select trim(both '-_' from regexp_replace(
    regexp_replace(lower(extensions.unaccent(coalesce(value, ''))), '[^\w\s-]', '', 'g'),
    '[-\s]+', '-', 'g'))
$$;

create or replace function public.set_updated_at() returns trigger
language plpgsql set search_path = '' as $$
begin
  new.updated_at := now();
  return new;
end $$;

-- ---------------------------------------------------------------- blog

alter table public.formatter_blogcategory
  alter column slug set default '',
  alter column description set default '',
  alter column created_at set default now();

alter table public.formatter_blogpost
  alter column slug set default '',
  alter column tags set default '',
  alter column meta_description set default '',
  alter column meta_keywords set default '',
  alter column published set default false,
  alter column created_at set default now(),
  alter column updated_at set default now(),
  alter column views set default 0,
  alter column reading_time set default 5,
  alter column author_name set default 'JSON Formatters Pro',
  alter column author_profile_url set default '';

create or replace function public.blogpost_before_save() returns trigger
language plpgsql set search_path = '' as $$
declare word_count integer;
begin
  if coalesce(new.slug, '') = '' then new.slug := public.slugify(new.title); end if;
  if new.published and new.published_at is null then new.published_at := now(); end if;
  if coalesce(new.meta_description, '') = '' then new.meta_description := new.excerpt; end if;
  word_count := coalesce(array_length(regexp_split_to_array(trim(coalesce(new.content, '')), '\s+'), 1), 0);
  if trim(coalesce(new.content, '')) = '' then word_count := 0; end if;
  new.reading_time := greatest(1, word_count / 200);
  return new;
end $$;

-- ---------------------------------------------------------------- tutorials

alter table public.formatter_programminglanguage
  alter column slug set default '',
  alter column icon set default '💻',
  alter column syntax_highlight set default 'python',
  alter column is_active set default true,
  alter column "order" set default 0;

alter table public.formatter_tutorialcategory
  alter column slug set default '',
  alter column description set default '',
  alter column icon set default '📂',
  alter column "order" set default 0;

alter table public.formatter_tutorial
  alter column slug set default '',
  alter column meta_title set default '',
  alter column meta_description set default '',
  alter column meta_keywords set default '',
  alter column "order" set default 0,
  alter column is_published set default false,
  alter column views set default 0,
  alter column created_at set default now(),
  alter column updated_at set default now();

alter table public.formatter_codeexample
  alter column output set default '',
  alter column explanation set default '',
  alter column "order" set default 0;

alter table public.formatter_mcqquestion
  alter column explanation set default '',
  alter column "order" set default 0;

alter table public.formatter_mcqoption
  alter column is_correct set default false,
  alter column "order" set default 0;

-- Categories and languages: slug from name.
create or replace function public.slug_from_name() returns trigger
language plpgsql set search_path = '' as $$
begin
  if coalesce(new.slug, '') = '' then new.slug := public.slugify(new.name); end if;
  return new;
end $$;

create or replace function public.tutorial_before_save() returns trigger
language plpgsql set search_path = '' as $$
begin
  if coalesce(new.slug, '') = '' then new.slug := public.slugify(new.title); end if;
  if coalesce(new.meta_title, '') = '' then new.meta_title := new.title; end if;
  return new;
end $$;

-- ---------------------------------------------------------------- careers

alter table public.formatter_jobposting
  alter column slug set default '',
  alter column department set default 'engineering',
  alter column location set default 'Delhi, India',
  alter column employment_type set default 'full-time',
  alter column benefits set default '',
  alter column salary_currency set default 'INR',
  alter column show_salary set default false,
  alter column meta_title set default '',
  alter column meta_description set default '',
  alter column meta_keywords set default '',
  alter column is_active set default true,
  alter column is_featured set default false,
  alter column created_at set default now(),
  alter column updated_at set default now(),
  alter column apply_email set default '',
  alter column apply_url set default '';

create or replace function public.jobposting_before_save() returns trigger
language plpgsql set search_path = '' as $$
begin
  if coalesce(new.slug, '') = '' then new.slug := public.slugify(new.title); end if;
  if coalesce(new.meta_title, '') = '' then
    new.meta_title := new.title || ' - Careers at JSON Formatters Pro';
  end if;
  if coalesce(new.meta_description, '') = '' then
    new.meta_description := 'Apply for ' || new.title || ' position at JSON Formatters Pro. ' ||
      case new.employment_type
        when 'full-time' then 'Full-time' when 'part-time' then 'Part-time'
        when 'contract' then 'Contract' when 'internship' then 'Internship'
        when 'remote' then 'Remote' when 'hybrid' then 'Hybrid' else new.employment_type
      end || ' role in ' || new.location || '.';
  end if;
  return new;
end $$;

-- ---------------------------------------------------------------- triggers

drop trigger if exists before_save on public.formatter_blogcategory;
create trigger before_save before insert or update on public.formatter_blogcategory
  for each row execute function public.slug_from_name();

drop trigger if exists before_save on public.formatter_programminglanguage;
create trigger before_save before insert or update on public.formatter_programminglanguage
  for each row execute function public.slug_from_name();

drop trigger if exists before_save on public.formatter_tutorialcategory;
create trigger before_save before insert or update on public.formatter_tutorialcategory
  for each row execute function public.slug_from_name();

drop trigger if exists before_save on public.formatter_blogpost;
create trigger before_save before insert or update on public.formatter_blogpost
  for each row execute function public.blogpost_before_save();

drop trigger if exists before_save on public.formatter_tutorial;
create trigger before_save before insert or update on public.formatter_tutorial
  for each row execute function public.tutorial_before_save();

drop trigger if exists before_save on public.formatter_jobposting;
create trigger before_save before insert or update on public.formatter_jobposting
  for each row execute function public.jobposting_before_save();

drop trigger if exists set_updated_at on public.formatter_blogpost;
create trigger set_updated_at before update on public.formatter_blogpost
  for each row execute function public.set_updated_at();

drop trigger if exists set_updated_at on public.formatter_tutorial;
create trigger set_updated_at before update on public.formatter_tutorial
  for each row execute function public.set_updated_at();

drop trigger if exists set_updated_at on public.formatter_jobposting;
create trigger set_updated_at before update on public.formatter_jobposting
  for each row execute function public.set_updated_at();

-- The helper functions don't need to be callable through the public API.
revoke execute on function public.slugify(text) from public, anon, authenticated;
revoke execute on function public.set_updated_at() from public, anon, authenticated;
revoke execute on function public.slug_from_name() from public, anon, authenticated;
revoke execute on function public.blogpost_before_save() from public, anon, authenticated;
revoke execute on function public.tutorial_before_save() from public, anon, authenticated;
revoke execute on function public.jobposting_before_save() from public, anon, authenticated;
