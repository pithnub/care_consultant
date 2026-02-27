import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- INITIAL SETUP ---
st.set_page_config(page_title="PelléCare Digital Consultant", layout="wide")

# Custom Styling: Premium Leather Aesthetics
st.markdown("""
    <style>
    .report-box {
        background-color: #fdfcfb;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #8e735b;
        color: #4a4a4a;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #8e735b;
        color: white;
        height: 4em;
        font-weight: bold;
        border-radius: 8px;
        font-size: 1.2em;
    }
    .roi-stat {
        color: #27ae60;
        font-weight: bold;
        font-size: 1.5em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ PelléCare Digital Consultant")
st.write("LASRA-Tested Science • Professional Leather Stewardship • Made in NZ")
st.write("---")

# --- 1. DIAGNOSTIC INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.header("📋 The Asset Profile")
    leather_type = st.selectbox(
        "Leather Finish Type:",
        ["Finished (Pigmented/Non-Aniline)", "Semi-Aniline", "Pure Aniline (Unsealed)", "Waxed / Oiled Pull-up"]
    )
    asset_value = st.number_input("Original Purchase Value ($):", min_value=100, value=4500, step=100)
    age = st.slider("Age of Leather (Years):", 0, 30, 2)
    condition = st.select_slider("Current Surface State:", options=["Pristine", "Slightly Dry", "Aged/Scratched", "Crisis"])

with col2:
    st.header("☀️ Environmental Stressors")
    sunlight = st.select_slider("Direct UV Exposure:", options=["None", "Moderate", "High (North Facing)"])
    heat = st.checkbox("Near Heat Source (Fire/Heat Pump)")
    traffic = st.radio("Usage Level:", ["Low (Formal)", "Moderate (Daily)", "High (Pets/Kids/Commercial)"])

# --- 2. LOGIC ENGINE ---
if st.button("🚀 EXECUTE DIAGNOSTIC & ROI PROJECTION"):
    warnings = []
    
    # Product Selection Logic
    if leather_type in ["Finished (Pigmented/Non-Aniline)", "Semi-Aniline"]:
        if condition == "Pristine" and age < 3:
            kit = "Supreme Leather Dual Kit (Finished)"
            agent = "Conditioner & Protector"
            kit_price = 50.00
        else:
            kit = "Master Kit (Semi-Aniline/Finished)"
            agent = "Revitaliser"
            kit_price = 65.00
            warnings.append("⚠️ Older/Finished leathers require Revitaliser to rejuvenate the base fibers.")
    else: # Aniline or Wax/Oil
        kit = "Supreme Leather Dual Kit (Wax/Oil)"
        agent = "Revitaliser"
        kit_price = 60.00
        if leather_type == "Pure Aniline (Unsealed)":
            warnings.append("❌ PRO TIP: Never use heavy waxes on pure aniline. Revitaliser only.")

    # Frequency Math
    base_freq = 12
    decline_multiplier = 1.0
    
    if sunlight == "High (North Facing)": 
        base_freq -= 4
        decline_multiplier += 0.5
    if heat: 
        base_freq -= 2
        decline_multiplier += 0.3
    if traffic == "High (Pets/Kids/Commercial)": 
        base_freq -= 2
        decline_multiplier += 0.2

    # --- 3. ROI & PROJECTION MATH ---
    years = np.arange(0, 11)
    # Scenario: No Care (Degrades to 20% integrity by Year 7-10)
    health_no_care = 100 * np.exp(-0.15 * decline_multiplier * years)
    # Scenario: Pellé Care (Maintains ~90% integrity)
    health_pelle = 100 * np.exp(-0.02 * years)

    # ROI Math
    depreciation_no_care = asset_value / 7 # Asset dies in 7 years
    depreciation_pelle = asset_value / 25 # Asset lasts 25+ years
    annual_savings = depreciation_no_care - (depreciation_pelle + kit_price)

    # --- 4. DISPLAY RESULTS ---
    res_col1, res_col2 = st.columns([3, 2])

    with res_col1:
        st.markdown(f"""
        <div class="report-box">
            <h3>🔬 Prescribed Care Ritual</h3>
            <p><b>Recommended System:</b> {kit}</p>
            <p><b>Primary Agent:</b> Pellé {agent}</p>
            <p><b>Application Interval:</b> Every {max(4, base_freq)} weeks</p>
            <hr>
            <p><i>The Pellé system is proven to reduce wear by up to 500% when compared to untreated leather.</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(years, health_pelle, color='#8e735b', linewidth=4, label="The Pellé Ritual")
        ax.plot(years, health_no_care, color='#cccccc', linestyle='--', linewidth=2, label="No Maintenance")
        ax.fill_between(years, health_pelle, health_no_care, color='#8e735b', alpha=0.1)
        ax.set_title("Fiber Integrity Over 10 Years")
        ax.set_ylabel("Structural Health (%)")
        ax.set_xlabel("Years")
        ax.legend()
        st.pyplot(fig)

    with res_col2:
        st.subheader("💰 Financial Return")
        st.markdown(f"""
        <div class="report-box" style="border-left-color: #27ae60;">
            <p>Annual Depreciation Cost (No Care):<br><b>${depreciation_no_care:.2f}</b></p>
            <p>Annual Depreciation Cost (Pellé):<br><b>${depreciation_pelle:.2f}</b></p>
            <hr>
            <p>Estimated Annual Wealth Retention:</p>
            <span class="roi-stat">${annual_savings:.2f} per year</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Consultant Notes")
        for w in warnings:
            st.warning(w)
        st.info("Step 1: Deep clean with Pellé Leather Cleaner.\n\nStep 2: Apply protection/revitaliser to restore pH balance and moisture.")
