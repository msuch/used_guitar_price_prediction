"""
This module contains the selenium web scraping script.
This module specifically scrapes used guitar data from Reverb.com
"""

# Imports
import pickle
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Create new logger
logger = logging.getLogger(__name__)

# Set logging level of root logger, will be used by "__name__" logger too
logging.basicConfig(level=logging.INFO)


def main():
    """
    Main function that runs all other functions. Scrapes Reverb.com for used 
    guitar features and pickles the data as a dictionary for later use.
    
    Args:
        None.
    
    Returns:
        None.
    """

    # Returns a list of links to used guitar sales on Reverb.com
    electric_guitar_links = get_site_links()
    
    # Pickle dump (serialize) the guitar links in case needed later
    pickle.dump(electric_guitar_links, open("data/electric_guitar_links.pkl", "wb"))
    
    # Collect electric guitar feature data from each of the used guitar links
    electric_guitar_dict = get_data(electric_guitar_links)
    
    # Pickle dump (serialize) the feature dictionary for later use
    pickle.dump(electric_guitar_dict, open("data/electric_guitar_dict.pkl", "wb"))


def get_site_links():
    """
    This portion of the web scraper cycles through all of the listings
    of used guitar sales and adds those links to a list. In the next 
    function we will go to each one of these links to extract data.
    
    Args:
        None.
        
    Returns:
        electric_guitar_links (list): Website links to each guitar listing.
    """
    
    # Logging
    logger.info("Getting used guitar site links.")
    
    # Open up webdriver object using Firefox
    driver = webdriver.Firefox()
    driver.get("https://reverb.com/signin")
    driver.implicitly_wait(60) #seconds
    
    # Log in to Reverb.com -- Need to login to see used guitar sales
    login_username = driver.find_element_by_id('user_session_login')
    login_username.send_keys("example@gmail.com") # Enter login username
    login_password = driver.find_element_by_id('user_session_password')
    login_password.send_keys("examplePassword") # Enter login password
    login_password.send_keys(Keys.RETURN)
    
    # Wait for the page to load so that I am fully logged in
    delay = 3 #seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'site-header__avatar')))
        logger.debug("Page is ready!")
    except TimeoutException:
        logger.debug("Loading took too much time!")
    
    # Go the the used guitar sales portion of Reverb.com
    driver.get("https://reverb.com/price-guide/electric-guitars")
    
    # Wait for the page to fully load
    delay = 60 #seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-card-img-container')))
        logger.debug("Page is ready!")
    except TimeoutException:
        logger.debug("Loading took too much time!")
    
    # Cycle through all of the guitar listing pages and collect links
    # For the individual guitar listings
    num_listings = 213
    electric_guitar_links = []
    for pages in range(1,num_listings+1): #212 pages of electric guitar listings to go through
        links = driver.find_elements_by_tag_name('a')
        for link in links:
            link = str(link.get_attribute('href'))
            if 'price-guide' and '/guide' in link:
                electric_guitar_links.append(link)
        next_page_link = driver.find_element_by_link_text('Next')
        next_page_link.click()
    
    return electric_guitar_links


def get_data(electric_guitar_links):
    """
    Collect electric guitar feature data from each of the used guitar links.
    
    Args:
        electric_guitar_links (list): Website links to each guitar listing.
    
    Returns:
        electric_guitar_dict (dict): Dictionary containing features from each 
        used guitar sale.
    """
    
    # Logging
    logger.info("Getting data from guitar links.")
    
    # Create empty dictionary to store the data from each guitar webpage
    data_header = ['Name', 'Date', 'Condition', 'Asking', 'Final']
    electric_guitar_dict = {key: [] for key in data_header}
    
    # Open up webdriver object using Firefox
    driver = webdriver.Firefox()
    driver.get("https://reverb.com/signin")
    driver.implicitly_wait(60) #seconds
    
    # Log in to Reverb.com -- Need to login to see used guitar sales
    login_username = driver.find_element_by_id('user_session_login')
    login_username.send_keys("example@gmail.com") # Enter login username
    login_password = driver.find_element_by_id('user_session_password')
    login_password.send_keys("examplePassword") # Enter login password
    login_password.send_keys(Keys.RETURN)
    
    # Wait for the page to load so that I am fully logged in
    delay = 3 #seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'site-header__avatar')))
        logger.debug("Page is ready!")
    except TimeoutException:
        logger.debug("Loading took too much time!")
    
    # Loop through all the electric guitar pages on reverb.com
    for link in electric_guitar_links:
        
        # Change to the new guitar webpage
        driver.get(link)
    
        # Check if there are any recent listings at all, skip if not
        # Script will crash without this line of code if there are no sales
        delay = 1
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'date')))
        except TimeoutException:
            continue
    
        # Get the WebElement objects for the data of the guitars
        name = driver.find_element_by_class_name('heading-1')
        dates = driver.find_elements_by_class_name('date')
        conditions = driver.find_elements_by_class_name('condition')
        prices = driver.find_elements_by_class_name('price-history-table-price')
        
        # Add the WebElement's text to the dictionary for guitar name
        for i in range(len(dates)-1):
            electric_guitar_dict['Name'].append(name.text)
            logger.debug(i)
        
        # Add the WebElement's text to the dictionary for selling date
        for date in dates[1:]:
            electric_guitar_dict['Date'].append(date.text)
            logger.debug(date.text)
        
        # Add the WebElement's text to the dictionary for guitar condition
        for condition in conditions[1:]:
            electric_guitar_dict['Condition'].append(condition.text)
            logger.debug(condition.text)
        
        # Add the WebElement's text to the dictionary for asking and selling price
        counter = 1
        for price in prices:
            if counter % 2 == 1:
                electric_guitar_dict['Asking'].append(price.text)
            else:
                electric_guitar_dict['Final'].append(price.text)
            counter += 1
            logger.debug(price.text)
        
    return electric_guitar_dict


if __name__ == '__main__':
    main()