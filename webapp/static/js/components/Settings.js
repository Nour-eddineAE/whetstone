import { html, useState, useEffect } from "../lib.js";
import * as api from "../api.js";

// Pick the Python interpreter used for PySpark autocomplete. Jedi introspects
// that env's installed libraries (pyspark, pandas, types) to power completions.
export function Settings() {
  const [envs, setEnvs] = useState([]);
  const [current, setCurrent] = useState("");
  const [manual, setManual] = useState("");
  const [msg, setMsg] = useState("");

  function load() {
    api.getEnvironments().then((d) => {
      setEnvs(d.environments || []);
      setCurrent(d.current || "");
    });
  }
  useEffect(load, []);

  async function choose(path) {
    setMsg("");
    const r = await api.setInterpreter(path);
    if (r.error) { setMsg(r.error); return; }
    setCurrent(r.interpreter);
    setMsg("interpreter set");
    load();
  }

  return html`
    <main className="settings-page">
      <header className="settings-head">
        <h1>Settings</h1>
        <p className="settings-sub">Configure how Whetstone runs and completes your code.</p>
      </header>

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
      </section>
    </main>`;
}
