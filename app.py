import streamlit as st
import feedparser
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta, timezone

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Luxury Intelligence",
    page_icon="💎",
    layout="wide"
)

# --------------------------------
# INDUSTRY NEWS CATEGORIES
# --------------------------------

NEWS_CATEGORIES = {
    "Fashion & Jewelry": [
        "luxury fashion industry",
        "luxury jewelry watches industry",
        "fashion retail luxury brands"
    ],

    "Beauty": [
        "luxury beauty industry",
        "prestige skincare cosmetics",
        "luxury fragrance industry"
    ],

    "Wine & Spirits": [
        "fine wine industry",
        "luxury wine spirits Champagne",
        "wine investment market"
    ],

    "Travel & Hospitality": [
        "luxury hospitality industry",
        "luxury hotels resorts",
        "luxury travel tourism"
    ],

    "Wellness": [
        "luxury wellness industry",
        "luxury wellness retreats",
        "longevity wellness business"
    ],

    "Luxury Business": [
        "luxury industry business earnings",
        "luxury conglomerate mergers acquisitions",
        "luxury consumer spending"
    ],

    "Risk & Regulation": [
        "luxury industry regulatory compliance",
        "luxury fashion supply chain scandal",
        "luxury brands fraud litigation"
    ]
}


# --------------------------------
# NEWS AGGREGATION FUNCTION
# --------------------------------

@st.cache_data(ttl=900, show_spinner=False)
def fetch_news():

    articles = []

    for category, queries in NEWS_CATEGORIES.items():

        for query in queries:

            encoded_query = urllib.parse.quote(query)

            url = (
                "https://news.google.com/rss/search?q="
                + encoded_query
                + "&hl=en-US&gl=US&ceid=US:en"
            )

            feed = feedparser.parse(url)

            for entry in feed.entries:

                # Extract publication date

                published = entry.get("published", "Date unavailable")

                if entry.get("published_parsed"):
                    published = datetime(
                        *entry.published_parsed[:6],
                        tzinfo=timezone.utc
                    )

                # Extract publisher

                publisher = entry.get(
                    "source", {}
                ).get("title", "Unknown Publisher")

                articles.append({
                    "Category": category,
                    "Headline": entry.get("title", "Untitled"),
                    "Publisher": publisher,
                    "Published": published,
                    "Summary": entry.get("summary", ""),
                    "Link": entry.get("link", "")
                })

    df = pd.DataFrame(articles)

    if not df.empty:

        # Remove duplicate headlines

        df = df.drop_duplicates(
            subset=["Headline"]
        )

        # Sort newest articles first

        df["_sort_date"] = pd.to_datetime(
            df["Published"],
            utc=True,
            errors="coerce"
        )

        df = df.sort_values(
            "_sort_date",
            ascending=False,
            na_position="last"
        )

    return df


# --------------------------------
# DASHBOARD HEADER
# --------------------------------

st.title("💎 LUXURY INTELLIGENCE")

st.caption(
    "Industry News & Strategic Intelligence Monitoring"
)

st.divider()


# --------------------------------
# SIDEBAR FILTERS
# --------------------------------

st.sidebar.title("Intelligence Filters")

selected_category = st.sidebar.selectbox(
    "Industry Sector",
    ["All Sectors"] + list(NEWS_CATEGORIES.keys())
)

search_term = st.sidebar.text_input(
    "Search News",
    placeholder="Search brands, topics, companies..."
)

date_range = st.sidebar.selectbox(
    "Publication Period",
    ["All Time", "Last 24 Hours", "Last 7 Days", "Last 30 Days"]
)

if st.sidebar.button("Refresh News", use_container_width=True):
    fetch_news.clear()
    st.rerun()


# --------------------------------
# LOAD NEWS
# --------------------------------

with st.spinner("Gathering industry intelligence..."):
    news_df = fetch_news()


# --------------------------------
# APPLY FILTERS
# --------------------------------

filtered_df = news_df.copy()

if not filtered_df.empty:

    if selected_category != "All Sectors":

        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ]

    if search_term:

        searchable = (
            filtered_df["Headline"].fillna("")
            + " "
            + filtered_df["Summary"].fillna("")
            + " "
            + filtered_df["Publisher"].fillna("")
        )

        filtered_df = filtered_df[
            searchable.str.contains(
                search_term,
                case=False,
                regex=False
            )
        ]

    if date_range != "All Time":

        now = datetime.now(timezone.utc)

        days = {
            "Last 24 Hours": 1,
            "Last 7 Days": 7,
            "Last 30 Days": 30
        }[date_range]

        dates = pd.to_datetime(
            filtered_df["Published"],
            utc=True,
            errors="coerce"
        )

        filtered_df = filtered_df[
            dates >= now - timedelta(days=days)
        ]


# --------------------------------
# DASHBOARD METRICS
# --------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Articles Retrieved",
    len(news_df)
)

col2.metric(
    "Articles Displayed",
    len(filtered_df)
)

col3.metric(
    "Industry Sectors",
    filtered_df["Category"].nunique()
    if not filtered_df.empty else 0
)

st.divider()


# --------------------------------
# NEWS DISPLAY
# --------------------------------

st.subheader("Latest Industry Developments")

if filtered_df.empty:

    st.info(
        "No articles found. Try changing your filters."
    )

else:

    for _, article in filtered_df.iterrows():

        with st.container(border=True):

            st.caption(
                f"{article['Category']} | "
                f"{article['Publisher']}"
            )

            st.markdown(
                f"### [{article['Headline']}]"
                f"({article['Link']})"
            )

            st.write(article["Summary"], unsafe_allow_html=False)

            if isinstance(article["Published"], datetime):

                st.caption(
                    "Published: "
                    + article["Published"].strftime(
                        "%B %d, %Y %H:%M UTC"
                    )
                )

            st.markdown(
                f"[Read Original Article ↗]({article['Link']})"
            )


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "LUXURY INTELLIGENCE | Independent Industry Monitoring"
)

st.caption(
    "News content belongs to its respective publishers. "
    "This dashboard aggregates publicly accessible news feeds."
)
