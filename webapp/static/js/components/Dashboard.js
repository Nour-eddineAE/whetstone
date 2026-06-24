import { html, useState, useEffect, useMemo } from "../lib.js";
import * as api from "../api.js";
import { KpiTile } from "./dashboard/KpiTile.js";
import { CategoryProgress } from "./dashboard/CategoryProgress.js";
import { Heatmap } from "./dashboard/Heatmap.js";
import { SheetCard } from "./dashboard/SheetCard.js";

const SUBJECT_COLORS = {
  SQL:       "#4c8dff",
  PySpark:   "#f97316",
  Java:      "#a78bfa",
  Spring:    "#34d399",
  Patterns:  "#fbbf24",
  Interview: "#fb923c",
};

const CAT_COLORS = ["#4c8dff", "#f97316", "#fbbf24", "#fb923c", "#34d399", "#a78bfa"];

function fmtMinutes(m) {
  if (!m) return "0m";
  return m < 60 ? m + "m" : Math.floor(m / 60) + "h " + (m % 60) + "m";
}

function timeAgo(ts) {
  const secs = Math.floor(Date.now() / 1000) - ts;
  if (secs < 3600) return Math.floor(secs / 60) + "m ago";
  if (secs < 86400) return Math.floor(secs / 3600) + "h ago";
  const d = Math.floor(secs / 86400);
  return d === 1 ? "Yesterday" : d + " days ago";
}

export function Dashboard({ onOpenSheet }) {
  const [dash, setDash] = useState(null);

  useEffect(() => {
    api.getDashboard().then(setDash).catch(() => {});
  }, []);

  const heatmapData = useMemo(() => {
    if (!dash?.activity) return {};
    const out = {};
    for (const { date, count } of dash.activity) if (count) out[date] = count;
    return out;
  }, [dash]);

  const kpis       = dash?.kpis       ?? null;
  const categories = dash?.categories ?? [];
  const recent     = dash?.recent     ?? [];

  const solvedPct = kpis
    ? Math.round(100 * kpis.solved.total / Math.max(kpis.solved.possible, 1))
    : null;

  const sheetsPct = kpis
    ? Math.round(100 * kpis.sheetsReviewed.count / Math.max(kpis.sheetsReviewed.total, 1))
    : null;

  return html`
    <div className="dashboard">

      <div className="dash-header">
        <div className="dash-identity">
          <div className="dash-avatar">N</div>
          <span className="dash-name">Nour-eddine</span>
          <span className="dash-badge">
            ${kpis && kpis.streak > 0 ? kpis.streak + "d streak" : "Lv 1"}
          </span>
        </div>
      </div>

      <div className="dash-kpis">
        <${KpiTile}
          label="Sheets reviewed"
          value=${kpis ? kpis.sheetsReviewed.count + "/" + kpis.sheetsReviewed.total : "—"}
          percent=${sheetsPct}
        />
        <${KpiTile}
          label="Problems solved"
          value=${kpis ? kpis.solved.total + "/" + kpis.solved.possible : "—"}
          percent=${solvedPct}
          color="#4c8dff"
        />
        <${KpiTile}
          label="Current streak"
          value=${kpis ? kpis.streak + "d" : "—"}
        />
        <${KpiTile}
          label="Score"
          value=${kpis ? kpis.score + "%" : "—"}
          percent=${kpis?.score ?? null}
          color="#3fb950"
        />
        <${KpiTile}
          label="Time this week"
          value=${kpis ? fmtMinutes(kpis.weekMinutes) : "—"}
        />
      </div>

      ${categories.length > 0 ? html`
        <section className="dash-section">
          <h2 className="dash-section-title">Category Progress</h2>
          <div className="dash-cats">
            ${categories.map((c, i) => html`
              <${CategoryProgress}
                key=${c.id}
                label=${c.label}
                percent=${c.total ? Math.round(100 * c.solved / c.total) : 0}
                color=${CAT_COLORS[i % CAT_COLORS.length]}
              />`)}
          </div>
        </section>` : null}

      <section className="dash-section">
        <h2 className="dash-section-title">Activity</h2>
        <${Heatmap} data=${heatmapData} months=${4} />
      </section>

      ${recent.length > 0 ? html`
        <section className="dash-section">
          <h2 className="dash-section-title">Continue where you left off</h2>
          <div className="dash-recent-row">
            ${recent.map((r) => html`
              <${SheetCard}
                key=${r.slug}
                title=${r.title}
                category=${r.subject}
                categoryColor=${SUBJECT_COLORS[r.subject] || "#5a6675"}
                lastReviewed=${timeAgo(r.ts)}
                onClick=${() => onOpenSheet(r.slug)}
              />`)}
          </div>
        </section>` : null}

    </div>`;
}
