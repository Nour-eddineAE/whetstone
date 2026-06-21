import { html, useState, useEffect } from "../lib.js";
import * as api from "../api.js";

// Settings sections shown in the left pane. Detail for the selected one renders
// on the right (master/detail, like the cheat sheet browser). Add more here.
const SECTIONS = [
  { id: "interpreter", title: "Python interpreter", blurb: "PySpark autocomplete env" },
];

// Pick the Python interpreter used for PySpark autocomplete. Jedi introspects
// that env's installed libraries (pyspark, pandas, types) to power completions.
function InterpreterPanel() {
  const [envs, setEnvs] = useState([]);
  const [manual, setManual] = useState("");
  const [msg, setMsg] = useState("");

  function load() {
    api.getEnvironments().then((d) => setEnvs(d.environments || []));
  }
  useEffect(load, []);

  async function choose(path) {
    setMsg("");
    const r = await api.setInterpreter(path);
    if (r.error) { setMsg(r.error); return; }
    setMsg("interpreter set");
    load();
  }

  return html`
    <section className="settings-section">
      <div className="section-head">
        <h2>Python interpreter</h2>
        <p className="desc">
          PySpark autocomplete reads libraries and types from this interpreter's
          environment. Pick the one where <code>pyspark</code> is installed.
        </p>
      </div>

      <div className="env-list">
        ${envs.map((e) => html`
          <label key=${e.path} className=${"env-row" + (e.current ? " active" : "")}>
            <input type="radio" name="interp" checked=${e.current}
                   onChange=${() => choose(e.path)} />
            <span className="env-main">
              <span className="env-label">${e.label}</span>
              <span className="env-path">${e.path}</span>
            </span>
            ${e.current ? html`<span className="env-tag">Active</span>` : null}
          </label>`)}
      </div>

      <div className="manual-row">
        <span className="manual-label">Custom path</span>
        <div className="manual-interp">
          <input className="path-input" placeholder="/path/to/python"
                 value=${manual} onInput=${(ev) => setManual(ev.target.value)} />
          <button className="primary" disabled=${!manual.trim()}
                  onClick=${() => choose(manual.trim())}>Use this path</button>
        </div>
      </div>
      ${msg ? html`<p className=${"settings-msg" + (msg.includes("set") ? " ok" : " err")}>${msg}</p>` : null}
    </section>`;
}

const PANELS = { interpreter: InterpreterPanel };

export function Settings() {
  const [cur, setCur] = useState(SECTIONS[0].id);
  const Panel = PANELS[cur];
  return html`<>
    <div className="pane">
      <div className="pane-head"><h2 className="pane-title">Settings</h2></div>
      <div className="pane-list">
        ${SECTIONS.map((s) => html`
          <div key=${s.id} className=${"pitem setting-item" + (s.id === cur ? " active" : "")}
               onClick=${() => setCur(s.id)}>
            <span className="setting-name">${s.title}</span>
            <span className="setting-blurb">${s.blurb}</span>
          </div>`)}
      </div>
    </div>
    <main>
      ${Panel ? html`<${Panel} />` : null}
    </main>
  </>`;
}
