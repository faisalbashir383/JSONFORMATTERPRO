---
title: "JSON vs YAML for Config Files: Which One Should You Use?"
category: "JSON Guides"
excerpt: "YAML is easier to read and write by hand. JSON is harder to get wrong. Here's how the two really differ, the YAML traps that catch people out, and a simple way to choose."
meta_description: "JSON vs YAML for configuration files: syntax, comments, the Norway problem, tooling and a simple rule for choosing the right format for your project."
meta_keywords: "json vs yaml, yaml vs json, json or yaml for config, yaml norway problem, convert json to yaml"
tags: "JSON, YAML, Configuration, DevOps"
published_at: "2026-10-18T10:00:00+00:00"
author_name: "Faisal Ahmad"
---
If you've worked on any project with a build step, you've edited both. `package.json` and `tsconfig.json` on one side, a GitHub Actions workflow, a `docker-compose.yml` or a Kubernetes manifest on the other. Ansible, Helm and most CI systems went with YAML. npm, TypeScript, Composer and VS Code went with JSON. Both formats describe the same kind of data: objects, lists, strings, numbers, booleans and null. They just make very different trade-offs.

This post covers where those trade-offs actually matter when you're picking a format for your own config.

## The same config, written both ways

Here's a small service config in JSON:

```json
{
  "service": "billing-api",
  "port": 8080,
  "debug": false,
  "allowed_origins": ["https://app.example.com", "https://admin.example.com"],
  "database": {
    "host": "db.internal",
    "pool_size": 10
  }
}
```

And the same thing in YAML:

```yaml
service: billing-api
port: 8080
debug: false
allowed_origins:
  - https://app.example.com
  - https://admin.example.com
database:
  host: db.internal
  pool_size: 10
```

The YAML version has no braces, no commas and almost no quotes. Nesting comes from indentation. For a file people open and edit by hand every week, that's a real difference. You can read it at a glance, and code review diffs stay short.

The JSON version is noisier, but every rule is spelled out. A string is in double quotes, always. A list is in square brackets, always. There's very little the parser has to guess.

## Comments: YAML has them, JSON doesn't

This is often the deciding factor. YAML lets you write `# why this is set to 10` next to a value. Standard JSON has no comment syntax at all, so a file like this won't parse:

```json
{
  // retry three times before giving up
  "retries": 3
}
```

Some tools work around this. `tsconfig.json` and VS Code's settings files accept comments because they use a looser variant often called JSONC. But plain `JSON.parse()` won't, and neither will most JSON libraries. If you need to explain settings inside the file itself, that points you towards YAML.

## Where YAML bites back

YAML's flexibility comes from the parser guessing what type a value is. Most of the time it guesses right. The cases where it doesn't are well known, and worth knowing before you choose it.

**The Norway problem.** Under the older YAML 1.1 rules, the words `yes`, `no`, `on` and `off` are booleans. So a list of country codes like this:

```yaml
countries:
  - GB
  - "IE"
  - NO
```

gives you `["GB", "IE", false]`. Norway turns into `false`. YAML 1.2 fixed this back in 2009, but plenty of widely used parsers still follow 1.1 rules, including PyYAML, the default YAML library in Python. The fix is to quote anything that could be read as a keyword. If you want 1.2 behaviour in Python, ruamel.yaml uses it by default.

**Version numbers become floats.** `version: 3.10` is parsed as the number `3.1`. If you've ever written `python-version: 3.10` in a GitHub Actions workflow and watched it go looking for Python 3.1, this is why. Write it as `"3.10"`.

**Indentation is the syntax.** One space out of place moves a key into a different object, and the file often still parses. You get a valid config that means something else. Tabs aren't allowed for indentation at all, which surprises people whose editor inserts them.

**Some values look like other things.** My favourite: under YAML 1.1, `22:22` isn't a time or a string. It's read as a base-60 number, so you get `1342`. A leading zero, a colon in an unquoted string or a value starting with `*` or `&` can all surprise you the same way. When in doubt, quote it.

None of this makes YAML a bad choice. It means YAML rewards people who know these rules and quietly punishes people who don't. JSON has almost none of these surprises, because it never guesses: `"NO"` is a string and `false` is a boolean, and they don't look alike.

## Features YAML has that JSON lacks

Apart from comments, YAML gives you a few things JSON simply can't do:

- **Multi-line strings.** The `|` block keeps line breaks exactly, which is handy for embedded scripts or certificates. In JSON you'd write one long line full of `\n` escapes.
- **Anchors and aliases.** You can define a block once with `&defaults` and reuse it with `*defaults`, so shared settings don't get copied across five environments.
- **Several documents in one file.** Kubernetes uses `---` separators to keep a Deployment and a Service side by side in the same file.

JSON goes the other way. It's one value per file and nothing else.

## Where JSON is the better fit

JSON wins when machines do most of the reading and writing:

- **APIs and data exchange.** Every language ships a fast JSON parser, and browsers have one built in. YAML parsers are larger, slower and less consistent with each other.
- **Generated files.** Lock files, build manifests and exported settings are written by programs. Nobody needs comments there, and a strict format makes them easier to check.
- **Security.** Some YAML libraries can create arbitrary objects from tags in the file. PyYAML's old `yaml.load()` without a safe loader became a well-known way to run code from an untrusted file. JSON parsers have no such feature.
- **Validation.** JSON Schema is mature, widely supported and works well in editors. You can validate YAML against a JSON Schema too, but the tooling around JSON is simpler.

## So which should you pick?

Here's the rule I'd use: **if people edit it by hand and it's worth explaining, use YAML. If programs write it or send it, use JSON.**

A few practical notes on top of that:

- Go with what your tools expect. If a tool looks for `docker-compose.yml` or `.eslintrc.json`, give it that. Fighting the default is rarely worth it.
- If you choose YAML, quote strings that could be confused with booleans, numbers or dates. It costs you two characters and saves a confusing afternoon.
- If you choose JSON and miss comments, a `"_comment"` key works in a pinch, though the program reading the file will see it as data. Check whether your tool supports JSONC before you go that way.

## Moving between the two

Because both formats describe the same data, converting is safe as long as you keep the type traps above in mind. Every JSON document is also valid YAML 1.2, so going from JSON to YAML is the easy direction.

Our [JSON to YAML converter](/json-to-yaml/) turns a JSON file into clean YAML and can convert it back again. If you're editing YAML by hand, paste it into the [YAML Formatter](/yaml-formatter/) first. It validates the file, fixes the indentation and can sort keys. That makes it much easier to spot a value that landed in the wrong place.

Both formats are fine. What causes trouble is not knowing which rules each one plays by.
