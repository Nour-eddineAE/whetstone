import { html } from "../lib.js";
import { LANGUAGES } from "../config.js";

// Segmented control. Adding a language = one entry in LANGUAGES.
export function LanguagePicker({ value, onChange }) {
  return html`
    <div className="seg">
      ${LANGUAGES.map((l) => html`
        <button key=${l.id} className=${value === l.id ? "active" : ""}
                onClick=${() => onChange(l.id)}>${l.label}</button>`)}
    </div>`;
}
