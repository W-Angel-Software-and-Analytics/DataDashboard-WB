from myapp import app

# import json
# import plotly
# from flask import render_template
# from wrangling_scripts.wrangle_data import return_figures


@app.route("/")
def hello_world():
    return "<p> Hello </p>"
