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
    <main>
      <h1>Settings</h1>

      <section className="settings-block">
        <h2>Python interpreter</h2>
        <p className="muted">
          PySpark autocomplete reads libraries and types from this interpreter's
          environment. Pick the one where <code>pyspark</code> is installed.
        </p>
        <p className="cur-interp">current: <code>${current}</code></p>

        <div className="env-list">
          ${envs.map((e) => html`
            <label key=${e.path} className=${"env-row" + (e.current ? " active" : "")}>
              <input type="radio" name="interp" checked=${e.current}
                     onChange=${() => choose(e.path)} />
              <span className="env-label">${e.label}</span>
              <span className="env-path muted">${e.path}</span>
            </label>`)}
        </div>

        <div className="manual-interp">
          <input className="path-input" placeholder="/path/to/python"
                 value=${manual} onInput=${(ev) => setManual(ev.target.value)} />
          <button className="primary" disabled=${!manual.trim()}
                  onClick=${() => choose(manual.trim())}>Use this path</button>
        </div>
        ${msg ? html`<p className="muted">${msg}</p>` : null}
      </section>
    </main>`;
}
