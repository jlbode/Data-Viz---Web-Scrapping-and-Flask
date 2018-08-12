# =============================================================================
# 
#  Josh Bode
#  Aug 11, 2018
#  UCBSAN201805DATA1 - Webscrapping/Flask Homework
# 
# # MISSION to MARS
#   
# ## Step 2 - MongoDB and Flask Application
#   Use MongoDB with Flask templating to create a new HTML 
#   page that displays all of the information that was 
#   scraped from the URLs above.
# 
# * Start by converting your Jupyter notebook into a 
#   Python script called `scrape_mars.py` 
#   with a function called `scrape` that will execute 
#   all of your scraping code from above and return 
#   one Python dictionary containing all of the scraped data.
# 
# =============================================================================

# =============================================================================
# 1. IMPORT LIBRARIES
# =============================================================================

import pandas as pd 
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser

# =============================================================================
# 2. Function to Scrape All Sites
# =============================================================================

def scrape():
    
    #-------------------------------------
    #A. SCRAPE THE MARS NEWS WEBPAGE
    #-------------------------------------
    
    #1. Define browser and url
    b = Browser('chrome')
    url = 'https://mars.nasa.gov/news/'
    
    #2. Use splinter to read the page
    b.visit(url)
    html = b.html
    
    #3. Create a beatiful soup object
    soup = bs(html, 'lxml')
    
    #4. Extract latest headline and text
    results = soup.find_all('div', class_="content_title")
    news_title = results[0].find('a').text.strip()
    news_text = soup.find('div', class_='image_and_description_container').a.text.strip()

    #-------------------------------------
    #B. SCRAPE MARS DATA TABLE
    #-------------------------------------
    
    #1. Define Url
    url = "https://space-facts.com/mars/"
    
    #2. Convert to data frame
    tables = pd.read_html(url)
    table_df = tables[0]
    table_df.columns = ['Metric', 'Value']
    table_dict = table_df.to_dict(orient = 'list')
    
    
    #-----------------------------------
    #C. JPL MARS FEATURED IMAGE
    #-----------------------------------
    
    #1.Define url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    
    #2. Use splinter to read the page
    b.visit(url)
    
    #3. Click on full image button
    b.click_link_by_partial_text('FULL')
    
    #4. Read in html into beautiful soup
    html = b.html
    soup = bs(html, 'lxml')
    
    #5. Find images with tag  (note tried pulling the attribut)
    image = soup.find('img', class_='fancybox-image')
    
    #6. Extract the url of the image
    try :
        image_dict = image.attrs
        feat_img = "https://www.jpl.nasa.gov" + image_dict['src']
        feat_img
    except AttributeError:
        print('Oops, the image is elusive')
        feat_img = ""
        
    
    #-------------------------------------
    #D. SCRAPE MARS HEMISPHERE IMAGES
    #-------------------------------------
    
    #1. Define Urls
    url1 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    url2 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    url3 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    url4 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    
    #2. List to hold image url information
    hemisphere_image_urls = []
    
    #3. LOOP THROUGH URLS
    for url in [url1, url2, url3, url4] : 
    
        #a. Send request
        response = requests.get(url)
    
        #b. Create Soup
        soup = bs(response.text,'lxml')
    
        #c. Extract hemisphere title 
        title = soup.find("h2", class_="title").text
        print(title)
        
        #d. Extract the image url
        links = soup.find_all("a", href = True)
        for row in links: 
            if row.text.strip() == "Sample":
                imgurl = row['href']
                print(f'{imgurl}') 
    
        #e. Extract the image title
        title = soup.find("h2", class_="title").text
        
        #f: Store in dictionary
        imgdict = {'title': title, 'url': imgurl}
        
        #g. Add to list
        hemisphere_image_urls.append(imgdict)

    #-------------------------------------
    #E. Store results in a dictionary and return
    #-------------------------------------
    
    # 1.Store results into a dictionary
    results_dict = {
            "news_title": news_title, 
            "news_text": news_text, 
            "mars_facts": table_dict,
            "feat_img": feat_img,
            "hemi_urls": hemisphere_image_urls,
            }
    
    # 2. Return results
    return  results_dict
           