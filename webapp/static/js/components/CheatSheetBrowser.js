import { html, useState, useEffect, useRef } from "../lib.js";
import * as api from "../api.js";

// Sheet list (pane) + rendered HTML (main). Code blocks highlighted by
// highlight.js after each render; degrades to plain text if it didn't load.
export function CheatSheetBrowser() {
  const [sheets, setSheets] = useState([]);
  const [cur, setCur] = useState(null);
  const [sheet, setSheet] = useState(null);
  const ref = useRef();

  useEffect(() => {
    api.getCheatsheets().then((d) => {
      setSheets(d.sheets);
      if (d.sheets[0]) setCur(d.sheets[0].slug);
    });
  }, []);
  useEffect(() => { if (cur) { setSheet(null); api.getCheatsheet(cur).then(setSheet); } }, [cur]);
  useEffect(() => {
    if (sheet && ref.current && window.hljs)
      ref.current.querySelectorAll("pre code").forEach((b) => window.hljs.highlightElement(b));
  }, [sheet]);

  return html`<>
    <div className="pane">
      <div className="pane-head"><h2 className="pane-title">Cheat Sheets</h2></div>
      <div className="pane-list">
        ${sheets.map((s) => html`
          <div key=${s.slug} className=${"pitem" + (s.slug === cur ? " active" : "")}
               onClick=${() => setCur(s.slug)}>${s.title}</div>`)}
      </div>
    </div>
    <main>
      ${sheet
        ? html`<div className="sheet" ref=${ref} dangerouslySetInnerHTML=${{ __html: sheet.html }}></div>`
        : html`<div className="center">Loading…</div>`}
    </main>
  </>`;
}
