import { html, useState, useEffect, useRef, useCallback } from "../lib.js";
import { LANGUAGES } from "../config.js";
import { promptHtml } from "../util.js";
import * as api from "../api.js";
import { SampleData } from "./SampleData.js";
import { CodeEditor } from "./CodeEditor.js";
import { ResultPanel } from "./ResultPanel.js";

export function ProblemView({ pid, track, onStatus }) {
  const [p, setP] = useState(null);
  const [result, setResult] = useState(null);
  const handle = useRef(null);          // editor: { getValue, getSelection }
  const actions = useRef({});

  useEffect(() => {
    setP(null); setResult(null);
    api.getProblem(pid, track).then(setP);
  }, [pid, track]);

  async function doCheck() {
    setResult({ kind: "running",
      msg: track === "pyspark" ? "Running... (first PySpark run warms Spark, a few seconds)" : "Running..." });
    const res = await api.checkAnswer(pid, track, handle.current.getValue());
    setResult({ kind: "check", res });
    onStatus(pid, track, res.status);
  }
  async function doSave() {
    await api.saveAnswer(pid, track, handle.current.getValue());
    setResult({ kind: "info", msg: "Saved to answers/" + track + "/" + pid });
  }
  async function doHint() { setResult({ kind: "hint", text: (await api.getHint(pid)).hint }); }
  async function doReveal() {
    if (!confirm(`Reveal the reference solution for ${pid} (${track})?`)) return;
    setResult({ kind: "reveal", track, solution: (await api.reveal(pid, track)).solution });
  }
  async function doScratch(sql) {
    setResult({ kind: "running", msg: "Running selection..." });
    setResult({ kind: "scratch", res: await api.runScratch(sql) });
  }
  function runShortcut() {
    const sel = (handle.current?.getSelection() || "").trim();
    if (track === "sql" && sel) doScratch(sel); else doCheck();
  }
  actions.current.runShortcut = runShortcut;
  const onRun = useCallback(() => actions.current.runShortcut(), []);

  if (!p) return html`<div className="center">Loading…</div>`;
  const lang = LANGUAGES.find((l) => l.id === track) || LANGUAGES[0];
  const hint = track === "sql"
    ? "⌘/Ctrl+↵ run · select SQL + ⌘/Ctrl+↵ runs the selection · ⌘/Ctrl+Space autocomplete · ⌘/Ctrl+E comments"
    : "⌘/Ctrl+↵ run · ⌘/Ctrl+Space autocomplete · ⌘/Ctrl+E comments";

  return html`
    <div>
      <h1>${p.id} - ${p.category} / ${p.difficulty}</h1>
      <div className="meta">
        <span className="chip">tables: <b>${p.tables.join(", ") || "-"}</b></span>
        <span className="chip">expected cols: <b>${p.columns.join(", ") || "-"}</b></span>
        <span className="chip">track: <b>${track}</b></span>
        ${p.ordered ? html`<span className="chip"><b>order-sensitive</b></span>` : null}
      </div>
      <div className="prompt" dangerouslySetInnerHTML=${{ __html: promptHtml(p.prompt) }}></div>
      <${SampleData} tables=${p.tables} samples=${p.samples} />
      <${CodeEditor} key=${pid + ":" + track} initial=${p.answer} mode=${lang.mode}
                     lineComment=${track === "sql" ? "--" : "#"} onRun=${onRun} handle=${handle} />
      <div className="toolbar">
        <button className="primary" onClick=${doCheck}>Run / Check<span className="kbd">⌘↵</span></button>
        <button onClick=${doSave}>Save</button>
        <button className="ghost" onClick=${doHint}>Hint</button>
        <button className="ghost" onClick=${doReveal}>Reveal</button>
        <span className="runhint">${hint}</span>
      </div>
      <div className="result"><${ResultPanel} state=${result} /></div>
    </div>`;
}
