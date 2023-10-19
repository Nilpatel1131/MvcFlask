from base import app
from flask import render_template


@app.route('/admin/home.html')
def home():
    return render_template("admin/home.html")
