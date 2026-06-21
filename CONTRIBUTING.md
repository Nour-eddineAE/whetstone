# Contributing

Thanks for wanting to extend this. The project is deliberately small and
data-driven - adding a problem, a cheat sheet, or even a whole new language is a
handful of files, no framework surgery. Everything flows through one engine
(`pengine/grader.py`) so the CLI and the web UI can never disagree.

## Setup

```bash
pip install -r requirements.txt
python manage.py seed        # build data + scaffold answer stubs
python manage.py check all --ref   # sanity check: every reference solution PASSes
```

---

## Add a new problem

A problem is one markdown file plus two reference solutions. The answer stubs
are scaffolded for you.

1. **Write the prompt** - `problems/pNN.md` (use the next free number). The file
   is YAML-style frontmatter followed by the prompt body:

   ```markdown
   ---
   id: p29
   category: window            # joins | window | patterns | sparkops |
                               # aggregation | cte | dates | subquery | <new>
   difficulty: med             # easy | med | hard
   tracks: sql, pyspark        # one or both
   ordered: false              # true only if row order is part of the answer
   columns: dept, headcount    # EXACT expected output columns, in order
   tables: employees, departments
   hint: One-line nudge shown by `hint` / the Hint button.
   ---

   Describe the task. State the expected output columns explicitly so the
   solver knows the target shape.
   ```

   `columns` is the contract: the grader compares result sets positionally, so
   column **order** matters but column **names** do not.

2. **Write the reference solutions** (these are what `--ref` grades and what
   `reveal` shows):
   - `solutions/sql/pNN.sql` - a query returning exactly `columns`.
   - `solutions/pyspark/pNN.py` - a `solve(spark, dfs)` returning a DataFrame.
     `dfs` is a dict keyed by table name (`employees`, `departments`, `events`,
     `transactions`, `user_tags`).

   Only provide the solution for the tracks listed in `tracks`.

3. **Scaffold + verify:**

   ```bash
   python manage.py seed                 # creates answers/{sql,pyspark}/pNN stubs
   python manage.py check all --ref      # your new reference must PASS
   ```

   `seed` discovers problems from `problems/*.md` automatically - no list to
   update. It never overwrites an existing answer file.

If you add a brand-new `category`, give it a pretty label in
`webapp/static/js/config.js` (`CATEGORY_LABELS`); unknown categories just
title-case by default.

---

## Add a cheat sheet

1. Drop a markdown file in `cheatsheets/`, numbered for ordering:
   `cheatsheets/NN-my-topic.md`. Start it with an `# H1` - that becomes the
   title and the slug (`my-topic`).
2. Use fenced code blocks with a language tag (```` ```sql ````, ```` ```python ````)
   so highlight.js colors them in the browser.

That's it - `/api/cheatsheets` lists every file in the folder and the Cheats
sub-nav picks it up on reload. No registration step.

---

## Add a language or a section (it's data-driven)

The whole left rail and the language picker are driven by arrays in
`webapp/static/js/config.js`.

**New language** (e.g. add Polars): one entry.

```js
export const LANGUAGES = [
  { id: "sql",     label: "SQL",     mode: "sql" },
  { id: "pyspark", label: "PySpark", mode: "python" },
  { id: "polars",  label: "Polars",  mode: "python" },   // <- added
];
```

Then add `tracks: polars` to the problems that support it, drop
`solutions/polars/pNN.py`, and teach `pengine/grader.py` how to execute that
track. The UI filtering and editor mode need no further changes.

**New section** (a 4th rail item): one config entry + one render case.

```js
// config.js
export const SECTIONS = [
  ...,
  { id: "notes", label: "Notes", icon: "book" },   // <- added
];
```

```js
// main.js - add the matching branch
else if (section === "notes") content = html`<${Notes} />`;
```

Build the `Notes` component under `static/js/components/` and you're done.

---

## Ground rules

- **Don't change the grader's semantics.** `pengine/grader.py` is the single
  source of truth; the CLI and UI both depend on it behaving identically.
- **Keep components small.** One component per file under
  `static/js/components/`. No build step - React + htm load from a CDN.
- Run `python manage.py check all --ref` before opening a PR. All references
  must PASS.
