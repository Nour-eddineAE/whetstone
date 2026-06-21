// Data-driven app config. Adding a section or a language is one entry here
// (plus, for a section, a component case in main.js).

export const SECTIONS = [
  { id: "problems",    label: "Problems", icon: "list" },
  { id: "cheatsheets", label: "Cheats",   icon: "book" },
  { id: "scoreboard",  label: "Score",    icon: "chart" },
];

// To add a language later: one entry. `mode` is the CodeMirror mode.
export const LANGUAGES = [
  { id: "sql",     label: "SQL",     mode: "sql" },
  { id: "pyspark", label: "PySpark", mode: "python" },
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
};
