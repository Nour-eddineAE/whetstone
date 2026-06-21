"""pengine - the practice engine.

Pure, UI-agnostic core shared by the CLI entrypoints and the web app:

  config   paths + constants (one place to resolve the project layout)
  meta     problem frontmatter parser
  content  answer / solution / hint file access
  grader   the grader (grade_result is the single source of truth)
  seed     deterministic data generation + answer-stub scaffolding
"""
