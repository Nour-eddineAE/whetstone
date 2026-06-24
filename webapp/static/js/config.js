// Data-driven app config. Adding a section or a language is one entry here
// (plus, for a section, a component case in main.js).

export const SECTIONS = [
  { id: "problems",    label: "Problems", icon: "list" },
  { id: "cheatsheets", label: "Cheats",   icon: "book" },
  { id: "scoreboard",  label: "Score",    icon: "chart" },
  { id: "progress",    label: "Progress", icon: "pulse" },
  { id: "settings",    label: "Settings", icon: "gear", bottom: true },
];

// To add a track: one entry here. `subject` groups tracks in the picker.
// `color` drives the active pill color. `mode` is the CodeMirror mode.
// Example: { id: "spring", label: "Spring JPA", mode: "text/x-java", subject: "Backend", color: "#34d399" }
export const LANGUAGES = [
  { id: "sql",     label: "SQL",     mode: "sql",    subject: "Data Engineering", color: "#4c8dff" },
  { id: "pyspark", label: "PySpark", mode: "python", subject: "Data Engineering", color: "#f97316" },
];

// Pretty names for problem categories (unknown ones are title-cased).
export const CATEGORY_LABELS = {
  joins: "Joins", window: "Window functions", patterns: "Patterns",
  sparkops: "Spark ops", aggregation: "Aggregation", cte: "CTEs / multi-step",
  dates: "Date functions", subquery: "Subqueries",
};

// Stroke-path icons for the rail.
export const ICONS = {
  list:  "M4 6h16M4 12h16M4 18h16",
  book:  "M5 4h11a2 2 0 012 2v14H7a2 2 0 01-2-2V4zM5 4v14",
  chart: "M4 20V11M10 20V5M16 20v-8M3 20h18",
  pulse: "M22 12h-4l-3 9L9 3l-3 9H2",
  gear:  "M12 9a3 3 0 100 6 3 3 0 000-6zM19.4 15a1.6 1.6 0 00.3 1.8l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.6 1.6 0 00-1.8-.3 1.6 1.6 0 00-1 1.5V21a2 2 0 11-4 0v-.1a1.6 1.6 0 00-1-1.5 1.6 1.6 0 00-1.8.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.6 1.6 0 00.3-1.8 1.6 1.6 0 00-1.5-1H3a2 2 0 110-4h.1a1.6 1.6 0 001.5-1 1.6 1.6 0 00-.3-1.8l-.1-.1a2 2 0 112.8-2.8l.1.1a1.6 1.6 0 001.8.3H9a1.6 1.6 0 001-1.5V3a2 2 0 114 0v.1a1.6 1.6 0 001 1.5 1.6 1.6 0 001.8-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.6 1.6 0 00-.3 1.8V9a1.6 1.6 0 001.5 1H21a2 2 0 110 4h-.1a1.6 1.6 0 00-1.5 1z",
};
