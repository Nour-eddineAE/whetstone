"""Print the reference solution (with its teaching comments).

  manage.py reveal p03           both tracks
  manage.py reveal p03 sql       SQL only
  manage.py reveal p03 pyspark   PySpark only
"""
import sys

from pengine import content, meta


def main(args=None):
    args = list(sys.argv[1:] if args is None else args)
    if not args:
        print("usage: manage.py reveal <pid> [sql|pyspark]")
        return
    pid = args[0]
    want = args[1] if len(args) > 1 else None
    m = meta.get(pid)
    tracks = [want] if want else m["tracks"]
    print(f"\n=== {pid} [{m['category']}/{m['difficulty']}] reference ===")
    for track in tracks:
        print(f"\n--- {track} ---")
        print(content.read_solution(pid, track))


if __name__ == "__main__":
    main()
