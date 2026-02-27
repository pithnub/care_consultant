import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- INITIAL SETUP ---
st.set_page_config(page_title="PelleCare: Digital Care Consultant", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .report-box {
        background-color: #fdfcfb;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #8e735b;
        color: #4a4a4a;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%;
        background-color: #8e735b;
        color: white;
        height: 3.5em;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ PelléCare Digital Care Consultant")
st.write("---")

# --- INPUT SECTION: THE DIAGNOSTIC ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. The Asset")
    leather_type = st.selectbox(
        "Leather Finish Type:",
        ["Finished (Pigmented/Sealed)", "Semi-Aniline", "Pure Aniline (Unsealed)", "Waxed / Oiled Pull-up"]
    )
    age = st.slider("Age of Leather (Years):", 0, 30, 2)
    current_state = st.radio("Current Condition:", ["Pristine", "Slightly Dry", "Scratched/Faded", "Heavily Soiled"])

with col2:
    st.header("2. The Environment")
    sunlight = st.select_slider("Direct Sunlight Exposure:", options=["None", "Low", "Moderate", "High (North Facing)"])
    heat_source = st.checkbox("Near Heat Source? (Fireplace/Heat Pump)")
    household = st.multiselect("Active Environment Variables:", ["Pets", "Young Children", "High Traffic / Commercial"])
    care_adherence = st.radio("Current Care Habit:", ["Reactive (Only when dirty)", "Occasional", "None"])

# --- THE LOGIC ENGINE ---
if st.button("🚀 EXECUTE DIAGNOSTIC & PROJECTION"):
    warnings = []
    
    # 1. Product Logic
    if leather_type in ["Finished (Pigmented/Sealed)", "Semi-Aniline"]:
        if age < 5 and current_state != "Scratched/Faded":
            agent = "Pellé Leather Conditioner & Protector"
            kit_suggestion = "Supreme Leather Dual Kit (Finished)"
        else:
            agent = "Pellé Leather Revitaliser"
            warnings.append("⚠️ Older/Worn finish requires Revitaliser to penetrate deeply.")
            kit_suggestion = "Master Kit (Semi-Aniline)"
    else:
        agent = "Pellé Leather Revitaliser"
        kit_suggestion = "Supreme Leather Dual Kit (Wax/Oil)"
        if leather_type == "Pure Aniline (Unsealed)":
            warnings.append("❌ CRITICAL: Avoid standard conditioners; use Revitaliser only.")

    # 2. Frequency & Graph Logic
    base_freq = 12
    decline_rate = 10 # Base decline
    
    # Environment Penalties
    if sunlight in ["Moderate", "High (North Facing)"]:
        base_freq -= 4
        decline_rate += 15
        warnings.append("☀️ UV Alert: High exposure accelerates pigment fading.")
    if heat_source:
        base_freq -= 2
        decline_rate += 10
        warnings.append("🔥 Heat Alert: Nearby heat leaches essential moisture.")
    if household:
        base_freq -= 2
        decline_rate += 5

    # 3. Projection Graph Data
    years = np.arange(0, 6)
    # Scenario A: Current Habit
    current_habit_boost = {"Reactive (Only when dirty)": 5, "Occasional": 10, "None": 0}[care_adherence]
    health_current = np.clip(100 - (years * (decline_rate - current_habit_boost)), 0, 100)
    
    # Scenario B: PelleCare Ritual
    health_pelle = np.clip(100 - (years * (decline_rate - 25)), 0, 100)

    # --- RESULTS DISPLAY ---
    c_left, c_right = st.columns([3, 2])
    
    with c_left:
        st.markdown(f"""
        <div class="report-box">
            <h3>📋 YOUR PERSONAL CARE RITUAL</h3>
            <p><strong>Recommended Agent:</strong> {agent}</p>
            <p><strong>Application Cycle:</strong> Every {max(4, base_freq)} weeks.</p>
            <p><strong>Prescribed Kit:</strong> {kit_suggestion}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Plotting the graph
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(years, health_pelle, color='#8e735b', linewidth=3, label="With PelleCare Ritual", marker='o')
        ax.plot(years, health_current, color='#cccccc', linestyle='--', label="Current Path", marker='x')
        ax.fill_between(years, health_pelle, health_current, color='#8e735b', alpha=0.1)
        ax.set_ylim(0, 110)
        ax.set_ylabel("Leather Integrity (%)")
        ax.set_xlabel("Years")
        ax.legend()
        st.pyplot(fig)

    with c_right:
        st.subheader("Consultant Notes")
        for w in warnings:
            st.write(w)
        st.markdown("---")
        st.info(f"**The Science:** LASRA-tested formulas provide a sacrificial wear layer. By applying {agent} every {max(4, base_freq)} weeks, you prevent the 'cracking point' shown in the graph.")
