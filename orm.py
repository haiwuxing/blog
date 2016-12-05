from app import app;
from flask import g;
import sqlite3; 

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE']);
    rv.row_factory = sqlite3.Row;
    return rv;

def get_db():
    """Opens a new database connection if there is none ye for the
    current application content.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db();
    return g.sqlite_db;

@app.teardown_appcontext
def close_db(error):
    """Closes the databse again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close();