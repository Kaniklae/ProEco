import pandas as pd
import numpy as np
import streamlit as st 
from google.oauth2 import ervice_account
from googleapiclient.discovery import build
import io
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
    SERVICE_ACCOUNT_FILE = "service_account.json"

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)
    drive_service = build ("drive", "v3", credentials = credentials)
    FILE_ID = "1fmlXxTP-wvczjYUkjCKKXM5tmSG6ft-r"
    def download_file(file_id):
        request = drive_service.files().get_media(fileId = file_id)
        fh = io.BytesIO()(fh, request)
        
        downloader = googleapiclient.hhtp.MediaIoBaseDownload
        done = False
        while not done:
            status, done = downloader.newt_chunk()
            st.write(f"Download {int(status.progress()*100)}%."
        fh.seek(0)
        return fh

    buffer = download_file(FILE_ID)

    
    df = pd.read_csv(buffer)

   
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
    
    
