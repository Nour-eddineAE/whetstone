#!/usr/bin/env python
"""Project command hub. One entrypoint, lazy imports (so `seed` won't load Flask
or PySpark, etc.).

  python manage.py seed                      build data + scaffold answer stubs
  python manage.py check sql p03             grade one answer
  python manage.py check pyspark p03
  python manage.py check all [sql|pyspark] [--ref]
  python manage.py hint p03                  one-line hint
  python manage.py reveal p03 [sql|pyspark]  reference solution
  python manage.py web                        launch the browser UI (localhost:5000)
"""
import sys

COMMANDS = {
    "seed": "cli.seed",
    "check": "cli.check",
    "hint": "cli.hint",
    "reveal": "cli.reveal",
    "web": "cli.web", "ui": "cli.web", "serve": "cli.web",
}


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]
    mod_name = COMMANDS.get(cmd)
    if not mod_name:
        print(f"unknown command: {cmd}\n")
        print(__doc__)
        return
    import importlib
    importlib.import_module(mod_name).main(rest)


if __name__ == "__main__":
    main()
