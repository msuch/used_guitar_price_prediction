"""
This module cleans up the scraped used guitar data for modeling.
Subsets to the top 20 guitar brands by number of sales.
Subsets to guitars selling between $30 and $40,000.
"""

# Imports
import pickle
import logging
import numpy as np
import pandas as pd
import re

# Create new logger
logger = logging.getLogger(__name__)

# Set logging level of root logger, will be used by "__name__" logger too
logging.basicConfig(level=logging.INFO)


def main():
    """
    Main function that runs all other functions. Put used guitar data into
    a pandas dataframe and cleans up some of the data formatting.
    """
    
    # Pickle load the scraped electric guitar data (dictionary)
    electric_guitar_dict = pickle.load(open("data/electric_guitar_dict.pkl", "rb"))
    
    # Convert the dictionary to a pandas dataframe and do some clean up
    logger.info("Converting from dictionary to pandas dataframe.")
    df = to_df(electric_guitar_dict)
    
    # Calling model year functin to create model year column in df
    logger.info("Extracting model year from website title.")
    df['Model Year'] = df.apply(get_model_year, axis = 1)
    
    # Calling model year clean up function
    logger.info("Reformatting model year column.")
    df['Model Year'] = df.apply(clean_model_year, axis = 1)
    
    # Calling model color function to create model color column in df
    logger.info("Extracting model color from website title.")
    df['Model Color'] = df.apply(get_model_color, axis = 1)
    
    # Changing money columns from string with '$' symbol to into float objects
    logger.info("Reformatting final price column.")
    df['Final'] = [float(row.replace(',','')[1:]) for row in df['Final']]
    
    # Calling funciton to change asking price from strings to floats
    logger.info("Reformatting asking price column.")
    df['Asking'] = df.apply(clean_asking_price, axis = 1)
    
    # Create a version of the dataframe with one-hot encoded categorical
    # Variables, and subset to final prices between $30 and $40,000
    logger.info("Dropping rows with NA values or outliers.")
    df_dummy = df_format(df)
    
    # Pickle 'df' and 'df_dummy'
    logger.info("Pickling dataframes.")
    pickle.dump(df, open("data/df.pkl", "wb"))
    pickle.dump(df_dummy, open("data/df_dummy.pkl", "wb"))
    
    
def to_df(electric_guitar_dict):
    """
    Converts the data dictionary into a pandas dataframe. Subsets the data
    to only the top 20 guitar brands by number of sales.
    
    Args:
        electric_guitar_dict (dict): Dictionary containing features from each 
        used guitar sale.
    
    Returns:
        df (pandas.DataFrame): Dataframe containing used guitar sales data
        for the 20 most popular guitar brands.
    """  
    
    # Creating pandas dataframe from dictionary and rearranging column order
    df = pd.DataFrame.from_dict(electric_guitar_dict)
    columns = ['Final', 'Asking', 'Name', 'Date', 'Condition']
    df = df[columns]
    
    # Creating a column for guitar Brand
    df['Brand'] = df['Name'].apply(lambda name: name.split()[0])
    
    # Creating a list of top 20 guitar brands
    top_twenty_guitar_brands =  df['Brand'].value_counts().index.tolist()[:20]
    
    # Creating a dataframe of top 20 guitar brands
    mask = (df['Brand'].isin(top_twenty_guitar_brands))
    df = df[mask]
    
    return df


def get_model_year(row):
    """
    Extracts the model year from the Reverb.com title and 
    create a dataframe column for model year.
    
    Args:
        row (pandas.Series): Pandas series for each row.
    
    Returns:
        (str): When there is a year 
        (np.nan):
    """
    
    # Using regular expressions to check the website title for strings 
    # Containing the model year, returns np.nan if nothing found
    regex_one = r"[1][9][3-9][0-9][s]"
    regex_two = r"[1][9][3-9][0-9]"
    regex_three = r"[2][0][01][0][s]"
    regex_four = r"[2][0][01][0-9]"
    regex_five = r"['][0-9][0][s]"
    regex_six = r"[0-9][0][s]"
    regex_seven = r"['][0-9][0-9]"    
    if re.search(regex_one, row['Name']):
        return re.search(regex_one, row['Name']).group(0)
    elif re.search(regex_two, row['Name']):
        return re.search(regex_two, row['Name']).group(0)
    elif re.search(regex_three, row['Name']):
        return re.search(regex_three, row['Name']).group(0)
    elif re.search(regex_four, row['Name']):
        return re.search(regex_four, row['Name']).group(0)
    elif re.search(regex_five, row['Name']):
        return re.search(regex_five, row['Name']).group(0)
    elif re.search(regex_six, row['Name']):
        return re.search(regex_six, row['Name']).group(0)
    elif re.search(regex_seven, row['Name']):
        return re.search(regex_seven, row['Name']).group(0)
    else:
        return np.nan


def clean_model_year(row):
    """
    Reformats the model year column to more consistent notation.
    
    Args:
        row (pandas.Series): Pandas series for each row.
    
    Returns:
        (int): Model year if one is present.
        (np.nan): NaN if model year is not present.
    """
    
    # Converting model year strings in the website title to ints
    if type(row['Model Year']) == str:
        if "00s" in row['Model Year']:
            return 2005
        if "10s" in row['Model Year']:
            return 2015
        if "30s" in row['Model Year']:
            return 1935
        if "50s" in row['Model Year']:
            return 1955
        if "60s" in row['Model Year']:
            return 1965
        if "'69" in row['Model Year']:
            return 1969
        if "70s" in row['Model Year']:
            return 1975
        if "80s" in row['Model Year']:
            return 1985
        if "90s" in row['Model Year']:
            return 1995
        else:
            return int(row['Model Year'])
    return row['Model Year'] #for nan


def get_model_color(row):
    """
    Extracts the model color from the Reverb.com title and 
    create a dataframe column for model color.
    
    Args:
        row (pandas.Series): Pandas series for each row.
    
    Returns:
        (str): Model year if one is present.
    """
    
    # Subset of colors -- Too many to include all of them
    # If not in this list, will be set to NA
    colors = ['Burst', 
              'Sunburst',
              'Fireburst',
              'Honeyburst',
              'Blue', 
              'White', 
              'Black', 
              'Natural', 
              'Blonde',
              'Turquoise',
              'Red',
              'Green',
              'Gold',
              'Silver',
              'Pink',
              'Yellow',
              'Orange',
              'Cherry',
              'Violet',
              'Ebony',
              'Brown',
              'Mahogany',
              'Walnut',
              'Ivory']
    
    # Returns color name if present in website title, and NA if not
    for color in colors:
        if color in row['Name']:
            return color
        
    return "NA"


def clean_asking_price(row):
    """
    Convert asking price column from a string to a float.
    
    Args:
        row (pandas.Series): Pandas series for each row.
    
    Returns:
        (float): Asking price if one is present.
        (np.nan): NaN if asking price is not 'FREE'.
    """
    
    if row['Asking'] == 'FREE':
        return np.nan
    else:
        return float(row['Asking'].replace(',','')[1:])


def df_format(df):
    """
    Drops rows with NA in them. Drops rows with final prices < $30 or 
    final prices > $ 40,000. One-hot encodes the categorical feature 
    variables. 
    
    Args:
        df (pandas.DataFrame): Dataframe containing used guitar sales data.
    
    Returns:
        df_dummy (pandas.DataFrame): Dataframe containing used guitar sales 
        data, with categorical variables one-hot encoded.
    """
    
    # Drop rows with NA in the asking or final prices
    df = df[np.isfinite(df['Model Year'])]
    df = df[np.isfinite(df['Asking'])]
    
    # Drop rows with final prices < $30 or > $100,000
    df = df[df['Final'] > 30] 
    df = df[df['Final'] < 40000]
    
    # Create one-hot encoded dataframes for each categorical variable
    dummy_brand = pd.get_dummies(df['Brand']) 
    dummy_condition = pd.get_dummies(df['Condition']) 
    dummy_color = pd.get_dummies(df['Model Color'])
    
    # Create a subset of the dataframe with all non-categorical variables
    df_subset = df[['Final', 'Asking', 'Model Year']]
    
    # Combine the subsetted dataframe with the one-hot encoded categoricals
    df_dummy = pd.concat([df_subset, dummy_brand, dummy_condition, dummy_color], axis = 1)
    
    return df_dummy


if __name__ == '__main__':
    main()