"""Build seed data + scaffold answer stubs.  manage.py seed"""
from pengine.seed import main as _build


def main(args=None):
    _build()


if __name__ == "__main__":
    main()
