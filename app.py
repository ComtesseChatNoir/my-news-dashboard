import streamlit as st
import feedparser
import urllib.parse
import ssl

if not hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(page_title="Luxury Industry Scanner", layout="wide")
st.title("💎 Luxury Industry Intelligence Briefing")
st.write("Live data aggregation for luxury sectors.")

# --- THE HOOK: SELECT MULTIPLE LUXURY SECTORS ---
luxury_topics = st.multiselect(
    "Select the luxury sectors you want to scan today:",
    options=[
        "Luxury Fashion & Goods",
        "Haute Horlogerie & Jewelry",
        "Wine & Spirits",
        "Luxury Hospitality & Travel",
        "High-End Real Estate",
        "Luxury Consumer Trends",
        "Premium and Luxury Beauty",
        "Luxury Wellness"
    ],
    default=["Luxury Fashion & Goods", "Haute Horlogerie & Jewelry"]
)

# Optional text box if you want to type a hyper-specific brand name on the fly
custom_brand = st.text_input("Or scan a specific luxury brand or competitor (e.g., LVMH, Rolex):")

# Combine your selected topics and your custom text search into one master list
scan_list = list(luxury_topics)
if custom_brand:
    scan_list.append(custom_brand)

# --- THE SCANNER ENGINE ---
if not scan_list:
    st.info("Please select at least one luxury topic or type a brand name above to start scanning.")
else:
    # Run a separate live scan for every single item chosen
    for topic in scan_list:
        st.header(f"📡 Live Stream: {topic}")
        
        encoded_term = urllib.parse.quote_plus(topic)
        google_news_url = f"https://google.com{encoded_term}&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(google_news_url)
        
        if not feed.entries:
            st.info(f"No recent news found for '{topic}'.")
        else:
            # Create a clean layout displaying the top 5 articles per topic
            for entry in feed.entries[:5]:
                title = entry.get('title', 'No Title')
                link = entry.get('link', '#')
                published = entry.get('published', 'Date unknown')
                source = entry.get('source', {}).get('text', 'Unknown Source')
                
                st.markdown(f"### **[{title}]({link})**")
                st.markdown(f"📰 *Source: {source}* | 🕒 *Published: {published}*")
        
        st.markdown("---")
