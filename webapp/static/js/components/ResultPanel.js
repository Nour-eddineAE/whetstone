import { html } from "../lib.js";
import { Table } from "./Table.js";

// Renders whatever the last action produced. Never shows the solution on FAIL.
export function ResultPanel({ state }) {
  if (!state) return null;

  if (state.kind === "running")
    return banner("info", state.msg || "Running...");
  if (state.kind === "info")
    return banner("info", state.msg);
  if (state.kind === "hint")
    return banner("info", "💡 " + state.text);

  if (state.kind === "reveal")
    return html`
      <div>
        <h3 className="muted" style=${{ margin: "6px 0" }}>Reference - ${state.track}</h3>
        <pre className="sol">${state.solution}</pre>
      </div>`;

  if (state.kind === "scratch") {
    const r = state.res;
    if (r.error) return banner("FAIL", "✗ " + r.error);
    const note = r.truncated ? ` (first ${r.rows.length})` : "";
    return html`
      <div>
        ${banner("info", `▶ selection result - ${r.rows.length} row(s)${note} · scratch, not graded`)}
        <div className="scroll" style=${{ marginTop: "10px" }}>
          <${Table} cols=${r.columns} rows=${r.rows} /></div>
      </div>`;
  }

  if (state.kind === "check") return checkResult(state.res);
  return null;
}

function banner(cls, text) {
  return html`<div className=${"banner " + cls}>${text}</div>`;
}

function checkResult(res) {
  if (res.status === "PASS")
    return banner("PASS", `✓ PASS - ${res.expected_count} row(s) match`);
  if (res.status === "SKIP")
    return banner("SKIP", "Not attempted - " + (res.error || ""));

  // FAIL
  if (res.error)
    return html`<div>${banner("FAIL", "✗ FAIL")}
      <p className="muted" style=${{ marginTop: "10px" }}>${res.error}</p></div>`;

  const d = res.diff;
  const cols = res.columns && res.columns.length ? res.columns
    : ((d.only_expected[0] || d.only_actual[0] || []).map((_, i) => "c" + i));
  return html`
    <div>
      ${banner("FAIL", "✗ FAIL")}
      <p className="muted" style=${{ marginTop: "10px" }}>
        expected ${res.expected_count} row(s), got ${res.actual_count} row(s)</p>
      ${d.col_count_mismatch
        ? banner("FAIL", `column count differs: expected ${d.col_count_mismatch[0]}, got ${d.col_count_mismatch[1]}`)
        : null}
      ${res.ordered && d.first_diff
        ? html`<div>
            <p className="muted">first differing row at index ${d.first_diff.index}</p>
            <div className="diffgrid">
              <div className="diffcol"><h3>expected</h3><${Table} cols=${cols} rows=${[d.first_diff.expected]} /></div>
              <div className="diffcol"><h3>yours</h3><${Table} cols=${cols} rows=${[d.first_diff.actual]} /></div>
            </div></div>`
        : html`<div className="diffgrid">
            <div className="diffcol"><h3>in expected, missing from yours</h3>
              ${d.only_expected.length ? html`<${Table} cols=${cols} rows=${d.only_expected} />` : html`<p className="muted">-</p>`}</div>
            <div className="diffcol"><h3>in yours, not expected</h3>
              ${d.only_actual.length ? html`<${Table} cols=${cols} rows=${d.only_actual} />` : html`<p className="muted">-</p>`}</div>
          </div>`}
    </div>`;
}
