// Small shared helpers.
import { CATEGORY_LABELS } from "./config.js";

export const catLabel = (c) =>
  CATEGORY_LABELS[c] || c.charAt(0).toUpperCase() + c.slice(1);

function esc(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

// Tiny, safe markdown for problem prompts: escape first, then **bold**, `code`,
// "- " bullets, blank-line paragraphs. Used via dangerouslySetInnerHTML.
export function promptHtml(md) {
  const inline = (s) =>
    esc(s).replace(/`([^`]+)`/g, "<code>$1</code>")
          .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  const lines = (md || "").split("\n");
  let out = "", inList = false;
  const close = () => { if (inList) { out += "</ul>"; inList = false; } };
  for (const ln of lines) {
    if (/^\s*-\s+/.test(ln)) {
      if (!inList) { out += "<ul>"; inList = true; }
      out += "<li>" + inline(ln.replace(/^\s*-\s+/, "")) + "</li>";
    } else if (ln.trim() === "") { close(); }
    else { close(); out += "<p>" + inline(ln) + "</p>"; }
  }
  close();
  return out;
}

// Group problems by category, ordered by where the category first appears
// (so p01.. order is preserved), each group sorted by id.
export function groupByCategory(problems) {
  const order = [], byCat = {};
  for (const p of problems) {
    if (!byCat[p.category]) { byCat[p.category] = []; order.push(p.category); }
    byCat[p.category].push(p);
  }
  return order.map((c) => ({ category: c, items: byCat[c].sort((a, b) => a.id.localeCompare(b.id)) }));
}

// first problem on this track not yet PASSed (falls back to the first)
export function firstUnfinished(problems, status, track) {
  const onTrack = problems.filter((p) => p.tracks.includes(track));
  const next = onTrack.find((p) => status[p.id + ":" + track] !== "PASS");
  return (next || onTrack[0] || {}).id;
}
