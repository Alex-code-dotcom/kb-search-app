import pandas as pd
import streamlit as st
import os

# Load the KB file
df = pd.read_excel("my_kb.xlsx")

st.set_page_config(page_title="Knowledge Base", layout="wide")
st.title("🔍 Internal Knowledge Base Search")

query = st.text_input("Enter your issue keyword:")

if query:
    results = df[df.apply(lambda row: query.lower() in str(row).lower(), axis=1)]

    if results.empty:
        st.warning("No matching results found.")
    else:
        for _, row in results.iterrows():
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

            st.markdown("---")
