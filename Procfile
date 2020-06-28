web: gunicorn -w 1 --chdir tests test1:app --preload
worker: python tests/server_db.py
