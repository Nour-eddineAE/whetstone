import { html, useEffect, useRef } from "../lib.js";
import * as api from "../api.js";

// Async Jedi-backed completion for Python: introspects the selected interpreter's
// installed libraries (pyspark, pandas, types). Marked async so CodeMirror waits
// for the server round-trip.
function pythonHint(cm, callback) {
  const cur = cm.getCursor();
  const line = cm.getLine(cur.line).slice(0, cur.ch);
  const prefix = (line.match(/[A-Za-z0-9_]*$/) || [""])[0];
  const from = { line: cur.line, ch: cur.ch - prefix.length };
  api.completePython(cm.getValue(), cur.line, cur.ch).then((res) => {
    const list = (res.completions || []).map((c) => ({
      text: c.name,
      className: "cm-hint-" + (c.type || "x"),
      render(el) {                       // editor-style row, full signature on hover
        el.title = c.signature || c.name;
        const name = document.createElement("span");
        name.className = "h-name"; name.textContent = c.name; el.appendChild(name);
        if (c.params) {
          const p = document.createElement("span");
          p.className = "h-params"; p.textContent = `(${c.params.join(", ")})`;
          el.appendChild(p);
        }
        if (c.type) {
          const t = document.createElement("span");
          t.className = "h-type"; t.textContent = c.type; el.appendChild(t);
        }
      },
    }));
    callback({ list, from, to: cur });
  }).catch(() => callback({ list: [], from, to: cur }));
}
pythonHint.async = true;

// Text typed inside the *current* call: walk back from the cursor to the "("
// that opens the enclosing call (skipping balanced nested brackets). Returns the
// argument substring, or null if the cursor isn't inside a "(" call.
function currentCallArgs(cm, cur) {
  const text = cm.getRange({ line: 0, ch: 0 }, cur);
  let depth = 0;
  for (let i = text.length - 1; i >= 0; i--) {
    const c = text[i];
    if (c === ")" || c === "]" || c === "}") depth++;
    else if (c === "(") { if (depth === 0) return text.slice(i + 1); depth--; }
    else if (c === "[" || c === "{") { if (depth === 0) return null; depth--; }   // in a literal, not a call
  }
  return null;
}

// Keyword args already written in the call (any depth — good enough to suppress
// re-suggesting them). e.g. "value=0, subset=" -> ["value", "subset"].
function usedKeywords(argText) {
  const used = [], re = /([A-Za-z_]\w*)\s*=(?!=)/g;
  let m; while ((m = re.exec(argText))) used.push(m[1]);
  return used;
}

// Build a completion list of the params NOT yet supplied for the call the cursor
// sits in. Drops self/cls, *args/**kwargs, params already passed positionally
// (index) or by keyword, and filters by the word typed at the cursor.
function paramHint(cm, cur, sig) {
  const args = currentCallArgs(cm, cur) || "";
  const used = usedKeywords(args);
  const idx = typeof sig.index === "number" ? sig.index : -1;
  const line = cm.getLine(cur.line).slice(0, cur.ch);
  const prefix = (line.match(/[A-Za-z0-9_]*$/) || [""])[0];
  const from = { line: cur.line, ch: cur.ch - prefix.length };

  const list = (sig.params || []).filter((p, i) => {
    if (p.name === "self" || p.name === "cls") return false;
    if (/VAR_/.test(p.kind || "")) return false;            // *args / **kwargs
    if (used.includes(p.name)) return false;                // already given by keyword
    if (idx >= 0 && i < idx) return false;                  // already filled positionally
    return p.name.toLowerCase().startsWith(prefix.toLowerCase());
  }).map((p) => ({
    text: p.name + "=",
    className: "cm-hint-param",
    render(el) {
      const desc = (p.desc || p.name).replace(/^param\s+/, "");
      const name = document.createElement("span");
      name.className = "h-name"; name.textContent = p.name; el.appendChild(name);
      const type = desc.slice(p.name.length).replace(/^:\s*/, "");   // "ColumnOrName"
      if (type) {
        const t = document.createElement("span");
        t.className = "h-type"; t.textContent = type; el.appendChild(t);
      }
    },
  }));
  return { list, from, to: cur };
}

// Singleton hover tooltip showing a name's signature + first docstring line.
let _tip;
function tipEl() {
  if (!_tip) {
    _tip = document.createElement("div");
    _tip.className = "cm-sig-tip";
    _tip.style.display = "none";
    document.body.appendChild(_tip);
  }
  return _tip;
}
function showTip(x, y, sig, doc) {
  const el = tipEl();
  el.innerHTML = "";
  const s = document.createElement("div");
  s.className = "tip-sig"; s.textContent = sig; el.appendChild(s);
  if (doc) {
    const d = document.createElement("div");
    d.className = "tip-doc"; d.textContent = doc.split("\n")[0].slice(0, 200);
    el.appendChild(d);
  }
  el.style.display = "block";
  el.style.left = Math.min(x + 12, window.innerWidth - el.offsetWidth - 12) + "px";
  el.style.top = (y + 18) + "px";
}
function hideTip() { if (_tip) _tip.style.display = "none"; }

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

// Known string-literal value sets that Jedi can't infer (they're plain `str`).
// Keyed by parameter name -> the valid literals. Drives value completion inside
// the quotes, e.g. how="<here>" on DataFrame.join.
const STRING_VALUES = {
  how: ["inner", "cross", "outer", "full", "fullouter", "full_outer",
        "left", "leftouter", "left_outer", "right", "rightouter", "right_outer",
        "semi", "leftsemi", "left_semi", "anti", "leftanti", "left_anti"],
};
// Practice dataset schema (same tables back the PySpark dfs and the SQL problems).
const ALL_COLUMNS = [...new Set(Object.values(SQL_TABLES).flat())];


// VSCode-style value completion for string arguments. Three cases:
//   dfs["<here>"]          -> table/dfs keys
//   how="<here>"           -> STRING_VALUES for that param
//   select("<here>", ...)  -> column names (any string arg in a call)
//   how=<here> (no quotes) -> same STRING_VALUES, inserts with quotes
// Returns a show-hint payload, or null when the cursor isn't in a relevant context.
function stringValueHint(cm, cur) {
  const tok = cm.getTokenAt(cur);
  const line = cm.getLine(cur.line).slice(0, cur.ch);

  // Case A: cursor is inside an open string literal
  if (tok.type === "string" || tok.type === "string-2") {
    const m = line.match(/(["'])([^"']*)$/);      // open quote + typed text
    if (!m) return null;
    const typed = m[2];
    const openIdx = cur.ch - typed.length - 1;
    const before = cm.getLine(cur.line).slice(0, openIdx).trimEnd();

    let values = null;
    if (/dfs\s*\[$/.test(before)) {
      values = Object.keys(SQL_TABLES);
    } else {
      const kw = before.match(/([A-Za-z_]\w*)\s*=$/);
      if (kw && STRING_VALUES[kw[1]]) values = STRING_VALUES[kw[1]];
      else if (/[(,]\s*$/.test(before)) values = ALL_COLUMNS;
    }
    if (!values) return null;

    const t = typed.toLowerCase();
    const list = values.filter((v) => v.toLowerCase().includes(t))
                       .map((v) => ({ text: v, displayText: v, className: "cm-hint-str" }));
    if (!list.length) return null;
    return { list, from: { line: cur.line, ch: openIdx + 1 }, to: cur };
  }

  // Case B: cursor at `param=` or `param=<unquoted partial>` — inserts value with quotes.
  // The partial ([A-Za-z_]*) at end must reach $ so it won't fire once the call is closed.
  const kwB = line.match(/([A-Za-z_]\w*)\s*=\s*([A-Za-z_]*)$/);
  if (kwB && STRING_VALUES[kwB[1]]) {
    const typed = kwB[2].toLowerCase();
    const list = STRING_VALUES[kwB[1]]
      .filter((v) => !typed || v.toLowerCase().startsWith(typed))
      .map((v) => ({ text: `"${v}"`, displayText: v, className: "cm-hint-str" }));
    if (!list.length) return null;
    return { list, from: { line: cur.line, ch: cur.ch - kwB[2].length }, to: cur };
  }

  return null;
}

// On-type Python helper: bracket depth of all text above `line`, so we can tell
// whether a method chain sits inside unclosed (), [], {} (implicit continuation,
// backslash redundant). Naive scan — does not skip brackets in strings/comments.
const OPENERS = "([{", CLOSERS = ")]}";
function netOpenBefore(cm, line) {
  let depth = 0;
  for (let i = 0; i < line; i++) {
    for (const ch of cm.getLine(i)) {
      if (OPENERS.includes(ch)) depth++;
      else if (CLOSERS.includes(ch)) depth = Math.max(0, depth - 1);
    }
  }
  return depth;
}

// If `dotLine` is a method-chain continuation (first non-ws char is "."), append
// " \" to the line above so the continuation is valid. Shared by both triggers:
// typing "." as the first char of a new line, and pressing Enter right before an
// existing ".". Skips lines already ending in "\", lines ending in an open
// bracket, and chains inside unclosed (), [], {} where the backslash is redundant.
// The replaceRange below has no "+input" origin, so the change listener ignores it.
function applyContinuation(cm, dotLine) {
  if (dotLine === 0) return;
  if (!/^\s*\./.test(cm.getLine(dotLine))) return;     // line must start with "."
  const prev = cm.getLine(dotLine - 1);
  const t = prev.replace(/\s+$/, "");
  if (t === "") return;                                  // nothing to continue
  if (t.endsWith("\\")) return;                          // already a continuation
  if (OPENERS.includes(t[t.length - 1])) return;         // open bracket: implicit continuation
  if (netOpenBefore(cm, dotLine) > 0) return;            // inside (), [], {}: redundant
  cm.replaceRange(" \\", { line: dotLine - 1, ch: t.length },
                         { line: dotLine - 1, ch: prev.length });
}

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
    let teardownHover = null;
    const sqlMode = { name: "sql", keywords: SQL_KEYWORDS, builtin: SQL_BUILTIN,
                      atoms: { true: true, false: true, null: true } };
    if (CM) {
      const toggle = (cm) => cm.toggleComment({ indent: true, lineComment });
      // Cmd/Ctrl-Space. SQL: table + column aware hints. Python: context-aware,
      // in priority order --
      //   1. inside a string literal with a known value set (how="...", dfs["..."],
      //      column args) -> those literals
      //   2. inside a call's argument list -> the params not yet supplied
      //   3. otherwise -> Jedi identifier/member completion
      const complete = (cm) => {
        if (mode === "sql") {
          cm.showHint({ hint: (c) => CM.hint.sql(c, { tables: SQL_TABLES }), completeSingle: false });
          return;
        }
        const cur = cm.getCursor();
        // Recomputing closures so the popup refilters live as more is typed.
        const empty = () => ({ list: [], from: cm.getCursor(), to: cm.getCursor() });
        if (stringValueHint(cm, cur)) {
          cm.showHint({ hint: () => stringValueHint(cm, cm.getCursor()) || empty(), completeSingle: false });
          return;
        }
        api.signaturePython(cm.getValue(), cur.line, cur.ch).then((res) => {
          const sig = (res.signatures || [])[0];
          if (sig && currentCallArgs(cm, cur) !== null) {
            const data = paramHint(cm, cm.getCursor(), sig);
            if (data.list.length) {
              cm.showHint({ hint: () => paramHint(cm, cm.getCursor(), sig), completeSingle: false });
              return;
            }
          }
          cm.showHint({ hint: pythonHint, completeSingle: false });
        }).catch(() => cm.showHint({ hint: pythonHint, completeSingle: false }));
      };
      const cm = CM(host, {
        value: initial, mode: mode === "sql" ? sqlMode : "python",
        theme: "material-darker", lineNumbers: true, indentUnit: 4, tabSize: 4, matchBrackets: true,
        autoCloseBrackets: "()[]{}''\"\"``",   // wrap selection / auto-close pairs
        extraKeys: { "Cmd-Enter": () => onRun(), "Ctrl-Enter": () => onRun(),
                     "Cmd-E": toggle, "Ctrl-E": toggle, "Cmd-/": toggle, "Ctrl-/": toggle,
                     "Shift-Tab": "indentLess",   // dedent one unit (not jump to line start)
                     "Cmd-Space": complete, "Ctrl-Space": complete },
      });
      // On-type (Python only): keep a method chain valid by adding " \" to the line
      // above when a line becomes a ".chain" continuation. Two ways that happens:
      //  (a) typing "." as the first non-ws char of a new line  -> inputRead
      //  (b) pressing Enter right before an existing "."         -> the split makes
      //      the new line start with "." -> caught via the "change" newline handler
      // Floats (x = 3.14) never start a line with ".", so they're skipped. The
      // helper's replaceRange has no "+input" origin, so it won't re-trigger (b).
      if (mode !== "sql") {
        cm.on("inputRead", (_cm, change) => {
          if (change.text.length !== 1 || change.text[0] !== ".") return;
          const cur = cm.getCursor();
          if (!/^\s*\.$/.test(cm.getLine(cur.line).slice(0, cur.ch))) return; // "." just typed, first on line
          applyContinuation(cm, cur.line);
        });
        cm.on("change", (_cm, change) => {
          if (change.origin !== "+input" || change.text.length < 2) return;   // a typed newline (Enter)
          applyContinuation(cm, change.from.line + 1);                         // the freshly split-off line
        });

        // Auto-trigger completion as you type (VSCode-style): identifiers, after a
        // ".", inside "(" / after "=" or ",", and inside strings that have a known
        // value set. Debounced; skipped in comments and while a popup is already open.
        let acTimer;
        cm.on("inputRead", (_cm, change) => {
          if (change.origin !== "+input") return;
          const cur = cm.getCursor();
          const tok = cm.getTokenAt(cur);
          if (tok.type === "comment") return;
          const text = change.text[0] || "";
          const inStr = tok.type === "string" || tok.type === "string-2";
          let fire;
          if (inStr) {
            fire = !!stringValueHint(cm, cur);
          } else if (text === ",") {
            fire = currentCallArgs(cm, cur) !== null;   // only trigger inside a call
          } else {
            fire = /[A-Za-z_.=(]/.test(text);
          }
          if (!fire) return;
          clearTimeout(acTimer);
          acTimer = setTimeout(() => { if (!cm.state.completionActive) complete(cm); }, 150);
        });

      }
      // Hover (Python only): show the signature + doc of the name under the
      // pointer. Debounced, deduped per token, and only for callables/classes so
      // hovering plain variables stays quiet.
      let hoverTimer, hoverKey, hoverSeq = 0;
      const wrap = cm.getWrapperElement();
      const onMove = (e) => {
        if (mode === "sql") return;
        clearTimeout(hoverTimer);
        hoverTimer = setTimeout(() => {
          const pos = cm.coordsChar({ left: e.clientX, top: e.clientY }, "window");
          const tok = cm.getTokenAt(pos);
          if (!tok || !/^[A-Za-z_]/.test(tok.string || "")) { hideTip(); hoverKey = null; return; }
          const key = pos.line + ":" + tok.start;
          if (key === hoverKey) return;                // same token: keep current tip
          hoverKey = key;
          const seq = ++hoverSeq, mx = e.clientX, my = e.clientY;
          api.hoverPython(cm.getValue(), pos.line, tok.end).then((r) => {
            if (seq !== hoverSeq) return;              // a newer hover superseded this
            const h = r.info;
            if (!h || !(h.signatures && h.signatures.length)) { hideTip(); return; }
            showTip(mx, my, h.signatures[0], h.doc);
          }).catch(hideTip);
        }, 320);
      };
      const onLeave = () => { clearTimeout(hoverTimer); hoverKey = null; hideTip(); };
      if (mode !== "sql") { wrap.addEventListener("mousemove", onMove); wrap.addEventListener("mouseleave", onLeave); }
      teardownHover = () => { wrap.removeEventListener("mousemove", onMove); wrap.removeEventListener("mouseleave", onLeave); hideTip(); };

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
    return () => { if (teardownHover) teardownHover(); host.innerHTML = ""; handle.current = null; };
  }, []);
  return html`<div className="editorwrap" ref=${hostRef}></div>`;
}
