"""Launch the local web UI.  manage.py web  ->  http://localhost:9000

Port/host come from pengine.config (override with env PRACTICE_PORT / PRACTICE_HOST).
One warm SparkSession is kept in this process (in pengine.grader) and reused for
every PySpark check.
"""
import os
import signal
import socket
import subprocess
import time

from pengine import config
from webapp import create_app


def _kill_stale_owner(port: int) -> None:
    """SIGTERM any manage.py instance already holding `port`."""
    with socket.socket() as s:
        if s.connect_ex(("127.0.0.1", port)) != 0:
            return
    try:
        pids = subprocess.check_output(
            ["lsof", "-ti", f":{port}"], stderr=subprocess.DEVNULL
        ).decode().split()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return
    for pid_str in pids:
        try:
            cmdline = subprocess.check_output(
                ["ps", "-p", pid_str, "-o", "command="], stderr=subprocess.DEVNULL
            ).decode()
        except subprocess.CalledProcessError:
            continue
        if "manage.py" in cmdline:
            os.kill(int(pid_str), signal.SIGTERM)
            print(f"killed stale instance (pid {pid_str}) on :{port}")
            time.sleep(0.6)


def main(args=None):
    app = create_app()
    host, port = config.WEB_HOST, config.WEB_PORT
    _kill_stale_owner(port)
    print(f"Practice UI -> http://localhost:{port}  (Ctrl-C to stop)")
    # threaded=False: serialize requests so the single SparkSession isn't hit
    # concurrently. use_reloader=False: don't spawn a second warm Spark process.
    app.run(host=host, port=port, debug=False, threaded=False, use_reloader=False)


if __name__ == "__main__":
    main()
