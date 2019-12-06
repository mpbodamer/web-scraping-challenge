import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time

def browserInit(): #create the browser object
	executablePath = {'executable_path' : "/usr/local/bin/chromedriver"}
	browser = Browser ('chrome', **executablePath, headless = False)

	return browser

def getWebData(url): #Load the html into a beautifulsoup object and return it

	nasaURL = url

	browser = browserInit()

	browser.visit(nasaURL)

	time.sleep(3) #The articleBody will be a nonetype if the webpage doesnt load fully. Sleep makes sure it does.

	marsHTML = browser.html
	marsSoup = BeautifulSoup(marsHTML, 'html.parser')

	return marsSoup

def webScraper():
	marsURL = "https://mars.nasa.gov/news"
	imageURL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	twitterURL = "https://twitter.com/marswxreport?lang=en"
	factsURL = "https://space-facts.com/mars/"
	marsHemispheresURL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

	scrapedData = {}
	marsSoup = getWebData(marsURL)

	articleTitle = marsSoup.find("div", class_= "content_title").find("a").text
	articleBody = marsSoup.find("div", class_= "article_teaser_body").text

	print(articleTitle)
	print(articleBody)

	scrapedData["articleTitle"] = articleTitle
	scrapedData["articleBody"] = articleBody

	#-------------------

	imageSoup = getWebData(imageURL)

	imageData = imageSoup.find("a", class_="button fancybox")
	largeImageData = (imageData.attrs["data-fancybox-href"].replace("mediumsize", "largesize")).replace("_ip", "_hires")


	featuredImage = ("https://www.jpl.nasa.gov" + largeImageData)

	print(featuredImage)

	scrapedData["featuredImage"] = featuredImage

	#-------------------

	twitterSoup = getWebData(twitterURL)
	twitterData = twitterSoup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

	print(twitterData)

	scrapedData["marsWeather"] = twitterData

	#-------------------

	factsData = pd.read_html(factsURL)
	factsDataDf = factsData[0]
	factsDataDf.columns = ["Description", "Value"]
	factsDataDf.set_index("Description", inplace=True)
	factsTable = factsDataDf.to_html()
	factsTable = factsTable.replace("\n", "")

	scrapedData["marsFacts"] = factsTable

	#-------------------

	print("hemisphere url unable to be reached")

	return scrapedData
