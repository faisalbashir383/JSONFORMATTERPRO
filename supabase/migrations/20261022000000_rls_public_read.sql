-- Phase 0: lock every table down, then open read access to public site content only.
--
-- Django connects as the `postgres` role, which bypasses RLS, so the admin and
-- the import keep working. The browser uses the `anon` key, which only sees
-- what the policies below allow.

-- 1. Enable RLS on every table in the public schema (no policy = no access).
do $$
declare t record;
begin
  for t in select tablename from pg_tables where schemaname = 'public' loop
    execute format('alter table public.%I enable row level security', t.tablename);
  end loop;
end $$;

-- 2. Public, read-only site content.
drop policy if exists "public read" on public.formatter_sitesettings;
create policy "public read" on public.formatter_sitesettings for select to anon, authenticated using (true);

drop policy if exists "public read" on public.formatter_blogcategory;
create policy "public read" on public.formatter_blogcategory for select to anon, authenticated using (true);

drop policy if exists "public read published" on public.formatter_blogpost;
create policy "public read published" on public.formatter_blogpost for select to anon, authenticated using (published);

drop policy if exists "public read active" on public.formatter_programminglanguage;
create policy "public read active" on public.formatter_programminglanguage for select to anon, authenticated using (is_active);

drop policy if exists "public read" on public.formatter_tutorialcategory;
create policy "public read" on public.formatter_tutorialcategory for select to anon, authenticated using (true);

drop policy if exists "public read published" on public.formatter_tutorial;
create policy "public read published" on public.formatter_tutorial for select to anon, authenticated using (is_published);

drop policy if exists "public read" on public.formatter_codeexample;
create policy "public read" on public.formatter_codeexample for select to anon, authenticated
  using (exists (select 1 from public.formatter_tutorial t where t.id = tutorial_id and t.is_published));

drop policy if exists "public read" on public.formatter_mcqquestion;
create policy "public read" on public.formatter_mcqquestion for select to anon, authenticated
  using (exists (select 1 from public.formatter_tutorial t where t.id = tutorial_id and t.is_published));

drop policy if exists "public read" on public.formatter_mcqoption;
create policy "public read" on public.formatter_mcqoption for select to anon, authenticated using (true);

drop policy if exists "public read active" on public.formatter_jobposting;
create policy "public read active" on public.formatter_jobposting for select to anon, authenticated using (is_active);

drop policy if exists "public read" on public.formatter_approveddomain;
create policy "public read" on public.formatter_approveddomain for select to anon, authenticated using (true);

-- 3. Typing leaderboard: readable, but never expose IPs or session keys.
revoke select on public.formatter_typingscore from anon, authenticated;
grant select (id, username, wpm, accuracy, level, duration, created_at, is_verified)
  on public.formatter_typingscore to anon, authenticated;
drop policy if exists "public read verified" on public.formatter_typingscore;
create policy "public read verified" on public.formatter_typingscore for select to anon, authenticated using (is_verified);

-- Write access (contact form, job applications, scores, mock/webhook endpoints)
-- is added in Phase 3/4, through Edge Functions or insert-only policies.
