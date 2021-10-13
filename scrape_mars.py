from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    Browser = init_browser()
    mars_dict = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    news_bs= bs(html, 'html.parser')
    title = news_bs.find_all('div', class_='content_title')[0].text
    title_p = news_bs.find_all('div', class_='article_teaser_body')[0].text

    jpl_url = 'https://www.jpl.nasa.gov'
    img_url = 'https://www.jpl.nasa.gov/images?query=mars'
    browser.visit(img_url)
    html = browser.html
    img_bs = bs(html, 'html.parser')
    image_path = img_bs.find_all('img')[2]["src"]
    feat_img_url = jpl_url + image_path

    mars_facts_url = 'https://galaxyfacts-mars.com/'
    html_fact_table = pd.read_html(mars_facts_url)
    mars_fact_df = html_fact_table[1]
    mars_fact_df.columns = ["Decription", "Value"]
    mfacts_html_table = mars_fact_df.to_html()

    
    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)
    hem_html = browser.html
    hem_bs = bs(hem_url)
    mars_hem = hem_bs.find_all('div', class_='item')
    hem_img_urls = []
    for x in all_hem:
        title = x.find("h3").text
        img_url = x.a["href"]
        url = hem_url + img_url
        response = requests.get(url)
        soup = bs(response.text,"html.parser")
        new_url = soup.find("img", class_="wide-image")["src"]
        full_url = hem_url + new_url
        hem_img_urls.append({"title": title, "img_url": full_url})



    mars_dict = {
        "title": title,
        "title_p": title_p,
        "feat_img_url": feat_img_url,
        "mars_fact_table": str(mfacts_html_table),
        "hemisphere_images": hem_img_urls
    }
    return mars_dict