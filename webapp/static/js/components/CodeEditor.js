import { html, useEffect, useRef } from "../lib.js";

// CodeMirror needs a fuller SQL keyword set than the generic text/x-sql mode
// ships with (LEFT/JOIN/OVER/window funcs), so we supply it explicitly.
const wordSet = (s) => Object.fromEntries(s.split(/\s+/).filter(Boolean).map((w) => [w.toLowerCase(), true]));
const SQL_KEYWORDS = wordSet(`
  select from where group by having order limit offset with recursive as distinct
  join left right inner outer full cross natural lateral on using union all intersect except
  and or not in exists is null between like ilike similar to escape qualify window filter within
  case when then else end cast asc desc nulls first last partition over rows range groups
  unbounded preceding following current row insert into values update set delete create table view drop`);
// Seed-data schema, so SQL autocomplete suggests real table + column names.
const SQL_TABLES = {
  employees: ["emp_id", "name", "dept", "salary", "manager_id", "hire_date"],
  departments: ["dept_id", "dept_name"],
  events: ["user_id", "event_type", "event_ts"],
  transactions: ["txn_id", "user_id", "amount", "txn_date"],
  user_tags: ["user_id", "tags"],
};
const SQL_BUILTIN = wordSet(`
  int integer bigint smallint double float decimal numeric varchar char text date timestamp time boolean
  count sum avg min max median stddev variance row_number rank dense_rank ntile lag lead first_value last_value
  coalesce nullif greatest least unnest string_split strftime date_trunc date_part extract datediff date_add date_sub
  percentile percentile_cont percentile_disc array_agg`);

// IntelliJ-style comment toggle for the textarea fallback.
function toggleTextareaComment(ta, prefix) {
  const v = ta.value, bare = prefix.trimEnd();
  let s = v.lastIndexOf("\n", ta.selectionStart - 1) + 1;
  let e = ta.selectionEnd; if (e > s && v[e - 1] === "\n") e--;
  let end = v.indexOf("\n", e); if (end === -1) end = v.length;
  const lines = v.slice(s, end).split("\n");
  const allOff = lines.every((l) => l.trim() === "" || l.trimStart().startsWith(bare));
  const out = lines.map((l) => {
    if (allOff) { const i = l.indexOf(bare); return i < 0 ? l : l.slice(0, i) + l.slice(i + bare.length).replace(/^ /, ""); }
    return l.trim() === "" ? l : prefix + l;
  }).join("\n");
  ta.setRangeText(out, s, end, "select");
}

// Mounts once; the parent gives a new `key` on (pid, language) change to remount.
// `handle` is a ref the parent reads getValue()/getSelection() from.
export function CodeEditor({ initial, mode, lineComment, onRun, handle }) {
  const hostRef = useRef();
  useEffect(() => {
    const host = hostRef.current;
    const CM = window.CodeMirror;
    const sqlMode = { name: "sql", keywords: SQL_KEYWORDS, builtin: SQL_BUILTIN,
                      atoms: { true: true, false: true, null: true } };
    if (CM) {
      const toggle = (cm) => cm.toggleComment({ indent: true, lineComment });
      // Cmd/Ctrl-Space: SQL gets table + column aware hints, Python gets word hints.
      const complete = (cm) => {
        const hint = mode === "sql"
          ? (c) => CM.hint.sql(c, { tables: SQL_TABLES })
          : CM.hint.anyword;
        cm.showHint({ hint, completeSingle: false });
      };
      const cm = CM(host, {
        value: initial, mode: mode === "sql" ? sqlMode : "python",
        theme: "material-darker", lineNumbers: true, indentUnit: 4, tabSize: 4, matchBrackets: true,
        extraKeys: { "Cmd-Enter": () => onRun(), "Ctrl-Enter": () => onRun(),
                     "Cmd-E": toggle, "Ctrl-E": toggle, "Cmd-/": toggle, "Ctrl-/": toggle,
                     "Cmd-Space": complete, "Ctrl-Space": complete },
      });
      handle.current = { getValue: () => cm.getValue(),
                         getSelection: () => (cm.somethingSelected() ? cm.getSelection() : "") };
    } else {
      const ta = document.createElement("textarea");
      ta.className = "fallback"; ta.value = initial; host.appendChild(ta);
      ta.addEventListener("keydown", (e) => {
        const m = e.metaKey || e.ctrlKey;
        if (m && e.key === "Enter") { e.preventDefault(); onRun(); }
        else if (m && (e.key === "e" || e.key === "/")) { e.preventDefault(); toggleTextareaComment(ta, lineComment + " "); }
      });
      handle.current = { getValue: () => ta.value,
        getSelection: () => (ta.selectionStart !== ta.selectionEnd ? ta.value.slice(ta.selectionStart, ta.selectionEnd) : "") };
    }
    return () => { host.innerHTML = ""; handle.current = null; };
  }, []);
  return html`<div className="editorwrap" ref=${hostRef}></div>`;
}
