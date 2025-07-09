import streamlit as st
import pandas as pd
import openai
import io

# 🔑 OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Mini Jane", layout="wide")
st.title("📊 Mini Jane – Energy File Analyzer")

uploaded_file = st.file_uploader("Upload your energy CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(df.head(20))

        if st.button("🔍 Analyze with GPT"):
            csv_preview = df.head(50).to_csv(index=False)
            prompt = f"""You are an energy analyst.
Analyze this data and give insights about energy use trends, costs, peaks, anomalies, and optimization opportunities. Be specific and helpful.

Data:
{csv_preview}
"""

            with st.spinner("Analyzing with GPT-4..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                analysis = response['choices'][0]['message']['content']

            st.subheader("🧠 AI Insights")
            st.write(analysis)

    except Exception as e:
        st.error(f"Oops! Could not process file: {e}")
