from flask import Flask, render_template;
from app import app;

@app.route('/')
def hello():
    """Renders a sample page."""
    return render_template('index.html');