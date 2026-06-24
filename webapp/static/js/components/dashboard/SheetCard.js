import { html } from "../../lib.js";

function CardIcon({ icon }) {
  if (icon == null) return null;
  return html`
    <div className="sheet-card-icon">
      ${typeof icon === "string"
        ? html`
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                 style=${{ width:"16px", height:"16px" }}>
              <path d=${icon} />
            </svg>`
        : icon}
    </div>`;
}

function CategoryBadge({ label, color }) {
  return html`
    <span className="sheet-card-badge" style=${{
      background: color + "1a",
      color,
      borderColor: color + "40",
    }}>
      ${label}
    </span>`;
}

// Props:
//   icon          – SVG path `d` string, or a React element; omit for no icon
//   title         – sheet/topic name
//   category      – short category label
//   categoryColor – hex color for the category badge (default: accent blue)
//   lastReviewed  – display string, e.g. "2 days ago"
//   readTime      – display string, e.g. "8 min"
//   onClick       – optional click handler
export function SheetCard({ icon, title, category, categoryColor = "#4c8dff", lastReviewed, readTime, onClick }) {
  return html`
    <div className="sheet-card" onClick=${onClick || null}>
      <div className="sheet-card-body">
        <${CardIcon} icon=${icon} />
        <div className="sheet-card-info">
          <div className="sheet-card-title">${title}</div>
          <div>
            <${CategoryBadge} label=${category} color=${categoryColor} />
          </div>
          <div className="sheet-card-meta">
            ${lastReviewed ? html`<span>${lastReviewed}</span>` : null}
            ${readTime ? html`<span>${readTime}</span>` : null}
          </div>
        </div>
      </div>
    </div>`;
}

// SheetCard variant with a progress bar and optional next-problem label.
// Props extend SheetCard with:
//   progress    – 0–100 completion percentage
//   nextProblem – display string for the next item in the series
export function ContinueCard({ icon, title, category, categoryColor = "#4c8dff", lastReviewed, readTime, onClick, progress = 0, nextProblem }) {
  return html`
    <div className="sheet-card" onClick=${onClick || null}>
      <div className="sheet-card-body">
        <${CardIcon} icon=${icon} />
        <div className="sheet-card-info">
          <div style=${{ display:"flex", justifyContent:"space-between", alignItems:"baseline", gap:"8px" }}>
            <div className="sheet-card-title">${title}</div>
            <span style=${{ fontSize:"11px", color:"var(--muted)", flexShrink:0 }}>${progress}%</span>
          </div>
          <div className="sheet-card-progress">
            <div className="sheet-card-progress-fill"
                 style=${{ width: progress + "%", background: categoryColor }} />
          </div>
          <div style=${{ display:"flex", alignItems:"center", gap:"8px", flexWrap:"wrap" }}>
            <${CategoryBadge} label=${category} color=${categoryColor} />
            ${nextProblem ? html`<span style=${{ fontSize:"11px", color:"var(--muted)" }}>Next: ${nextProblem}</span>` : null}
          </div>
          <div className="sheet-card-meta">
            ${lastReviewed ? html`<span>${lastReviewed}</span>` : null}
            ${readTime ? html`<span>${readTime}</span>` : null}
          </div>
        </div>
      </div>
    </div>`;
}
