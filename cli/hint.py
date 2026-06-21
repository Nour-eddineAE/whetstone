"""One-line hint for a problem.  manage.py hint p03 [sql|pyspark]"""
import sys

from pengine import content, meta


def main(args=None):
    args = list(sys.argv[1:] if args is None else args)
    if not args:
        print("usage: manage.py hint <pid> [track]   e.g. manage.py hint p03 pyspark")
        return
    pid = args[0]
    track = args[1] if len(args) > 1 else None
    m = meta.get(pid)
    print(f"\n{pid} [{m['category']}/{m['difficulty']}]  hint:")
    tracks = [track] if track else m["tracks"]
    for t in tracks:
        print(f"  [{t}] {content.get_hint(pid, t)}")
    print()


if __name__ == "__main__":
    main()
