import streamlit as st
import pandas as pd
import openai
import io

openai.api_key = "YOUR_API_KEY"

st.title("Mini Jane: Energy File Analyzer")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Preview")
    st.write(df.head())

    # Prepare data for GPT
    csv_string = df.head(50).to_csv(index=False)
    prompt = f"Analyze this building energy data:\n\n{csv_string}\n\nGive insights on cost trends, usage spikes, and potential savings."

    with st.spinner("Analyzing with GPT..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        insights = response['choices'][0]['message']['content']

    st.subheader("AI Insights")
    st.write(insights)
