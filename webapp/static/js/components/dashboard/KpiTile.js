import { html } from "../../lib.js";

function DonutChart({ percent, size = 52, color = "#4c8dff" }) {
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
    </svg>`;
}

// Props:
//   value        – string or number displayed large
//   label        – short descriptor shown below the value
//   percent      – 0–100; when provided renders a mini donut ring
//   color        – hex string used for the donut fill (default: accent blue)
export function KpiTile({ value, label, percent = null, color = "#4c8dff" }) {
  return html`
    <div className="kpi-tile">
      <div style=${{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "12px" }}>
        <div>
          <div className="kpi-value">${value}</div>
          <div className="kpi-label">${label}</div>
        </div>
        ${percent !== null ? html`<${DonutChart} percent=${percent} color=${color} />` : null}
      </div>
    </div>`;
}
