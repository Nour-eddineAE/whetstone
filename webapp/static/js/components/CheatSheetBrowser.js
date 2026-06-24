import { html, useState, useEffect, useRef } from "../lib.js";
import * as api from "../api.js";
import { SheetCard } from "./dashboard/SheetCard.js";

const SUBJECT_COLORS = {
  SQL:       "#4c8dff",
  PySpark:   "#f97316",
  Java:      "#a78bfa",
  Spring:    "#34d399",
  Patterns:  "#fbbf24",
  Interview: "#fb923c",
};

const COPY_SVG = `<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="9" height="10" rx="1.5"/><path d="M3 3V2a1 1 0 011-1h6a1 1 0 011 1v1M3 3H2a1 1 0 00-1 1v8a1 1 0 001 1h1"/></svg>`;
const CHECK_SVG = `<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8l4 4 8-8"/></svg>`;

function injectCopyButtons(container) {
  container.querySelectorAll("pre").forEach((pre) => {
    if (pre.parentNode.classList.contains("code-wrap")) return;
    const wrap = document.createElement("div");
    wrap.className = "code-wrap";
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    const code = pre.querySelector("code");
    const m = code && code.className.match(/language-(\w+)/);
    if (m) {
      const label = document.createElement("span");
      label.className = "code-lang";
      label.textContent = m[1].toUpperCase();
      wrap.appendChild(label);
    }
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.title = "Copy";
    btn.innerHTML = COPY_SVG;
    btn.addEventListener("click", () => {
      navigator.clipboard.writeText(pre.innerText).then(() => {
        btn.innerHTML = CHECK_SVG;
        btn.classList.add("copied");
        setTimeout(() => { btn.innerHTML = COPY_SVG; btn.classList.remove("copied"); }, 1500);
      }).catch(() => {});
    });
    wrap.appendChild(btn);
  });
}

export function CheatSheetBrowser({ initialSlug = null }) {
  const [sheets, setSheets] = useState([]);
  const [cur, setCur] = useState(initialSlug);
  const [sheet, setSheet] = useState(null);
  const [search, setSearch] = useState("");
  const searchRef = useRef();
  const detailRef = useRef();

  useEffect(() => {
    api.getCheatsheets().then((d) => setSheets(d.sheets));
  }, []);

  useEffect(() => {
    if (cur) { setSheet(null); api.getCheatsheet(cur).then(setSheet); }
  }, [cur]);

  useEffect(() => {
    if (!sheet || !detailRef.current) return;
    if (window.hljs)
      detailRef.current.querySelectorAll("pre code").forEach((b) => window.hljs.highlightElement(b));
    injectCopyButtons(detailRef.current);
  }, [sheet]);

  useEffect(() => {
    const handler = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        searchRef.current?.focus();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  if (cur !== null) {
    const curMeta = sheets.find((s) => s.slug === cur);
    const curColor = curMeta ? (SUBJECT_COLORS[curMeta.subject] || "#5a6675") : "#5a6675";
    return html`
      <main>
        <button className="ghost cs-back" onClick=${() => { setSheet(null); setCur(null); }}>
          ← Back to overview
        </button>
        ${sheet
          ? html`
            <div className="cs-page">
              <div className="cs-page-tag"
                style=${{ background: curColor + "18", color: curColor, borderColor: curColor + "45" }}>
                ${curMeta ? curMeta.subject : ""}
              </div>
              <div className="sheet" ref=${detailRef}
                dangerouslySetInnerHTML=${{ __html: sheet.html }}>
              </div>
            </div>`
          : html`<div className="center">Loading…</div>`}
      </main>`;
  }

  const q = search.toLowerCase();
  const filteredSheets = search.trim()
    ? sheets.filter((s) =>
        s.title.toLowerCase().includes(q) || s.subject.toLowerCase().includes(q))
    : sheets;

  return html`
    <div className="cheats-view">
      <div className="cheats-header">
        <span className="cheats-title">
          Reference Sheets
          <span className="dash-count">${filteredSheets.length}</span>
        </span>
        <input
          ref=${searchRef}
          className="dash-search"
          type="search"
          placeholder="Search sheets… ⌘K"
          value=${search}
          onChange=${(e) => setSearch(e.target.value)}
        />
      </div>
      <div className="dash-sheets-grid">
        ${filteredSheets.map((s) => html`
          <${SheetCard}
            key=${s.slug}
            title=${s.title}
            category=${s.subject}
            categoryColor=${SUBJECT_COLORS[s.subject] || "#5a6675"}
            onClick=${() => setCur(s.slug)}
          />`)}
      </div>
    </div>`;
}
