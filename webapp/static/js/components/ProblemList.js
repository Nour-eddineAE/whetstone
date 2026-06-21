import { html } from "../lib.js";
import { groupByCategory, catLabel } from "../util.js";
import { StatusIcon } from "./StatusIcon.js";

// Problems for the active language, grouped by category, with status + difficulty.
export function ProblemList({ problems, status, track, currentPid, onSelect }) {
  const onTrack = problems.filter((p) => p.tracks.includes(track));
  const groups = groupByCategory(onTrack);
  return html`
    <div className="pane-list">
      ${groups.map((g) => html`
        <div key=${g.category}>
          <div className="cat">${catLabel(g.category)}</div>
          ${g.items.map((p) => html`
            <div key=${p.id}
                 className=${"pitem" + (p.id === currentPid ? " active" : "")}
                 onClick=${() => onSelect(p.id)}>
              <${StatusIcon} status=${status[p.id + ":" + track]} />
              <span className="pid">${p.id}</span>
              <span className=${"badge " + p.difficulty}>${p.difficulty}</span>
            </div>`)}
        </div>`)}
    </div>`;
}
