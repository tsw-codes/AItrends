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
st.info("⏱️ **Rate Limit Notice:** Please wait at least 10 seconds between searches to avoid Google Trends rate limits.")

# User inputs
keywords_input = st.text_input(
    "Enter keywords (comma-separated):", 
    value="ChatGPT, artificial intelligence, machine learning"
)

# Add some popular keyword suggestions
st.write("💡 **Popular AI keywords that usually have data:**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("ChatGPT"):
        keywords_input = "ChatGPT"
with col2:
    if st.button("AI"):
        keywords_input = "artificial intelligence"
with col3:
    if st.button("Machine Learning"):
        keywords_input = "machine learning"
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
    
    # Fix timeframe to use past data only
    from datetime import datetime
    current_year = datetime.now().year
    start_year = current_year - years
    timeframe = f"{start_year}-01-01 {current_year-1}-12-31"
    
    try:
        # Initialize session state for rate limiting
        if 'last_request_time' not in st.session_state:
            st.session_state.last_request_time = 0
        
        # Check if enough time has passed since last request (minimum 10 seconds)
        current_time = time.time()
        time_since_last_request = current_time - st.session_state.last_request_time
        
        if time_since_last_request < 10:
            wait_time = 10 - time_since_last_request
            st.warning(f"⏳ Please wait {wait_time:.1f} more seconds before making another request to avoid rate limits.")
            st.stop()
        
        # Add delay to avoid rate limiting
        time.sleep(2)
        
        # Update last request time
        st.session_state.last_request_time = current_time
        
        # Debug information
        st.write(f"🔍 Searching for: {keywords}")
        st.write(f"📅 Time period: {timeframe}")
        st.write(f"🌍 Region: {region} ({geo_map[region]})")
        
        pytrends.build_payload(kw_list=keywords, geo=geo_map[region], timeframe=timeframe)
        data = pytrends.interest_over_time()
        
        if data.empty:
            st.warning("📭 No data found for your search.")
            st.info("💡 **Suggestions to get data:**")
            st.info("• Try more popular keywords (e.g., 'AI', 'ChatGPT', 'machine learning')")
            st.info("• Use 'Worldwide' instead of a specific region")
            st.info("• Try a longer time period (5-10 years)")
            st.info("• Check spelling of keywords")
            st.info("• Try single keywords instead of multiple")
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
        st.error("⚠️ Too many requests to Google Trends. Please wait 5-10 minutes before trying again.")
        st.info("💡 Tips to avoid rate limits:")
        st.info("• Wait at least 10 seconds between requests")
        st.info("• Refresh the page and wait before making new requests")
        st.info("• Try using fewer keywords (max 3-4)")
        st.info("• Avoid rapid consecutive searches")
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("💡 Try different keywords, region, or time period.")
        st.info("💡 If the error persists, wait a few minutes and try again.")
