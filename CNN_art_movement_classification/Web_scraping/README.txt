### This is the README for the scraping part.

# INTRO AND MOTIVATION
We decided to get our own dataset of images by scraping the website "https://www.copia-di-arte.com/". 
Note that we chose this website because scraping is allowed to everyone, as the robots.txt file of the website says. 
We were particularly interested in the artistic movement of a painting and the content of the painting (the image itself), but we also considered that additional information (as image height and width) could have been useful to filter out some images through a top-down approach.
First of all, we have to understand the structure of the website. Under the section ("Artisti A-Z") we can find a static menu with links of artist names from the first letter of the alphabet to the last. Inside each of these pages, all references to single artists are contained. Then, some artists have more pictures than others, therefore they have more pages. Inside each page, there are links that point to a single painting. Finally this link contains the image, the artistic movement, the image height and the image width.

# OUR WORKFLOW
Because of the complicated structure of the website, we divided the tasks into 5 different jupyter notebooks, which tackle sequentially each part of the scraping part. Most of the notebooks produce an output (either a .csv or a .txt file) that the subsequent notebooks use as an input for their own tasks.

# UTILITY FUNCTIONS
Since this project implied to massively scrape an entire website, we built some utility functions and programs to automate repetitive tasks.
1) The whole scraping part is handled by the class Scraper inside the web_scraping.py file. 
    - everytime a scraper object is instantiated, a selenium webdriver page is initialized with a random fake user agent
    - the scraper is able to scroll down until the bottom of the page
    - the scraper gets an url through the get_url function and automatically scrolls down, such that the whole content of the website is    loaded
    - a find_hrefs function specifically thought for this project, in order to find all the links that match a subset of strings (remember the website is full of links pointing to other links)
2) Help functions inside the help_functions.py, which are used to clean the artists names, title names and check that a specific file has effectively been saved.

# PART 1: scraping schema
The first .py file iterates over each alphabetical page, gets all the pages of each artist using "find_hrefs", then inside each artist finds all the pages and references to each image. The output of this notebook is a .csv called "links_final.csv", containing the link to the image, the title, the artist and the artistic movement. Roughly 55 thousand image links were obtained.

# PART 2: category selection and split
We analyze the data inside the links_final.csv file and make a top-down selection of the images, consider only artistic movements with at least 2 thousand entries. We decided to scrape 29311 images and we created 4 different .csv files with links of the images to download, such that the scraping time was significantly reduced. These 4 .csv files are inside the "temp_txt" folder.

# PART 3: getting height and width
Before downloading the image, we decided to make further restrictions on some images basing on the height and width of the image. Therefore we decided to get more information at image level. Each group member run seperately the PART3 file, producing a f"{member_name}_updated.csv" file. These files are inside the temp2_txt folder.

# PART 4: 
In part 4 we put together the information in the 4 updated .csv files. We filter out images with missing values, the ones that are too squared (a height/width ratio beyond 6.5/10 or 10/6.5) and the ones belonging to three underrepresented movements ('Arte Figurativa astratta', 'Arte Vittoriana', 'Arte astratta figurativa'). After having cleaned artist names and titles we decided to scrape 16K images,
randomly assigning the remaining images to train, validation and test set. The output of this phase is the .csv called "images_to_scrape.csv".

# PART 5: scraping the images
We scrape only the selected images using the Scraper class. The scraper object changes user agent every 100 pictures obtained and checks that the images are saved. All images are saved into a folder called "raw_data" into a Train-Validation-Test structure that will allow us to train our CNN using .flow_from_directory. The raw_data folder is not here inside this folder because:
    - is heavy
    - we manually selected good images, eliminating other 4-4.5 thousand images which were unsuitable for our project. 
