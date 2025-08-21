import pandas as pd
import streamlit as st
import os

# Load the KB file
df = pd.read_excel("my_kb.xlsx")

st.set_page_config(page_title="Knowledge Base", layout="wide")

# Custom CSS for background & card style
st.markdown("""
    <style>
    /* Change page background */
    .stApp {
        background-color: #f5f7fa;
        color: #1f2937;
    }

    /* Style the search results as cards */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Style headings */
    h2, h3 {
        color: #2c5282;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Internal Knowledge Base Search")

query = st.text_input("Enter your issue keyword:")

if query:
    results = df[df.apply(lambda row: query.lower() in str(row).lower(), axis=1)]

    if results.empty:
        st.warning("No matching results found.")
    else:
        for _, row in results.iterrows():
            with st.container():
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                
                st.subheader(f"📝 {row.get('Issue Title', 'No Title')}")
                st.markdown(f"**Description:** {row.get('Description', 'No Description')}")
                st.markdown(f"**Resolution:** {row.get('Resolution', 'No Resolution')}")

                # Show screenshot if available
                screenshot = row.get('Screenshot_URL', '')
                if pd.notna(screenshot) and screenshot != '':
                    if screenshot.startswith("http"):  # If it's a URL
                        st.image(screenshot, use_column_width=True)
                    elif os.path.exists(screenshot):  # If it's a local file
                        st.image(screenshot, use_column_width=True)
                    else:
                        st.warning(f"⚠ Screenshot not found: {screenshot}")

                tags = row.get('Tags', '')
                if pd.notna(tags) and tags != '':
                    st.caption(f"📌 Tags: {tags}")

                st.markdown("</div>", unsafe_allow_html=True)
