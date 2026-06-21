import { html } from "../lib.js";

// outlined rounded checkbox; green check on PASS, red box on FAIL, gray otherwise
export function StatusIcon({ status }) {
  const cls = "chk " + (status || "untried");
  return html`
    <svg className=${cls} viewBox="0 0 24 24" width="16" height="16" fill="none">
      <rect className="box" x="3" y="3" width="18" height="18" rx="6" strokeWidth="2" />
      <path className="tick" d="M7.5 12.5l3 3 6-6.5" strokeWidth="2.4"
            strokeLinecap="round" strokeLinejoin="round" />
    </svg>`;
}
