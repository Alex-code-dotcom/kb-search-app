
import pandas as pd
import streamlit as st

# Load the KB file
df = pd.read_excel("my_kb.xlsx")  # <- Update name if needed

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
            st.write(row.get('Resolution', 'No Resolution'))
            st.caption(f"📌 Tags: {row.get('Tags', '')}")
            if 'test' in row:
                st.text(f"Test: {row['test']}")
            st.markdown("---")
