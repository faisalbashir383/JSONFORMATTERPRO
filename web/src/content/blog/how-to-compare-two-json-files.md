---
title: "How to Compare Two JSON Files and Find What Actually Changed"
category: "JSON Guides"
excerpt: "A plain text diff on JSON is mostly noise. Key order and whitespace change, the data doesn't. Here are four ways to compare JSON by what it means, from a browser tool to jq and Python."
meta_description: "Compare two JSON files without the noise. Learn why text diffs fail on JSON and how to compare by meaning using an online JSON diff, jq, Python or JavaScript."
meta_keywords: "compare json files, json diff, compare two json objects, jq diff, json compare online"
tags: "JSON, Debugging, jq, Python, JavaScript"
published_at: "2026-10-21T08:45:00+00:00"
author_name: "Faisal Ahmad"
---
You have two versions of a JSON file. Maybe it's an API response from before and after a deploy, or a config that works on staging and breaks in production. You want to know what's different. So you run `diff`, or open both files side by side, and get forty changed lines for what turns out to be one value.

The problem is that JSON is data, but `diff` compares text. Two files can hold exactly the same data and still look completely different line by line.

## Why a text diff gets it wrong

Take these two snippets:

```json
{"id": 42, "name": "Asha", "roles": ["admin", "editor"]}
```

```json
{
  "name": "Asha",
  "id": 42,
  "roles": [
    "admin",
    "editor"
  ]
}
```

To a JSON parser, these are the same object. RFC 8259, the JSON standard, defines an object as an unordered collection of name/value pairs, so key order doesn't matter. Neither does whitespace. To `diff`, every single line is different.

This comes up all the time in practice. Many serializers don't guarantee key order. One service pretty-prints its output and another minifies it. Someone runs a formatter on the file before committing. The data hasn't changed, but the text has.

So the trick is to compare the parsed data, not the characters. There are a few ways to do that.

## Option 1: use a JSON diff tool

The quickest way is a tool that understands JSON. Paste both versions into our [JSON Diff](/json-diff/) tool and it parses each side, then compares them value by value. Key order and formatting are ignored, so you only see real changes, marked as added, removed or changed. Each one comes with its path, like `user.address.city` or `items[2]`, so you know exactly where to look in a big file.

Everything runs in your browser, which matters if the files contain customer data or tokens you'd rather not upload anywhere.

## Option 2: normalise with jq, then diff

If you're in a terminal, [jq](https://jqlang.github.io/jq/) can rewrite both files into a single standard layout first. The `-S` flag sorts keys, and the `.` filter pretty-prints everything with the same indentation:

```bash
diff <(jq -S . before.json) <(jq -S . after.json)
```

Now a key that moved shows up as nothing, and a value that changed shows up as one line. This works well in scripts and CI jobs. It also works with `git diff --no-index` if you prefer git's output and colours:

```bash
jq -S . before.json > /tmp/before.json
jq -S . after.json > /tmp/after.json
git diff --no-index /tmp/before.json /tmp/after.json
```

One thing jq won't do is sort arrays for you, and that's deliberate. More on that below.

## Option 3: compare in Python

For a simple "are these the same?" check, Python's dictionaries already ignore key order:

```python
import json

with open("before.json") as f:
    before = json.load(f)
with open("after.json") as f:
    after = json.load(f)

print(before == after)
```

That gives you a yes or a no, which is often all a test needs. To find *where* the difference is, write a small recursive function that walks both structures and records the path whenever something doesn't match:

```python
def find_changes(a, b, path="$"):
    if type(a) != type(b):
        return [f"{path}: type changed from {type(a).__name__} to {type(b).__name__}"]
    if isinstance(a, dict):
        changes = []
        for key in a.keys() | b.keys():
            if key not in b:
                changes.append(f"{path}.{key}: removed")
            elif key not in a:
                changes.append(f"{path}.{key}: added")
            else:
                changes += find_changes(a[key], b[key], f"{path}.{key}")
        return changes
    if isinstance(a, list):
        if len(a) != len(b):
            return [f"{path}: length {len(a)} -> {len(b)}"]
        changes = []
        for i, (x, y) in enumerate(zip(a, b)):
            changes += find_changes(x, y, f"{path}[{i}]")
        return changes
    return [] if a == b else [f"{path}: {a!r} -> {b!r}"]

for line in find_changes(before, after):
    print(line)
```

If you'd rather not maintain your own, the `deepdiff` package on PyPI does the same job with many more options.

## Option 4: compare in JavaScript

In JavaScript there's no built-in deep equality, and `JSON.stringify(a) === JSON.stringify(b)` is a trap. It does compare the data, but it also compares key order, so two equal objects with keys in a different order come out as different.

For tests, use what your test runner already gives you. Jest and Vitest have `expect(actual).toEqual(expected)`, and Node has `assert.deepStrictEqual()`. All of them ignore key order and print a readable diff when the check fails. One catch with `toEqual`: it treats a key set to `undefined` as if it were missing. Use `toStrictEqual` if that difference matters to you. For application code, Lodash's `_.isEqual()` is the usual choice.

## The part every method gets "wrong": arrays

Every approach above treats arrays as ordered. That's correct, since JSON arrays *are* ordered, and `[1, 2, 3]` really is different from `[3, 2, 1]`. But it causes noise when order doesn't mean anything to you. Say an API returns a list of users in a different order each time. Comparing by position reports every element as changed.

If order doesn't matter for your data, sort the arrays the same way on both sides before you compare. With jq you can sort a list of objects by a field:

```bash
jq -S '.users |= sort_by(.id)' before.json
```

In Python, sort both lists with `key=lambda u: u["id"]` before comparing. Pick a field that's unique, usually an ID, so the sort gives the same result every time.

## Small things that cause false alarms

A few cases trip people up even with a proper JSON comparison:

- **Numbers.** `1` and `1.0` are equal in Python and JavaScript. But a number that's been rounded, like `0.30000000000000004` becoming `0.3`, will show up as a change.
- **null versus missing.** `{"note": null}` and `{}` are different. One has a key set to null, the other doesn't have the key at all. Some APIs switch between the two without warning.
- **Timestamps and IDs.** Fields like `updated_at` or `request_id` change on every response. Delete them from both sides before comparing, or your diff will never be empty.

For the last point, jq makes it easy: `jq -S 'del(.updated_at, .request_id)' file.json`.

If you need to send the changes somewhere rather than just read them, look at JSON Patch, defined in RFC 6902. It describes a diff as a list of `add`, `remove` and `replace` operations with paths, and there are libraries for it in most languages, such as `fast-json-patch` for JavaScript and `jsonpatch` for Python.

## Which one should you use?

For a one-off check, paste both files into the [JSON Diff](/json-diff/) tool and read the list of changes. In a script or CI job, `jq -S` plus `diff` is hard to beat. In tests, use your framework's deep equality check rather than comparing strings.

And if the files are large and you only care about one part, pull that part out first with a JSONPath expression such as `$.orders[*].total` in the [JSONPath Tester](/json-path-tester/), then compare just those values. It's a lot easier to review ten values than ten thousand lines.
