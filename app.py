import streamlit as st
import pandas as pd
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Mini Jane", layout="wide")
st.title("📊 Mini Jane – Energy File Analyzer")

# 📤 File Upload (Always Shown)
st.markdown("### 📤 Step 1: Upload your energy data")
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    st.success(f"✅ File '{uploaded_file.name}' received!")

# Store file in session_state
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df
    except Exception as e:
        st.error(f"Error processing file: {e}")

if "df" in st.session_state:
    st.success("✅ File uploaded successfully.")
    st.subheader("📄 Data Preview")
    st.dataframe(st.session_state.df.head(50))

    # 📈 Charts Section
    st.subheader("📈 Usage & Cost Charts")
    df = st.session_state.df.copy()

    # Parse date column if possible
    for col in df.columns:
        if "date" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
                df = df.sort_values(by=col)
            except:
                pass

    # Line chart: total usage over time
    if "Usage" in df.columns or "Usage_kWh" in df.columns:
        usage_col = "Usage" if "Usage" in df.columns else "Usage_kWh"
        date_col = next((c for c in df.columns if "date" in c.lower()), None)

        if date_col:
            st.markdown("**🔹 Total Usage Over Time**")
            usage_chart_data = df.groupby(date_col)[usage_col].sum()
            st.line_chart(usage_chart_data)

    # Bar chart: total usage by building
    if "Building" in df.columns:
        st.markdown("**🏢 Total Usage by Building**")
        usage_by_building = df.groupby("Building")[usage_col].sum().sort_values(ascending=False)
        st.bar_chart(usage_by_building)

    # Scatterplot: cost vs usage
    if "Cost" in df.columns and "Building" in df.columns:
        st.markdown("**💸 Cost vs Usage by Building**")
        building_summary = df.groupby("Building")[[usage_col, "Cost"]].sum()
        st.scatter_chart(building_summary.rename(columns={usage_col: "Usage", "Cost": "Cost"}))

    # Tabs for different analysis types
    tab1, tab2, tab3, tab4 = st.tabs([
        "💼 Asset Manager Analysis",
        "📦 Energy Procurement",
        "⚡ Demand Response",
        "🚀 Next Best Actions"
    ])

    def run_analysis(prompt_text):
        csv_preview = st.session_state.df.head(100).to_csv(index=False)
        full_prompt = f"""{prompt_text}

If the data includes buildings, cities, or locations, please reference them directly in your analysis.
Call out any buildings or sites with unusual usage or cost behavior.

Data:
{csv_preview}
"""
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

    # Tab 4: Next Best Actions
    with tab4:
        st.markdown("### 🚀 Investment Memo: Next Best Actions")
        if st.button("Generate Next Best Actions"):
            result = run_analysis(
                """You are writing an investment memo for a sustainability director at a commercial real estate firm.
Based on the following usage and cost data, recommend the top 3 investment actions they should consider.
Each recommendation should include:
- The building(s) or site(s) it applies to
- Estimated impact or savings
- A short explanation of why it's important
- Suggested timeframe (immediate / short term / long term)

Use clear bullet points or sections so this can be copied into a board presentation."""
            )
            st.subheader("📋 Recommended Investment Actions")
            st.write(result)

else:
    st.warning("👈 Please upload a file first to view charts and run analysis.")
