import { html, useState, useEffect, ReactDOMClient } from "./lib.js";
import { LANGUAGES } from "./config.js";
import { firstUnfinished } from "./util.js";
import * as api from "./api.js";
import { Sidebar } from "./components/Sidebar.js";
import { LanguagePicker } from "./components/LanguagePicker.js";
import { ProblemList } from "./components/ProblemList.js";
import { ProblemView } from "./components/ProblemView.js";
import { CheatSheetBrowser } from "./components/CheatSheetBrowser.js";
import { Scoreboard } from "./components/Scoreboard.js";

function ProblemsSection({ problems, status, track, pid, onPick, onTrack, onStatus }) {
  return html`<>
    <div className="pane">
      <div className="pane-head">
        <h2 className="pane-title">Problems</h2>
        <${LanguagePicker} value=${track} onChange=${onTrack} />
      </div>
      <${ProblemList} problems=${problems} status=${status} track=${track}
                      currentPid=${pid} onSelect=${onPick} />
    </div>
    <main>
      ${pid ? html`<${ProblemView} pid=${pid} track=${track} onStatus=${onStatus} />`
            : html`<div className="center">Pick a problem</div>`}
    </main>
  </>`;
}

function App() {
  const [section, setSection] = useState("problems");
  const [problems, setProblems] = useState([]);
  const [status, setStatus] = useState({});
  const [track, setTrack] = useState(LANGUAGES[0].id);
  const [pid, setPid] = useState(null);

  useEffect(() => {
    api.getProblems().then((d) => {
      setProblems(d.problems);
      setStatus(d.status || {});
      setPid(firstUnfinished(d.problems, d.status || {}, LANGUAGES[0].id));
    });
  }, []);

  const setStatusFor = (p, t, st) => setStatus((s) => ({ ...s, [p + ":" + t]: st }));
  const changeTrack = (t) => { setTrack(t); setPid(firstUnfinished(problems, status, t)); };

  let content;
  if (section === "problems")
    content = html`<${ProblemsSection} problems=${problems} status=${status} track=${track}
        pid=${pid} onPick=${setPid} onTrack=${changeTrack} onStatus=${setStatusFor} />`;
  else if (section === "cheatsheets")
    content = html`<${CheatSheetBrowser} />`;
  else
    content = html`<${Scoreboard} problems=${problems} status=${status} onStatus=${setStatusFor} />`;

  return html`<div className="app"><${Sidebar} active=${section} onSelect=${setSection} />${content}</div>`;
}

ReactDOMClient.createRoot(document.getElementById("root")).render(html`<${App} />`);
