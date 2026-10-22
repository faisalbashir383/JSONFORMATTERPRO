// GET /api/dummy-json/<resource>/?count=N&fields=a,b
//
// Port of the dummy_json_*_api views in formatter/views.py: same resources, fields and
// response shape ({ success, count, data }). Public API, so any origin may call it.
// `fields` (documented on /dummy-json-api/) keeps only the listed keys of each item.

type Item = Record<string, unknown>;

const CORS = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, OPTIONS' };

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', ...CORS } });

const pick = <T>(list: T[]): T => list[Math.floor(Math.random() * list.length)];
const randInt = (min: number, max: number) => min + Math.floor(Math.random() * (max - min + 1));
const uniform = (min: number, max: number, decimals: number) =>
  Number((min + Math.random() * (max - min)).toFixed(decimals));
const isoDate = (offsetDays: number) => new Date(Date.now() + offsetDays * 86_400_000).toISOString().slice(0, 10);

const FIRST = ['Emma', 'James', 'Sarah', 'Michael', 'Emily', 'David', 'Olivia', 'Daniel', 'Sophia', 'William',
  'Ava', 'Alexander', 'Isabella', 'Matthew', 'Mia', 'Ethan', 'Charlotte', 'Andrew', 'Amelia', 'Joseph'];
const LAST = ['Wilson', 'Rodriguez', 'Kim', 'Johnson', 'Chen', 'Smith', 'Brown', 'Davis', 'Garcia', 'Miller',
  'Martinez', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Moore'];
const USER_COMPANIES = ['TechStart Inc', 'DataFlow Systems', 'CloudNine Labs', 'ByteWave', 'NexGen Solutions',
  'Quantum Dynamics', 'SkyPeak Tech', 'BlueShift AI', 'InnovateCo', 'FuturePath'];

const GENERATORS: Record<string, { defaultCount: number; make: (id: number) => Item }> = {
  users: {
    defaultCount: 5,
    make: (id) => {
      const first = pick(FIRST), last = pick(LAST);
      return {
        id, name: `${first} ${last}`, email: `${first.toLowerCase()}.${last.toLowerCase()}@example.com`,
        phone: `+1-555-${randInt(1000, 9999)}`, company: pick(USER_COMPANIES),
        status: pick(['active', 'active', 'active', 'inactive', 'pending']),
        avatar: `https://i.pravatar.cc/150?u=${id}`,
      };
    },
  },
  products: {
    defaultCount: 10,
    make: (id) => {
      const [name, category] = pick([
        ['Wireless Headphones', 'Electronics'], ['Smart Watch', 'Electronics'], ['Bluetooth Speaker', 'Electronics'],
        ['Ergonomic Chair', 'Furniture'], ['Standing Desk', 'Furniture'], ['LED Desk Lamp', 'Furniture'],
        ['Running Shoes', 'Sports'], ['Yoga Mat', 'Sports'], ['Dumbbell Set', 'Sports'],
        ['Coffee Maker', 'Kitchen'], ['Air Fryer', 'Kitchen'], ['Blender Pro', 'Kitchen'],
        ['Laptop Backpack', 'Accessories'], ['Leather Wallet', 'Accessories'], ['Sunglasses', 'Accessories'],
      ]);
      return {
        id, name: `${name} ${pick(['Pro', 'Plus', 'Max', 'Lite', 'X', ''])}`.trim(),
        price: uniform(19.99, 499.99, 2), category, inStock: pick([true, true, true, false]),
        rating: uniform(3.5, 5.0, 1), image: `https://picsum.photos/seed/product${id}/300/300`,
      };
    },
  },
  posts: {
    defaultCount: 5,
    make: (id) => ({
      id,
      title: pick(['Getting Started with React', 'Python Best Practices', 'Introduction to Machine Learning',
        'Docker for Beginners', 'REST API Design Patterns', 'Building Microservices', 'JavaScript ES6 Features',
        'Cloud Architecture Basics', 'Database Optimization Tips', 'Security Best Practices',
        'CI/CD Pipeline Setup', 'Testing Strategies']),
      body: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
      author: pick(['John Developer', 'Jane Coder', 'Alex Engineer', 'Sam Architect', 'Chris DevOps']),
      authorAvatar: `https://i.pravatar.cc/100?u=author${randInt(1, 50)}`,
      date: isoDate(-randInt(1, 365)),
      views: randInt(100, 10000),
      thumbnail: `https://picsum.photos/seed/post${id}/400/200`,
    }),
  },
  comments: {
    defaultCount: 5,
    make: (id) => {
      const name = pick(['Alice Johnson', 'Bob Smith', 'Carol Williams', 'David Brown', 'Eva Martinez',
        'Frank Lee', 'Grace Kim', 'Henry Davis']);
      return {
        id, name, email: `${name.split(' ')[0].toLowerCase()}@example.com`,
        avatar: `https://i.pravatar.cc/80?u=commenter${randInt(1, 100)}`,
        body: pick([
          'Great article! Very informative and well written.',
          'Thanks for sharing this, it really helped me understand the topic.',
          'I have a question about the third point you mentioned.',
          'This is exactly what I was looking for. Bookmarked!',
          'Could you elaborate more on the implementation details?',
        ]),
        postId: randInt(1, 100),
      };
    },
  },
  todos: {
    defaultCount: 5,
    make: (id) => ({
      id,
      title: pick(['Complete project documentation', 'Review pull request', 'Fix login bug', 'Update dependencies',
        'Write unit tests', 'Refactor authentication module', 'Design new dashboard', 'Implement search feature',
        'Optimize database queries', 'Deploy to staging', 'Code review', 'Team meeting', 'Update README']),
      completed: pick([true, false, false]),
      priority: pick(['low', 'medium', 'medium', 'high', 'critical']),
      dueDate: isoDate(randInt(1, 30)),
    }),
  },
  companies: {
    defaultCount: 5,
    make: (id) => {
      const name = pick(['TechCorp', 'DataVerse', 'CloudNine', 'ByteWorks', 'NexGen', 'SkyPeak', 'BlueShift',
        'InnovateCo', 'FuturePath', 'QuantumLeap']);
      return {
        id, name: `${name} ${pick(['Inc', 'LLC', 'Corp', 'Group', 'Solutions', 'Labs', 'Systems'])}`,
        industry: pick(['Technology', 'Finance', 'Healthcare', 'E-commerce', 'Manufacturing', 'Consulting', 'Education']),
        employees: randInt(10, 10000), revenue: `$${randInt(1, 500)}M`, founded: randInt(1990, 2023),
        logo: `https://ui-avatars.com/api/?name=${name}&size=128&background=random`,
      };
    },
  },
};

export const onRequestOptions: PagesFunction = async () => new Response(null, { status: 204, headers: CORS });

export const onRequestGet: PagesFunction = async ({ request, params }) => {
  const resource = ([] as string[]).concat(params.path ?? []).filter(Boolean)[0];
  const generator = resource && GENERATORS[resource];
  if (!generator) {
    return json({ success: false, error: `Unknown resource. Use one of: ${Object.keys(GENERATORS).join(', ')}` }, 404);
  }

  const url = new URL(request.url);
  const requested = parseInt(url.searchParams.get('count') ?? '', 10);
  const count = Math.min(Number.isNaN(requested) ? generator.defaultCount : Math.max(requested, 0), 100);
  const fields = (url.searchParams.get('fields') ?? '').split(',').map((f) => f.trim()).filter(Boolean);

  let data = Array.from({ length: count }, (_, i) => generator.make(i + 1));
  if (fields.length) {
    data = data.map((item) => Object.fromEntries(fields.filter((f) => f in item).map((f) => [f, item[f]])));
  }
  return json({ success: true, count, data });
};
