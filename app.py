import streamlit as st
import feedparser
import urllib.parse
import urllib.request
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
        "Premium Automotive & Yachts",
        "Luxury Hospitality & Travel",
        "High-End Real Estate",
        "Luxury Consumer Trends"
    ],
    default=["Luxury Fashion & Goods", "Haute Horlogerie & Jewelry"]
)

custom_brand = st.text_input("Or scan a specific luxury brand or competitor (e.g., LVMH, Rolex):")

scan_list = list(luxury_topics)
if custom_brand:
    scan_list.append(custom_brand)

# --- THE SCANNER ENGINE ---
if not scan_list:
    st.info("Please select at least one luxury topic or type a brand name above to start scanning.")
else:
    for topic in scan_list:
        st.header(f"📡 Live Stream: {topic}")
        
        encoded_term = urllib.parse.quote_plus(topic)
        google_news_url = f"https://google.com{encoded_term}&hl=en-US&gl=US&ceid=US:en"
        
        try:
            req = urllib.request.Request(
                google_news_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_xml_data = response.read()
            
            feed = feedparser.parse(raw_xml_data)
            
            if not feed.entries:
                st.info(f"No recent news found for '{topic}'.")
            else:
                for entry in feed.entries[:5]:
                    title = entry.get('title', 'No Title')
                    link = entry.get('link', '#')
                    published = entry.get('published', 'Date unknown')
                    source = entry.get('source', {}).get('text', 'Unknown Source')
                    
                    st.markdown(f"### **[{title}]({link})**")
                    st.markdown(f"📰 *Source: {source}* | 🕒 *Published: {published}*")
        
        except Exception as e:
            st.error(f"Could not reach data stream for '{topic}'. The server might be busy. Please try refreshing.")
        
        st.markdown("---")
