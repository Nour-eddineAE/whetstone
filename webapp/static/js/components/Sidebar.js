import { html } from "../lib.js";
import { SECTIONS, ICONS } from "../config.js";

// Slim icon rail of top-level sections. Data-driven from SECTIONS.
export function Sidebar({ active, onSelect }) {
  const item = (s) => html`
    <div key=${s.id} className=${"item" + (active === s.id ? " active" : "")}
         onClick=${() => onSelect(s.id)} title=${s.label}>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
           strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d=${ICONS[s.icon]} />
      </svg>
      <span>${s.label}</span>
    </div>`;
  // `bottom: true` sections (e.g. Settings) are pinned to the foot of the rail.
  return html`
    <nav className="rail">
      <div className="logo" title="Whetstone">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2"
             strokeLinecap="round" strokeLinejoin="round">
          <polyline points="3,4 7,15 12,7 17,15 21,4"/>
          <line x1="3" y1="20" x2="21" y2="20"/>
        </svg>
      </div>
      ${SECTIONS.filter((s) => !s.bottom).map(item)}
      <div className="rail-spacer"></div>
      ${SECTIONS.filter((s) => s.bottom).map(item)}
    </nav>`;
}
