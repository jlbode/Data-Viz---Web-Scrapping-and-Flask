# =============================================================================
# -*- coding: utf-8 -*-
#  Josh Bode
#  Aug 11, 2018
#  UCBSAN201805DATA1 - Webscrapping/Flask Homework
# 
# # MISSION to MARS
#
#   Step # 3
# 
# * Next, create a route called `/scrape` that will 
#   import your `scrape_mars.py` script and 
#   call your `scrape` function.
# 
#  * Store the return value in Mongo as a Python dictionary.
# 
# * Create a root route `/` that will query your Mongo database 
#   and pass the mars data into an HTML template to 
#   display the data.
# 
# * Create a template HTML file called `index.html` that
#   will take the mars data dictionary and display all 
#   of the data in the appropriate HTML elements. 
#   Use the following as a guide for what the final product
#   should look like, but feel free to create your own design. 
# =============================================================================


# =============================================================================
# 1. IMPORT LIBRARIES
# =============================================================================

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# =============================================================================
# 2. CREATE THE FLASK INSTANCE AND MONGO DB DATABASE
# =============================================================================

# A. Create an instance of our Flask app.
app = Flask(__name__)

# B.Create connection variable
conn = 'mongodb://localhost:27017'

# C. Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# D. Declare the database
db = client.mars_db

# E. Declare the collection
collection = db.mars

# =============================================================================
# 3. ROOT ROUTE - FOR FLASK
# =============================================================================
    
# A. Route that will trigger scrape functions
@app.route("/scrape")
def use_scrape():

    #1. Run scraping function
    results_dict = scrape_mars.scrape()

    #2. Insert forecast into database
    collection.insert_one(results_dict)
    
    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

# B. Root route - passes mars data into the HTML template
@app.route("/")
def home():

    # Find data
    mars_info = db.mars.find_one()
   
    # return template and data
    return render_template("01_index.html", mars_info = mars_info)
 

# =============================================================================
# 4. CLOSE OUT FLASK / DEBUG
# =============================================================================

if __name__ == "__main__":
    app.run(debug=True)