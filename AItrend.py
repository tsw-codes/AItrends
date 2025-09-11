# app.py

import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from pytrends import exceptions

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("AI Trends Explorer 🌐")
st.write("Explore Google Trends data for AI keywords!")

# User inputs
keywords_input = st.text_input(
    "Enter keywords (comma-separated):", 
    value="ChatGPT, AI jobs, AI art"
)
keywords = [kw.strip() for kw in keywords_input.split(",")]

region = st.selectbox(
    "Select region:",
    options=[
        "Worldwide", "United States", "Nigeria", "India", "United Kingdom",
        "Canada", "Australia", "Germany", "France", "Japan", "Brazil", 
        "South Korea", "China", "Russia", "Mexico", "Italy", "Spain", 
        "Netherlands", "Sweden", "Norway", "Denmark", "Finland", 
        "Switzerland", "Austria", "Belgium", "Poland", "Turkey", 
        "South Africa", "Egypt", "Kenya", "Ghana", "Morocco", 
        "Argentina", "Chile", "Colombia", "Peru", "Venezuela",
        "Thailand", "Vietnam", "Malaysia", "Singapore", "Indonesia",
        "Philippines", "Taiwan", "Hong Kong", "New Zealand", "Israel"
    ]
)

years = st.slider(
    "Select number of past years to analyze:",
    min_value=1,
    max_value=10,
    value=5
)

if st.button("Fetch Trends"):
    st.write("Fetching data... ⏳")
    
    # -----------------------------
    # Connect to Google Trends
    # -----------------------------
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # Map region names to pytrends codes
    geo_map = {
        "Worldwide": "",
        "United States": "US", "Nigeria": "NG", "India": "IN", "United Kingdom": "GB",
        "Canada": "CA", "Australia": "AU", "Germany": "DE", "France": "FR", 
        "Japan": "JP", "Brazil": "BR", "South Korea": "KR", "China": "CN", 
        "Russia": "RU", "Mexico": "MX", "Italy": "IT", "Spain": "ES",
        "Netherlands": "NL", "Sweden": "SE", "Norway": "NO", "Denmark": "DK",
        "Finland": "FI", "Switzerland": "CH", "Austria": "AT", "Belgium": "BE",
        "Poland": "PL", "Turkey": "TR", "South Africa": "ZA", "Egypt": "EG",
        "Kenya": "KE", "Ghana": "GH", "Morocco": "MA", "Argentina": "AR",
        "Chile": "CL", "Colombia": "CO", "Peru": "PE", "Venezuela": "VE",
        "Thailand": "TH", "Vietnam": "VN", "Malaysia": "MY", "Singapore": "SG",
        "Indonesia": "ID", "Philippines": "PH", "Taiwan": "TW", "Hong Kong": "HK",
        "New Zealand": "NZ", "Israel": "IL"
    }
    
    timeframe = f"{2025-years}-01-01 2025-12-31"
    
    try:
        # Add a small delay to avoid rate limiting
        time.sleep(1)
        
        pytrends.build_payload(kw_list=keywords, geo=geo_map[region], timeframe=timeframe)
        data = pytrends.interest_over_time()
        
        if data.empty:
            st.write("No data found. Try different keywords or region.")
        else:
            data = data.drop(columns=['isPartial'])
            st.write("### Trend Data")
            st.dataframe(data.tail())

            # -----------------------------
            # Plotting
            # -----------------------------
            st.write("### Trend Graph")
            plt.figure(figsize=(10,5))
            sns.lineplot(data=data)
            plt.title("Keyword Popularity Over Time")
            plt.xlabel("Date")
            plt.ylabel("Search Interest")
            plt.legend(labels=keywords)
            plt.xticks(rotation=45)
            st.pyplot(plt)
            
    except exceptions.TooManyRequestsError:
        st.error("⚠️ Too many requests to Google Trends. Please wait a few minutes before trying again.")
        st.info("💡 Tip: Google Trends has rate limits. Try waiting 2-3 minutes between requests.")
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("💡 Try different keywords, region, or time period.")
