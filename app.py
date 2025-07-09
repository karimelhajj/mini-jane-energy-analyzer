import streamlit as st
import pandas as pd
import openai
import io
import os

# 🔐 OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Mini Jane", layout="wide")
st.title("📊 Mini Jane – Energy File Analyzer")

# ─────────────────────────────────────
# 📚 Sidebar Controls
# ─────────────────────────────────────
st.sidebar.title("Mini Jane Controls")

uploaded_file = st.sidebar.file_uploader("📤 Upload energy CSV or Excel", type=["csv", "xlsx"])

prompt_type = st.sidebar.radio("📌 Choose your analysis focus:", [
    "💼 Asset Management",
    "📦 Energy Procurement",
    "⚡ Demand Response"
])

# ─────────────────────────────────────
# 🧠 Prompt Templates
# ─────────────────────────────────────
def get_prompt(csv_preview, focus):
    if focus == "💼 Asset Management":
        return f"""You are an energy analyst advising a real estate asset manager.
Analyze this usage and cost data. Provide:
- Key usage/cost patterns
- Any anomalies in weekday vs weekend usage
- Estimated annualized energy spend
- Suggestions that could improve NOI through better energy use

Stay concise and financial-focused.

Data:
{csv_preview}
"""
    elif focus == "📦 Energy Procurement":
        return f"""You are an energy analyst advising a procurement manager.
Analyze this energy usage data and suggest:
- Better-fitting supply rate structures (flat, TOU, etc.)
- Opportunities to renegotiate contracts
- Cost trends or risk factors related to procurement decisions

Be direct and sourcing-focused.

Data:
{csv_preview}
"""
    elif focus == "⚡ Demand Response":
        return f"""You are a demand response program advisor.
Analyze the energy usage data and provide:
- Peak demand periods
- Frequency and duration of load spikes
- Opportunities to reduce or shift load for DR participation
- Estimated potential earnings or benefits from joining DR programs

Be technical and DR-focused.

Data:
{csv_preview}
"""
    else:
        return "Invalid prompt selection."

# ─────────────────────────────────────
# 🧾 Main App Logic
# ─────────────────────────────────────
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📄 Data Preview")
        st.dataframe(df.head(20))

        if st.button("🔍 Analyze with GPT"):
            csv_preview = df.head(50).to_csv(index=False)
            prompt = get_prompt(csv_preview, prompt_type)

            with st.spinner("Analyzing with GPT-3.5..."):
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful energy analyst."},
                        {"role": "user", "content": prompt}
                    ]
                )
                analysis = response.choices[0].message.content

            st.subheader("🧠 AI Insights")
            st.write(analysis)

    except Exception as e:
        st.error(f"❌ Oops! Could not process file: {e}")
