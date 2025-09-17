import streamlit as st
from myingres import INGRESChatBot

# ===============================
# Initialize chatbot with dataset
# ===============================
st.set_page_config(page_title="INGRES AI ChatBot", page_icon="💧", layout="wide")
@st.cache_resource
def load_chatbot():
    bot = INGRESChatBot()

    # 🔹 Directly GitHub raw link se load karenge
    github_url = "https://github.com/misterk1269/INGRES_Groundwater_data/raw/main/final_groundwater_predictions%20(1).csv"
    bot.load_data(github_url)

    return bot


ingres_bot = load_chatbot()

# ===============================
# Streamlit UI
# ===============================

st.title("💧 INGRES AI ChatBot (Groundwater Analysis)")
st.write("Ask about groundwater status, predictions, or analysis for any state/year.")

# ===============================
# General Query
# ===============================
query = st.text_input("💬 Ask your question:")
if query:
    with st.spinner("Processing your query..."):
        response = ingres_bot.process_query(query)
    st.success(response)

# ===============================
# State Analysis
# ===============================
st.subheader("🏛️ State Analysis")
state = st.text_input("🔎 Enter State for Analysis:")
if state:
    with st.spinner(f"Analyzing {state}..."):
        analysis = ingres_bot.get_state_analysis(state)
    st.json(analysis)

# ===============================
# Prediction Section
# ===============================
st.subheader("🔮 Groundwater Prediction")
col1, col2 = st.columns(2)

with col1:
    state_pred = st.text_input("State")
    year_pred = st.number_input("Year", min_value=2019, max_value=2025, step=1, value=2023)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=500.0)
    recharge = st.number_input("Recharge (ham)", min_value=0.0, value=100000.0)

with col2:
    discharge = st.number_input("Natural Discharge (ham)", min_value=0.0, value=1000.0)
    extractable = st.number_input("Extractable Resources (ham)", min_value=0.0, value=50000.0)

if st.button("🚀 Predict"):
    with st.spinner("Making prediction..."):
        result = ingres_bot.predict_groundwater_metrics(
            state_pred, year_pred, rainfall, recharge, discharge, extractable
        )
    st.json(result)

# ===============================
# Data Summary Section
# ===============================
if st.button("📊 Show Data Summary"):
    with st.spinner("Generating summary..."):
        summary = ingres_bot.get_data_summary()
    st.json(summary)
