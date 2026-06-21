import { html } from "../lib.js";

const cell = (v) =>
  v === null || v === undefined ? html`<span className="null">NULL</span>` : String(v);

// Simple value table. `cols` = header names, `rows` = array of arrays.
export function Table({ cols, rows }) {
  return html`
    <table>
      <thead><tr>${cols.map((c, i) => html`<th key=${i}>${c}</th>`)}</tr></thead>
      <tbody>
        ${rows.map((r, ri) => html`
          <tr key=${ri}>${r.map((v, ci) => html`<td key=${ci}>${cell(v)}</td>`)}</tr>`)}
      </tbody>
    </table>`;
}
