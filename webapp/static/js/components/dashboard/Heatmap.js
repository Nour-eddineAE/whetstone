import { html, useMemo } from "../../lib.js";

const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const DAY_LABELS = ["M","","W","","F","",""];

function localISO(d) {
  return d.getFullYear() + "-" +
    String(d.getMonth() + 1).padStart(2, "0") + "-" +
    String(d.getDate()).padStart(2, "0");
}

function cellColor(count, max) {
  if (!count) return "rgba(255,255,255,0.04)";
  const t = Math.min(count / Math.max(max, 1), 1);
  if (t < 0.25) return "#1a3a2a";
  if (t < 0.5)  return "#2d6a3f";
  if (t < 0.75) return "#3fb950";
  return "#a3f0b8";
}

// Props:
//   data    – { "YYYY-MM-DD": number } activity counts keyed by local ISO date
//   months  – number of months to display, 3–6 (default: 4)
export function Heatmap({ data = {}, months = 4 }) {
  const { weeks, monthLabels } = useMemo(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const start = new Date(today);
    start.setDate(start.getDate() - months * 31);
    // Snap back to nearest Monday (getDay: 0=Sun,1=Mon,...,6=Sat)
    const dow = start.getDay();
    start.setDate(start.getDate() - ((dow + 6) % 7));

    const weeks = [];
    const monthLabels = {};
    const cur = new Date(start);
    let lastMonth = -1;

    while (cur <= today) {
      const wi = weeks.length;
      const mo = cur.getMonth();
      if (mo !== lastMonth) {
        monthLabels[wi] = MONTHS[mo];
        lastMonth = mo;
      }
      const week = [];
      for (let d = 0; d < 7; d++) {
        const isFuture = cur > today;
        week.push({ date: localISO(cur), count: isFuture ? null : (data[localISO(cur)] || 0) });
        cur.setDate(cur.getDate() + 1);
      }
      weeks.push(week);
    }
    return { weeks, monthLabels };
  }, [data, months]);

  const max = useMemo(() => {
    const vals = Object.values(data);
    return vals.length ? Math.max(...vals) : 1;
  }, [data]);

  return html`
    <div className="heatmap">
      <!-- month labels aligned to week columns -->
      <div style=${{ display:"flex", gap:"2px", marginBottom:"5px", paddingLeft:"22px" }}>
        ${weeks.map((_, wi) => html`
          <div key=${wi} style=${{
            width:"10px", fontSize:"9px", color:"var(--muted)",
            overflow:"visible", whiteSpace:"nowrap", lineHeight:"12px"
          }}>
            ${monthLabels[wi] || ""}
          </div>`)}
      </div>
      <div style=${{ display:"flex", gap:"6px" }}>
        <!-- day-of-week labels: alternate M/W/F to save space -->
        <div style=${{ display:"flex", flexDirection:"column", gap:"2px", width:"16px" }}>
          ${DAY_LABELS.map((d, i) => html`
            <div key=${i} style=${{
              fontSize:"9px", color:"var(--muted)", height:"10px",
              lineHeight:"10px", textAlign:"right"
            }}>
              ${d}
            </div>`)}
        </div>
        <!-- week columns -->
        <div style=${{ display:"flex", gap:"2px" }}>
          ${weeks.map((week, wi) => html`
            <div key=${wi} style=${{ display:"flex", flexDirection:"column", gap:"2px" }}>
              ${week.map(({ date, count }) => html`
                <div key=${date}
                  title=${count !== null ? date + ": " + count + " solved" : ""}
                  style=${{
                    width:"10px", height:"10px", borderRadius:"2px",
                    background: count !== null ? cellColor(count, max) : "rgba(255,255,255,0.02)"
                  }} />`)}
            </div>`)}
        </div>
      </div>
    </div>`;
}
