# CE 49X - Lab 2: Soil Test Data Analysis

# Student Name: Ada Baştürk
# Student ID: 2020403168
# Date: 16.10.2025

import pandas as pd
import numpy as np

"""
Load the soil test dataset from a CSV file.

Parameters:
    file_path (str): The path to the CSV file.

Returns:
    pd.DataFrame: The loaded DataFrame, or None if the file is not found.
"""

def load_data(file_path):

    try:
        df = pd.read_csv(file_path)
        df.columns = [c.strip() for c in df.columns]
        return df
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File not found: {file_path}. Please check the path."
        )
    except pd.errors.EmptyDataError:
        raise ValueError("CSV appears to be empty (EmptyDataError).")
    except pd.errors.ParserError as pe:
        raise ValueError(f"CSV parsing error: {pe}")

def clean_data(df):
    """
    Clean the dataset by handling missing values and removing outliers from 'soil_ph'.
    
    For each column in ['soil_ph', 'nitrogen', 'phosphorus', 'moisture']:
    - Missing values are filled with the column mean.
    
    Additionally, remove outliers in 'soil_ph' that are more than 3 standard deviations from the mean.
    
    Parameters:
        df (pd.DataFrame): The raw DataFrame.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df_cleaned = df.copy()

    # Columns we expect to clean
    target_cols = ['soil_ph', 'nitrogen', 'phosphorus', 'moisture']

    for col in target_cols:
        if col in df_cleaned.columns:
            # Turns the data to numerical, if not possible marks it 'Nan'
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

            # Finds the mean without NaN values and fill NaN values with column mean
            col_mean = df_cleaned[col].mean(skipna=True)
            df_cleaned[col] = df_cleaned[col].fillna(col_mean)
    
    # Remove outliers in 'soil_ph'which are values more than 3 standard deviations from the mean
    if 'soil_ph' in df_cleaned.columns:
        ph = df_cleaned['soil_ph']
        mu = ph.mean()
        #Calculates the standard deviation of the data set
        sigma = ph.std(ddof=1)  # sample std. deviation by default in pandas
        if pd.notna(sigma) and sigma > 0:
            mask = (np.abs(ph - mu) <= 3 * sigma)
            df_cleaned = df_cleaned.loc[mask].reset_index(drop=True)

    # Prints a preview with 5 rows of the dataframe
    print("Preview after cleaning (first 5 rows):")
    print(df_cleaned.head())

    return df_cleaned

def compute_statistics(df, column):
    """
    Compute and print descriptive statistics for the specified column.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column (str): The name of the column for which to compute statistics.
    """

    # Checks if the input column exists inside the dataframe
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame.")

    # Turns the non-numerical values to NaN, then removes (drops) the NaN values from the column
    s = pd.to_numeric(df[column], errors='coerce').dropna()

    if s.empty:
        raise ValueError(f"Column '{column}' has no numeric data after cleaning.")

    # Calculates the minimum, maximum, mean, median and standard deviation values

    min_val = s.min()
    max_val = s.max()
    mean_val = s.mean()
    median_val = s.median()
    std_val = s.std(ddof=1)  # sample standard deviation

    print(f"\nDescriptive statistics for '{column}':")
    print(f"  Minimum: {min_val}")
    print(f"  Maximum: {max_val}")
    print(f"  Mean: {mean_val:.2f}")
    print(f"  Median: {median_val:.2f}")
    print(f"  Standard Deviation: {std_val:.2f}")

def main():

    # Updates the path to soil_test.csv
    file_path = 'soil_test.csv'

    # Loads and directs the dataset to df dataframe while checking errors
    df = load_data(file_path)

    # Cleans the dataset (fills NaNs with mean, removes soil_ph outliers)
    df_clean = clean_data(df)

    # Computes and displays statistics for 'soil_ph' column
    compute_statistics(df_clean, 'soil_ph')

    compute_statistics(df_clean, 'nitrogen')
    # compute_statistics(df_clean, 'phosphorus')
    # compute_statistics(df_clean, 'moisture')
    
if __name__ == '__main__':
    main()

# =============================================================================
# REFLECTION QUESTIONS
# =============================================================================
# Answer these questions in comments below:

# 1. What was the most challenging part of this lab?
# Answer: Understanding the new functions that comes with Pandas library was challenging

# 2. How could soil data analysis help civil engineers in real projects?
# Answer: Soil data analysis helps us design safe foundations by understanding the behavior and limitations of the soil on the project site

# 3. What additional features would make this soil analysis tool more useful?
# Answer: We could make the tool more interactive by letting users upload their own .csv file and choose which column to analyze.

# 4. How did error handling improve the robustness of your code?
# Answer: The code uses try–except blocks to handle file loading errors, and also checks that the standard deviation is greater than zero and numeric before performing.