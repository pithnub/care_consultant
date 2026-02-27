import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- INITIAL SETUP ---
st.set_page_config(page_title="PelleCare: Digital Care Consultant", layout="wide")

st.title("🛡️ PelleCare Digital Care Consultant")
st.write("---")

# --- INPUT SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. The Asset")
    leather_type = st.selectbox("Finish Type:", ["Finished", "Semi-Aniline", "Aniline", "Waxed/Oiled"])
    current_state = st.select_slider("Current Condition:", options=["Pristine", "Slightly Dry", "Aged/Wear", "Crisis"])

with col2:
    st.header("2. Environment")
    sunlight = st.select_slider("Sun Exposure:", options=["Indoor", "Moderate", "High Sun"])
    care_adherence = st.radio("Care Frequency:", ["None (Reactive)", "Occasional", "PelleCare Ritual (Proactive)"])

# --- THE SIMULATION ENGINE ---
if st.button("🚀 EXECUTE 5-YEAR PROJECTION"):
    # Mock data for leather health over 5 years
    years = np.arange(0, 6)
    
    # Calculate degradation rate based on inputs
    uv_penalty = {"Indoor": 5, "Moderate": 15, "High Sun": 30}[sunlight]
    care_boost = {"None (Reactive)": 0, "Occasional": 10, "PelleCare Ritual (Proactive)": 25}[care_adherence]
    
    # Baseline health decline
    health = 100 - (years * uv_penalty) + (years * care_boost)
    health = np.clip(health, 0, 100) # Keep within 0-100%

    # --- PLOTTING ---
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(years, health, marker='o', color='#8e735b', linewidth=3, label="Projected Health")
    ax.fill_between(years, health, alpha=0.1, color='#8e735b')
    ax.set_ylim(0, 110)
    ax.set_xlabel("Years into the Future")
    ax.set_ylabel("Leather Integrity (%)")
    ax.set_title(f"5-Year Integrity Forecast for {leather_type} Leather")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    st.pyplot(fig)

    if health[-1] < 40:
        st.error(f"🚨 CRITICAL: Without better care, this asset faces catastrophic cracking by year {np.where(health < 50)[0][0]}.")
    elif health[-1] > 80:
        st.success("✨ SUSTAINABLE: This ritual will maintain showroom quality for the next 5+ years.")
