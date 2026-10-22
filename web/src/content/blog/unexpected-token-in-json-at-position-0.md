---
title: "Unexpected Token in JSON at Position 0: How to Fix It"
category: "JSON Guides"
excerpt: "That error almost never means your JSON is broken. It usually means you didn't get JSON at all. Here's how to find out what you did get, and fix it in a few minutes."
meta_description: "Getting \"Unexpected token in JSON at position 0\"? Learn what the error really means, how to see what your API returned, and how to fix each common cause."
meta_keywords: "unexpected token in json at position 0, unexpected token < in json, is not valid json, json parse error, unexpected end of json input"
tags: "JSON, Debugging, JavaScript, APIs"
published_at: "2026-10-15T09:30:00+00:00"
author_name: "Faisal Ahmad"
---
You call an API, pass the response to `JSON.parse()` or `response.json()`, and the console throws this at you:

```
SyntaxError: Unexpected token < in JSON at position 0
```

Newer versions of Chrome and Node word it a little differently:

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

Firefox says `JSON.parse: unexpected character at line 1 column 1 of the JSON data`, and Safari says `JSON Parse error: Unrecognized token '<'`. Same problem, four different sentences.

Here's the part most answers skip. When the error points at **position 0**, the parser gave up on the very first character. That means the text you handed it was never JSON to begin with. So staring at your JSON won't help. You need to see what actually came back.

## Step one: look at the raw response

Don't parse anything yet. Read the body as plain text and print it, along with the status code and the content type:

```javascript
const res = await fetch('/api/users');
const text = await res.text();

console.log(res.status, res.headers.get('content-type'));
console.log(text.slice(0, 300));
```

Nine times out of ten the problem is obvious the second you see this output. The first character tells you most of the story:

| First character | What you probably got |
|---|---|
| `<` | An HTML page: a 404, a login page, an error page or your app's `index.html` |
| Nothing at all | An empty body, often from a 204 or a failed request |
| `u` | The string `"undefined"` |
| `[` followed by `o` | The string `"[object Object]"` |
| An invisible character | A byte order mark (BOM) at the start of a file |
| `'` | Single quotes, which JSON doesn't allow |

If you'd rather not dig through the console, paste the response into our [JSON Formatter](/json-formatter/). It points to the exact line and column where parsing stops, which is quicker than counting characters by hand.

## Cause 1: the server sent HTML

This is the big one. The `<` is the start of `<!DOCTYPE html>` or `<html>`. Your code asked for JSON and got a web page instead. The usual reasons:

- **Wrong URL.** A typo, a missing `/api` prefix or a trailing slash the server doesn't expect. The server answers with its 404 page, which is HTML.
- **Dev server fallback.** Tools like Vite or Create React App serve `index.html` for any path they don't recognise. If your API isn't proxied correctly, `/api/users` quietly returns your own front end.
- **You're not logged in.** The request gets redirected to a login page. `fetch` follows redirects by default, so you end up parsing the login form.
- **The server crashed.** A 500 error from Nginx, Apache or your framework usually comes back as an HTML error page.

The fix is to check the response before you parse it:

```javascript
const res = await fetch('/api/users');

if (!res.ok) {
  throw new Error(`Request failed: ${res.status}`);
}

const type = res.headers.get('content-type') || '';
if (!type.includes('application/json')) {
  const body = await res.text();
  throw new Error(`Expected JSON, got ${type}: ${body.slice(0, 100)}`);
}

const data = await res.json();
```

Now when something goes wrong you get an error that tells you what happened, instead of a parser complaining about a `<`.

## Cause 2: the body was empty

An empty string isn't valid JSON either. In that case the message changes to:

```
SyntaxError: Unexpected end of JSON input
```

This happens with `204 No Content` responses, with `DELETE` endpoints that return nothing, and with requests blocked by CORS or killed by a timeout. If an endpoint can legitimately return nothing, handle that case on purpose:

```javascript
const text = await res.text();
const data = text ? JSON.parse(text) : null;
```

## Cause 3: you parsed something that wasn't a string

`JSON.parse()` turns its argument into a string first. That leads to two classic mistakes.

The first is parsing a variable that's `undefined`, often from `localStorage.getItem()` on a key that was never set, or a missing field. JavaScript turns it into the text `undefined`, and the parser fails on the `u`. Recent Chrome versions say so directly: `"undefined" is not valid JSON`.

The second is parsing something that's already an object. Axios, jQuery and `response.json()` all hand you parsed data. Parse it again and JavaScript converts the object to the string `[object Object]`, so the parser fails on the `o` right after the bracket.

```javascript
const res = await axios.get('/api/users');
JSON.parse(res.data); // wrong: res.data is already an object
console.log(res.data); // right
```

If you're not sure what you're holding, `console.log(typeof value)` settles it in one line.

## Cause 4: a BOM at the start of the file

Files saved by some Windows editors start with a byte order mark, the invisible character `U+FEFF`. You can't see it in most editors, but the parser can. The error points at position 0 and you're looking at a perfectly normal `{`.

Strip it before parsing:

```javascript
const clean = text.replace(/^﻿/, '');
const data = JSON.parse(clean);
```

In Node, reading a file with `fs.readFileSync(path, 'utf8')` keeps the BOM, so the same fix applies there. Better still, set your editor to save files as UTF-8 without BOM.

## Cause 5: it looks like JSON but isn't

Sometimes the text really is meant to be JSON, it's just written the JavaScript way. These all fail:

```javascript
{'name': 'Asha'}      // single quotes
{name: "Asha"}        // unquoted key
{"name": "Asha",}     // trailing comma
```

Only the first two fail right at the start. With single quotes or an unquoted key, the parser hits a problem at position 1, just after the opening brace, and newer Chrome says `Expected property name or '}' in JSON at position 1`. A trailing comma fails further along, on the closing brace.

If the data was typed by hand or copied out of a code file, run it through the [JSON Fixer](/json-fixer/). It converts single quotes, quotes bare keys and removes trailing commas, then lists the fixes it applied.

## Cause 6: JSON inside a string

Some APIs return JSON that has been encoded twice, so the body is a string holding escaped JSON:

```
"{\"name\":\"Asha\",\"age\":31}"
```

Parsing this once gives you a string, not an object. Calling `.name` on it returns `undefined`, and passing it somewhere that expects an object causes strange errors further down the line. Parse it a second time, or paste it into the [String to JSON](/string-json-to-json/) converter to unescape it and see the real structure. Then, if you control the server, find where the data gets stringified twice and fix it there.

## The same error in Python

Python's `json` module reports the same problem in its own words:

```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

`char 0` is the same as position 0, and the usual causes are the same too: an HTML page or an empty body. With `requests`, print the response before you call `.json()`:

```python
r = requests.get(url, timeout=10)
print(r.status_code, r.headers.get("Content-Type"))
print(r.text[:300])
```

A BOM gets its own message in Python: `Unexpected UTF-8 BOM (decode using utf-8-sig)`. The error tells you the fix. Open the file with `encoding="utf-8-sig"` and Python drops the BOM for you.

## A quick checklist

When you see a JSON error at position 0, go through these in order:

1. Print the status code, the content type and the first 300 characters of the raw body.
2. If it starts with `<`, find out why the server sent HTML: wrong URL, missing proxy, login redirect or a server error.
3. If it's empty, handle empty responses on purpose.
4. If you're passing a variable, check it with `typeof` before parsing.
5. If the text looks fine, check for a BOM or JavaScript-style quotes and commas.

Most of the time you'll be done by step two. The error message makes it sound like a syntax problem, but it's really telling you to go and look at what came back.
