import { html } from "../../lib.js";

function RingChart({ percent, size = 52, color = "#4c8dff" }) {
  const r = (size - 8) / 2;
  const circ = 2 * Math.PI * r;
  const fill = (Math.min(percent, 100) / 100) * circ;
  const mid = size / 2;
  return html`
    <svg width=${size} height=${size} viewBox=${"0 0 " + size + " " + size} style=${{ flexShrink: 0 }}>
      <circle cx=${mid} cy=${mid} r=${r}
        fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="4" />
      <circle cx=${mid} cy=${mid} r=${r}
        fill="none" stroke=${color} strokeWidth="4"
        strokeDasharray=${fill + " " + circ}
        strokeLinecap="round"
        transform=${"rotate(-90 " + mid + " " + mid + ")"} />
      <text x=${mid} y=${mid} textAnchor="middle" dominantBaseline="central"
        fill="var(--text)" fontSize="10" fontWeight="600">${percent}%</text>
    </svg>`;
}

// Props:
//   label    – category name
//   percent  – 0–100 completion
//   color    – hex string for fill color (default: accent blue)
//   variant  – "bar" (default) | "ring"
export function CategoryProgress({ label, percent, color = "#4c8dff", variant = "bar" }) {
  if (variant === "ring") {
    return html`
      <div className="cat-ring">
        <${RingChart} percent=${percent} color=${color} />
        <span className="cat-label">${label}</span>
      </div>`;
  }

  return html`
    <div className="cat-card">
      <div className="cat-bar-wrap">
        <div className="cat-bar" style=${{ "--cat-color": color, width: percent + "%" }} />
      </div>
      <div className="cat-footer">
        <span className="cat-label">${label}</span>
        <span className="cat-pct">${percent}%</span>
      </div>
    </div>`;
}
