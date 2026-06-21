import { html } from "../lib.js";
import { Table } from "./Table.js";

// Collapsible preview of the seed tables a problem touches.
export function SampleData({ tables, samples }) {
  if (!samples) return null;
  const present = (tables || []).filter((t) => samples[t]);
  if (!present.length) return null;
  return html`
    <details className="samples" open>
      <summary>Sample data (${present.length} table${present.length > 1 ? "s" : ""})</summary>
      ${present.map((t) => {
        const s = samples[t];
        return html`
          <div className="sample" key=${t}>
            <div className="sample-cap"><b>${t}</b>
              <span>showing ${s.rows.length} of ${s.total} rows</span></div>
            <div className="scroll"><${Table} cols=${s.columns} rows=${s.rows} /></div>
          </div>`;
      })}
    </details>`;
}
