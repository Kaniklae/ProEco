import pandas as pd
import numpy as np
import streamlit as st 
import requests


st.title ("Energy Consumption and Production in France")
st.header("Risk of Blackout Analysis")
st.sidebar.title("Table of contents")
pages=["Exploration","Data Visualization","Forecasting"]
page=st.sidebar.radio("Go to",pages)

if page==pages[0]:
    st.subheader("Exploration")
    st.write("## Data Presentation")
    text = "The data is from the French government and contains information about the energy consumption in France from 2000 to 2020"

    url = f"https://drive.google.com/uc?export=download&id=1fmlXxTP-wvczjYUkjCKKXM5tmSG6ft-r"
    response = requests.get(url)
    with open ("eco.csv", "wb") as f:
        f.write(response.content)

    df = pd.read_csv("eco.csv", sep=";")
    st.dataframe(df.head(10))
    st.write(df.shape)
    st.dataframe(df.describe())
    if st.checkbox("Show NA"):
        st.write(df.isna().sum())
    st.write("The data contains some missing values, which will be handled in the data cleaning step.")
    st.write("# Check for 'ND' values in specific columns:")
    st.write(df.columns)


    numerical_cols = df.select_dtypes(include=np.number).columns
    for col in numerical_cols:
        df[col].fillna(df[col].mean(), inplace=True)

    # Handle 'ND' values in 'Eolien (MW)'
    eolien_numeric = []
    for value in df['Eolien (MW)']:
        if isinstance(value, str) and value != 'ND':
            try:
                eolien_numeric.append(float(value))
            except ValueError:
                pass  # Ignore values that can't be converted to numeric

    if eolien_numeric:
        mean_eolien = np.mean(eolien_numeric)
        df['Eolien (MW)'] = df['Eolien (MW)'].replace('ND', mean_eolien)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Data Validation
    print("\nMissing values per column after cleaning:")
    print(df.isnull().sum())
    print("\n'ND' values in 'Eolien (MW)' after cleaning:", (df['Eolien (MW)'] == 'ND').sum())
    print("\nNumber of duplicate rows after cleaning:", df.duplicated().sum())

    # Save the cleaned DataFrame
    df.to_csv("cleaned_eco2mix.csv", index=False)

    
    # Converting the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')  
   

    # Verify the conversion
    st.write(df['Date'].dtype)




if page == pages[1]:
    df = pd.read_csv("cleaned_eco2mix.csv")
    st.write("## Data Visualization")
    text= "Example analysis: Group data by region and calculate the average consumption"
    region_consumption = df.groupby('Région')['Consommation (MW)'].mean()

    st.write ( "Plotting the average consumption by region")

    fig = plt.figure(figsize=(10,5))
    
    st.barplot(x=region_consumption.index, y=region_consumption.values)
    st.xlabel("Region")
    st.ylabel("Average Consumption (MW)")
    st.title("Average Consumption by Region")
    st.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    st.tight_layout()
    st.show()
    st.pyplot(fig) 
    
    
