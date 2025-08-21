import pandas as pd
import streamlit as st
import os

# --- CONFIG ---
st.set_page_config(page_title="Internal Knowledge Base", page_icon="📚", layout="wide")

# --- LOAD DATA FROM GOOGLE SHEETS ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ExLRaOwXtaFOSFSsNJXkI-19SWkzNUKO_rrV625Ui_0/gviz/tq?tqx=out:csv&sheet=Internal%20KB%20Data"
df = pd.read_csv(sheet_url)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .company-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='company-logo'><img src='https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_2013.png' width='200'></div>", unsafe_allow_html=True)
st.title("🔍 Internal Knowledge Base Search")
st.write("Search issues, view resolutions, and access supporting screenshots instantly.")

# --- SEARCH BAR ---
query = st.text_input("Enter your issue keyword:")

# --- SEARCH FUNCTION ---
if query:
    results = df[df.apply(lambda row: query.lower() in str(row).lower(), axis=1)]

    if results.empty:
        st.warning("No matching results found.")
    else:
        for _, row in results.iterrows():
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)

            st.subheader(f"📝 {row.get('Issue Title', 'No Title')}")

            with st.expander("📄 Description", expanded=False):
                st.write(row.get('Description', 'No Description'))

            with st.expander("✅ Resolution", expanded=False):
                st.write(row.get('Resolution', 'No Resolution'))

            # Screenshot if available
            screenshot = row.get('Screenshot_URL', '')
            if pd.notna(screenshot) and screenshot != '':
                if screenshot.startswith("http"):
                    st.image(screenshot, use_column_width=True)
                elif os.path.exists(screenshot):
                    st.image(screenshot, use_column_width=True)

            tags = row.get('Tags', '')
            if pd.notna(tags) and tags != '':
                st.caption(f"📌 Tags: {tags}")

            st.markdown("</div>", unsafe_allow_html=True)

        # --- DOWNLOAD RESULTS ---
        csv_data = results.to_csv(index=False)
        st.download_button(
            label="⬇ Download Results as CSV",
            data=csv_data,
            file_name="search_results.csv",
            mime="text/csv"
        )
