#!/usr/bin/env python
import json
from datetime import datetime
from datetime import date
from flask import Flask, request, session, url_for, redirect, abort, render_template, jsonify, flash

# Define flask app
app = Flask(__name__)
app.config.from_object('config')

# Flask Views

@app.route('/')
def index():
  return render_template('index.html', house="House of Representatives", year=2015, datafile="house-2015.json")

@app.route('/house/<int:year>')
def house(year):
  return render_template('index.html', house="House of Representatives", year=year, datafile="house-"+str(year)+".json")

@app.route('/senate/<int:year>')
def senate(year):
  return render_template('index.html', house="House of Representatives", year=year, datafile="senate-"+str(year)+".json")

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=5001)