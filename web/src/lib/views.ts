// Template contexts for the data-driven pages, built the same way as the Django views in
// formatter/views.py (blog_list, blog_detail, blog_category, careers_page, job_detail,
// tutorials_list, tutorial_detail). Model methods the templates call are precomputed here.
import { table, type Row } from './db';
import { staticPosts } from './static-posts';

const POSTS_PER_PAGE = 10;

// ---------------------------------------------------------------- blog

/** Supabase posts plus the Markdown posts in src/content/blog, newest first. */
async function blogData() {
  const categories = [...await table('formatter_blogcategory', 'name.asc')];
  const posts = (await table('formatter_blogpost', 'published_at.desc')).filter((p) => p.published);

  for (const post of staticPosts()) {
    let category = categories.find((c) => c.slug === post.category_slug);
    if (!category) {
      category = { id: `static:${post.category_slug}`, name: post.category_name, slug: post.category_slug, description: '' };
      categories.push(category);
    }
    posts.push({ ...post, category_id: category.id });
  }
  categories.sort((a, b) => a.name.localeCompare(b.name));
  posts.sort((a, b) => (a.published_at < b.published_at ? 1 : a.published_at > b.published_at ? -1 : 0));

  const byId = new Map(categories.map((c) => [c.id, { ...c, posts: [] as Row[] }]));
  const enriched = posts.map((p) => ({
    ...p,
    category: byId.get(p.category_id),
    get_absolute_url: `/blog/${p.slug}/`,
    get_tags_list: String(p.tags ?? '').split(',').map((t) => t.trim()).filter(Boolean),
  }));
  for (const p of enriched) p.category?.posts.push(p);
  return { categories: [...byId.values()], posts: enriched };
}

function paginate<T>(items: T[], number: number, baseUrl: string) {
  const numPages = Math.max(1, Math.ceil(items.length / POSTS_PER_PAGE));
  const url = (n: number) => (n === 1 ? baseUrl : `${baseUrl}page/${n}/`);
  return {
    object_list: items.slice((number - 1) * POSTS_PER_PAGE, number * POSTS_PER_PAGE),
    number,
    paginator: { num_pages: numPages },
    has_previous: number > 1,
    has_next: number < numPages,
    has_other_pages: numPages > 1,
    previous_page_number: number - 1,
    next_page_number: number + 1,
    previous_page_url: url(number - 1),
    next_page_url: url(number + 1),
  };
}

export async function blogListPages() {
  const { categories, posts } = await blogData();
  const pages: { url: string; context: Row }[] = [];
  const addListing = (list: Row[], baseUrl: string, extra: Row) => {
    const numPages = Math.max(1, Math.ceil(list.length / POSTS_PER_PAGE));
    for (let n = 1; n <= numPages; n++) {
      pages.push({
        url: n === 1 ? baseUrl : `${baseUrl}page/${n}/`,
        context: { page_obj: paginate(list, n, baseUrl), categories, total_posts: posts.length, ...extra },
      });
    }
  };
  addListing(posts, '/blog/', {});
  for (const category of categories) {
    addListing(category.posts, `/blog/category/${category.slug}/`, { category, current_category: category.slug });
  }
  return pages;
}

export async function blogDetailPages() {
  const { posts } = await blogData();
  return posts.map((post, i) => ({
    url: `/blog/${post.slug}/`,
    context: {
      post,
      related_posts: posts.filter((p) => p.category_id === post.category_id && p.id !== post.id).slice(0, 3),
      // posts are newest first: the previous (older) post comes after, the next (newer) one before.
      previous_post: posts.slice(i + 1).find((p) => p.published_at < post.published_at),
      next_post: [...posts.slice(0, i)].reverse().find((p) => p.published_at > post.published_at),
    },
  }));
}

// ---------------------------------------------------------------- careers

const EMPLOYMENT_TYPES: [string, string][] = [
  ['full-time', 'Full-time'], ['part-time', 'Part-time'], ['contract', 'Contract'],
  ['internship', 'Internship'], ['remote', 'Remote'], ['hybrid', 'Hybrid'],
];
const DEPARTMENTS: [string, string][] = [
  ['engineering', 'Engineering'], ['product', 'Product'], ['design', 'Design'], ['marketing', 'Marketing'],
  ['sales', 'Sales'], ['operations', 'Operations'], ['hr', 'Human Resources'], ['finance', 'Finance'],
  ['other', 'Other'],
];
const label = (choices: [string, string][], code: string) => choices.find(([c]) => c === code)?.[1] ?? code;
const thousands = (n: number) => n.toLocaleString('en-US');

async function jobs() {
  const rows = (await table('formatter_jobposting', 'is_featured.desc,created_at.desc')).filter((j) => j.is_active);
  return rows.map((j) => ({
    ...j,
    get_absolute_url: `/careers/${j.slug}/`,
    get_department_display: label(DEPARTMENTS, j.department),
    get_employment_type_display: label(EMPLOYMENT_TYPES, j.employment_type),
    get_salary_range: j.show_salary && j.salary_min
      ? j.salary_max
        ? `${j.salary_currency} ${thousands(j.salary_min)} - ${thousands(j.salary_max)}`
        : `${j.salary_currency} ${thousands(j.salary_min)}+`
      : null,
  }));
}

export async function careersContext() {
  const list = await jobs();
  return { jobs: list, departments: DEPARTMENTS, employment_types: EMPLOYMENT_TYPES, total_jobs: list.length };
}

export async function jobDetailPages() {
  const list = await jobs();
  return list.map((job) => ({
    url: job.get_absolute_url,
    context: {
      job,
      related_jobs: list.filter((j) => j.department === job.department && j.id !== job.id).slice(0, 3),
    },
  }));
}

// ---------------------------------------------------------------- tutorials

async function tutorialData() {
  const languages = (await table('formatter_programminglanguage', 'order.asc,name.asc')).filter((l) => l.is_active);
  const allLanguages = await table('formatter_programminglanguage', 'order.asc,name.asc');
  const categories = await table('formatter_tutorialcategory', 'order.asc,name.asc');
  const tutorials = await table('formatter_tutorial', 'order.asc,title.asc');
  const examples = await table('formatter_codeexample', 'order.asc');
  const questions = await table('formatter_mcqquestion', 'order.asc');
  const options = await table('formatter_mcqoption', 'order.asc');

  const langById = new Map(allLanguages.map((l) => [l.id, l]));
  const catById = new Map(categories.map((c) => [c.id, { ...c, tutorials: [] as Row[] }]));
  const questionsFor = (tutorialId: number) => questions
    .filter((q) => q.tutorial_id === tutorialId)
    .map((q) => {
      const opts = options.filter((o) => o.question_id === q.id);
      return { ...q, options: opts, get_correct_option: opts.find((o) => o.is_correct) };
    });

  const enriched = tutorials.map((t) => ({
    ...t,
    category: catById.get(t.category_id),
    get_absolute_url: `/tutorials/${t.slug}/`,
    mcq_questions: questionsFor(t.id),
    code_examples: examples.filter((e) => e.tutorial_id === t.id).map((e) => ({ ...e, language: langById.get(e.language_id) })),
  }));
  // Tutorial.Meta.ordering is ['category__order', 'order', 'title'].
  enriched.sort((a, b) => (a.category?.order ?? 0) - (b.category?.order ?? 0));
  for (const t of enriched) t.category?.tutorials.push(t);

  return { languages, categories: [...catById.values()], tutorials: enriched };
}

export async function tutorialsListContext() {
  const { languages, categories } = await tutorialData();
  return {
    languages,
    selected_language: languages[0],
    categories: categories.filter((c) => c.tutorials.some((t: Row) => t.is_published)),
  };
}

export async function tutorialDetailPages() {
  const { languages, tutorials } = await tutorialData();
  const published = tutorials.filter((t) => t.is_published);
  return published.map((tutorial) => {
    const siblings = published
      .filter((t) => t.category_id === tutorial.category_id)
      .sort((a, b) => a.order - b.order);
    return {
      url: tutorial.get_absolute_url,
      context: {
        tutorial,
        languages,
        selected_language: languages[0],
        code_examples: tutorial.code_examples,
        mcq_questions: tutorial.mcq_questions,
        category_tutorials: siblings,
        next_tutorial: published.find((t) => t.category_id === tutorial.category_id && t.order > tutorial.order),
        prev_tutorial: [...siblings].reverse().find((t) => t.order < tutorial.order),
      },
    };
  });
}
