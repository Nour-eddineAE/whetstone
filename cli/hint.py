"""One-line hint for a problem.  manage.py hint p03"""
import sys

from pengine import content, meta


def main(args=None):
    args = list(sys.argv[1:] if args is None else args)
    if not args:
        print("usage: manage.py hint <pid>   e.g. manage.py hint p03")
        return
    pid = args[0]
    m = meta.get(pid)
    print(f"\n{pid} [{m['category']}/{m['difficulty']}]  hint:")
    print(f"  {content.get_hint(pid)}\n")


if __name__ == "__main__":
    main()
