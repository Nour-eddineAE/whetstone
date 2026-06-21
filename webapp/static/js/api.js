// All server calls in one place. Endpoints are unchanged from the CLI's grader;
// answers/ files stay the single source of truth.
const j = (r) => r.json();

export const getProblems = () => fetch("/api/problems").then(j);
export const getProblem = (pid, track) => fetch(`/api/problem/${pid}/${track}`).then(j);
export const saveAnswer = (pid, track, text) =>
  fetch(`/api/answer/${pid}/${track}`, post({ text })).then(j);
export const checkAnswer = (pid, track, text) =>
  fetch(`/api/check/${pid}/${track}`, post({ text })).then(j);
export const checkFile = (pid, track) =>
  fetch(`/api/check/${pid}/${track}`, post({})).then(j);   // grade saved file as-is
export const getHint = (pid) => fetch(`/api/hint/${pid}`).then(j);
export const reveal = (pid, track) => fetch(`/api/reveal/${pid}/${track}`).then(j);
export const runScratch = (sql) => fetch("/api/run/sql", post({ sql })).then(j);
export const getCheatsheets = () => fetch("/api/cheatsheets").then(j);
export const getCheatsheet = (slug) => fetch(`/api/cheatsheet/${slug}`).then(j);
export const getEnvironments = () => fetch("/api/environments").then(j);
export const setInterpreter = (path) => fetch("/api/settings/interpreter", post({ path })).then(j);
export const completePython = (code, line, ch) =>
  fetch("/api/complete/python", post({ code, line, ch })).then(j);
export const signaturePython = (code, line, ch) =>
  fetch("/api/signature/python", post({ code, line, ch })).then(j);
export const hoverPython = (code, line, ch) =>
  fetch("/api/hover/python", post({ code, line, ch })).then(j);

function post(body) {
  return { method: "POST", headers: { "Content-Type": "application/json" },
           body: JSON.stringify(body || {}) };
}
