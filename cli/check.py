"""CLI grader - presentation over pengine.grader.grade_result().

  manage.py check sql p03        grade answers/sql/p03.sql
  manage.py check pyspark p03    grade answers/pyspark/p03.py
  manage.py check all            scoreboard of everything attempted
  manage.py check all sql        scoreboard, SQL track only
  manage.py check all pyspark    scoreboard, PySpark track only

Add --ref to grade the REFERENCE solutions (self-test: everything should PASS).
"""
import sys

from pengine import meta
from pengine.grader import grade_result

G, R, Y, DIM, X = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


def _print_diff(res):
    print(f"  {DIM}expected {res['expected_count']} row(s), "
          f"got {res['actual_count']} row(s){X}")
    d = res["diff"]
    if d["col_count_mismatch"]:
        ce, ca = d["col_count_mismatch"]
        print(f"  {R}column count differs: expected {ce}, got {ca}{X}")
    if res["ordered"]:
        fd = d["first_diff"]
        if fd:
            print(f"  {R}first diff at row {fd['index']}{X}")
            print(f"    expected: {fd['expected']}")
            print(f"    actual:   {fd['actual']}")
        return
    if d["only_expected"]:
        print(f"  {Y}in EXPECTED but missing from yours:{X}")
        for r in d["only_expected"]:
            print(f"    {tuple(r)}")
    if d["only_actual"]:
        print(f"  {Y}in YOURS but not expected:{X}")
        for r in d["only_actual"]:
            print(f"    {tuple(r)}")


def grade(track, pid, ref=False, verbose=True):
    """Grade and (optionally) print. Returns 'PASS'|'FAIL'|'SKIP'."""
    res = grade_result(track, pid, ref=ref)
    if not verbose:
        return res["status"]
    st, tag = res["status"], f"{DIM}({res['category']}/{res['difficulty']}){X}"
    if st == "SKIP":
        print(f"{Y}-  {pid} {track}: skipped ({res['error']}){X}")
    elif st == "PASS":
        print(f"{G}OK {pid} {track}: PASS{X}  {tag}")
    elif res["error"]:
        print(f"{R}x  {pid} {track}: ERROR {res['error']}{X}")
    else:
        print(f"{R}x  {pid} {track}: FAIL{X}  {tag}")
        _print_diff(res)
    return st


def scoreboard(ref=False, only=None):
    rows, passed, total = [], 0, 0
    for m in meta.all_meta():
        for track in m["tracks"]:
            if only and track != only:
                continue
            st = grade(track, m["id"], ref=ref, verbose=False)
            if st == "SKIP":
                continue
            total += 1
            passed += st == "PASS"
            rows.append((m["id"], track, m["category"], st))

    print(f"\n  {'ID':<5} {'TRACK':<8} {'CATEGORY':<12} RESULT")
    print(f"  {'-'*5} {'-'*8} {'-'*12} {'-'*6}")
    for pid, track, cat, st in rows:
        c = G if st == "PASS" else R
        print(f"  {pid:<5} {track:<8} {cat:<12} {c}{'OK' if st == 'PASS' else 'x '} {st}{X}")
    if not rows:
        print(f"  {Y}nothing attempted yet -- solve a problem then re-run{X}")
    else:
        c = G if passed == total else Y
        print(f"\n  {c}{passed}/{total} passed{X}")


def main(args=None):
    args = list(sys.argv[1:] if args is None else args)
    ref = "--ref" in args
    args = [a for a in args if a != "--ref"]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "all":
        scoreboard(ref=ref, only=args[1] if len(args) > 1 else None)
    elif cmd in ("sql", "pyspark"):
        if len(args) < 2:
            print("usage: manage.py check {sql|pyspark} <pid>")
            return
        grade(cmd, args[1], ref=ref)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
