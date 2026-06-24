import { html } from "../lib.js";
import { LANGUAGES } from "../config.js";

// Groups tracks by subject. Single-subject = flat pills; multi-subject = labeled groups.
export function LanguagePicker({ value, onChange }) {
  const groupMap = new Map();
  for (const l of LANGUAGES) {
    const s = l.subject || "";
    if (!groupMap.has(s)) groupMap.set(s, []);
    groupMap.get(s).push(l);
  }
  const groups = [...groupMap.entries()];
  const multiSubject = groups.length > 1;

  return html`
    <div className="track-picker">
      ${groups.map(([subject, langs]) => html`
        <div key=${subject} className="track-group">
          ${multiSubject && subject
            ? html`<span className="track-subject-label">${subject}</span>`
            : null}
          ${langs.map((l) => html`
            <button key=${l.id}
              className=${"track-pill" + (value === l.id ? " active" : "")}
              style=${{ "--tp-color": l.color || "var(--accent)" }}
              onClick=${() => onChange(l.id)}>
              ${l.label}
            </button>`)}
        </div>`)}
    </div>`;
}
