import streamlit as st
import pandas as pd
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Mini Jane", layout="wide")
st.title("📊 Mini Jane – Energy File Analyzer")

# ─────────────────────────────────────
# 📤 File Upload (Always Shown)
# ─────────────────────────────────────
st.sidebar.header("📤 Step 1: Upload your data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Store file in session_state so it's accessible across tabs
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Show upload confirmation
if "df" in st.session_state:
    st.success("✅ File uploaded successfully.")
    st.subheader("📄 Data Preview")
    st.dataframe(st.session_state.df.head(20))

    # Tabs for different analysis types
    tab1, tab2, tab3 = st.tabs([
        "💼 Asset Manager Analysis",
        "📦 Energy Procurement",
        "⚡ Demand Response"
    ])

    def run_analysis(prompt_text):
        csv_preview = st.session_state.df.head(50).to_csv(index=False)
        full_prompt = f"{prompt_text}\n\nData:\n{csv_preview}"
        with st.spinner("Analyzing with GPT..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful energy analyst."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            return response.choices[0].message.content

    # Tab 1: Asset Manager
    with tab1:
        st.markdown("### 👤 Real Estate Asset Manager View")
        if st.button("Run Asset Management Analysis"):
            result = run_analysis(
                """You are an energy analyst advising a real estate asset manager.
Analyze this usage and cost data. Provide:
- Key usage/cost patterns
- Any anomalies in weekday vs weekend usage
- Estimated annualized energy spend
- Suggestions that could improve NOI through better energy use

Be concise and financial-focused."""
            )
            st.subheader("🧠 GPT Insights")
            st.write(result)

    # Tab 2: Procurement
    with tab2:
        st.markdown("### 📦 Energy Procurement View")
        if st.button("Run Procurement Analysis"):
            result = run_analysis(
                """You are an energy analyst advising a procurement manager.
Analyze this energy usage data and suggest:
- Better-fitting supply rate structures (flat, TOU, etc.)
- Opportunities to renegotiate contracts
- Cost trends or risk factors related to procurement decisions

Be direct and sourcing-focused."""
            )
            st.subheader("🧠 GPT Insights")
            st.write(result)

    # Tab 3: Demand Response
    with tab3:
        st.markdown("### ⚡ Demand Response Strategy")
        if st.button("Run Demand Response Analysis"):
            result = run_analysis(
                """You are a demand response advisor analyzing a building’s energy profile.
Provide:
- Peak demand periods
- Opportunities to reduce or shift load
- Recommendations for DR participation
- Potential earnings if enrolled in DR

Be technical and DR-focused."""
            )
            st.subheader("🧠 GPT Insights")
            st.write(result)

else:
    st.warning("👈 Please upload a file first to view the analysis tabs.")
