import marsScraper
import pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsApp")

@app.route("/")
def home_page():
	mars = mongo.db.mars.find_one()
	return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
	mars = mongo.db.mars
	mars_facts = marsScraper.webScraper()
	mars.update({}, mars_facts, upsert=True)
	return render_template("index.html", mars=mars)

if __name__ == "__main__":
	app.run(debug=True)
	app.run(host="0.0.0.0", port=5000)