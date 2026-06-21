import { html, useState } from "../lib.js";
import * as api from "../api.js";
import { StatusIcon } from "./StatusIcon.js";

// Full-width table: every (problem, track) with its saved status. "Re-run all"
// re-grades each saved answer file (stubs stay SKIP, warm Spark keeps it quick).
export function Scoreboard({ problems, status, onStatus }) {
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  const rows = [];
  problems.forEach((p) => p.tracks.forEach((t) =>
    rows.push({ id: p.id, cat: p.category, track: t, st: status[p.id + ":" + t] || "" })));

  async function rerun() {
    setBusy(true);
    const combos = [];
    problems.forEach((p) => p.tracks.forEach((t) => combos.push([p.id, t])));
    let i = 0;
    for (const [id, t] of combos) {
      setMsg(`grading ${id} ${t} (${++i}/${combos.length})`);
      const res = await api.checkFile(id, t);
      onStatus(id, t, res.status);
    }
    setMsg("done"); setBusy(false);
  }

  return html`
    <main>
      <h1>Scoreboard</h1>
      <div className="toolbar">
        <button className="primary" disabled=${busy} onClick=${rerun}>Re-run all attempted</button>
        <span className="muted">${msg}</span>
      </div>
      <table className="scoretable">
        <thead><tr><th>ID</th><th>Category</th><th>Track</th><th>Status</th></tr></thead>
        <tbody>
          ${rows.map((r, i) => html`
            <tr key=${i}>
              <td>${r.id}</td><td>${r.cat}</td><td>${r.track}</td>
              <td><span className="scell"><${StatusIcon} status=${r.st} /> ${r.st || "untried"}</span></td>
            </tr>`)}
        </tbody>
      </table>
    </main>`;
}
