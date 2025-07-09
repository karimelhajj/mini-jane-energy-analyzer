import streamlit as st

st.set_page_config(page_title="Upload Test", layout="centered")
st.title("🧪 File Upload Debugger")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    st.write(uploaded_file)
