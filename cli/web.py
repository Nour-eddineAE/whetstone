"""Launch the local web UI.  manage.py web  ->  http://localhost:9000

Port/host come from pengine.config (override with env PRACTICE_PORT / PRACTICE_HOST).
One warm SparkSession is kept in this process (in pengine.grader) and reused for
every PySpark check.
"""
from pengine import config
from webapp import create_app


def main(args=None):
    app = create_app()
    host, port = config.WEB_HOST, config.WEB_PORT
    print(f"Practice UI -> http://localhost:{port}  (Ctrl-C to stop)")
    # threaded=False: serialize requests so the single SparkSession isn't hit
    # concurrently. use_reloader=False: don't spawn a second warm Spark process.
    app.run(host=host, port=port, debug=False, threaded=False, use_reloader=False)


if __name__ == "__main__":
    main()
