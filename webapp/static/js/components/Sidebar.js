import { html } from "../lib.js";
import { SECTIONS, ICONS } from "../config.js";

// Slim icon rail of top-level sections. Data-driven from SECTIONS.
export function Sidebar({ active, onSelect }) {
  return html`
    <nav className="rail">
      <div className="logo" title="SQL + PySpark Practice">ΣQ</div>
      ${SECTIONS.map((s) => html`
        <div key=${s.id} className=${"item" + (active === s.id ? " active" : "")}
             onClick=${() => onSelect(s.id)} title=${s.label}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
               strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d=${ICONS[s.icon]} />
          </svg>
          <span>${s.label}</span>
        </div>`)}
    </nav>`;
}
