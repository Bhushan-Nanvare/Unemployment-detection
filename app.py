import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie

# =========================
# Page Config & Custom CSS
# =========================
st.set_page_config(
    page_title="Labor Market Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI - Custom CSS
st.markdown("""
<style>
    /* Global Font & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Card Styling */
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #4F8BF9;
        margin-bottom: 10px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1E293B;
        font-weight: 700;
    }
    
    /* Timeline Styling */
    .timeline-item {
        padding: 15px;
        border-left: 2px solid #E2E8F0;
        margin-left: 10px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 20px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #3B82F6;
    }
    .timeline-year {
        font-weight: bold;
        color: #3B82F6;
    }
    
    /* Custom Badge */
    .badge {
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-high { background-color: #FEE2E2; color: #991B1B; }
    .badge-medium { background-color: #FEF3C7; color: #92400E; }
    .badge-low { background-color: #D1FAE5; color: #065F46; }

</style>
""", unsafe_allow_html=True)

# Helper: Load Lottie Animation
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Animations
lottie_analytics = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
lottie_robot = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_sweb47f4.json")
lottie_warning = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_Tkwjw8.json")

API_URL = "http://127.0.0.1:8000/simulate"

# =========================
# Header Section
# =========================
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🧠 Labor Market Intelligence Platform")
    st.markdown("""
    **Next-Gen Scenario Analysis & Decision Support System**  
    *Model economic shocks, predict sector resilience, and generate policy insights using rule-based AI.*
    """)
with col_head2:
    if lottie_analytics:
        st_lottie(lottie_analytics, height=150, key="header_anim")

st.divider()

# =========================
# Sidebar Controls
# =========================
with st.sidebar:
    st.header("⚙️ Simulation Controls")
    
    # Global Settings
    forecast_horizon = st.slider("Forecast Horizon (Years)", 3, 10, 6)
    
    st.markdown("---")
    
    def scenario_controls(label, preset_index):
        st.subheader(f"📌 {label}")
        
        SCENARIO_PRESETS = [
            "Baseline (Natural Flow)", "Severe Shock", "Mild Shock", "Policy Support", 
            "COVID-like Shock (2020)", "Global Recession"
        ]
        
        preset = st.selectbox(f"Select Preset", SCENARIO_PRESETS, index=preset_index, key=f"{label}_preset")
        
        # Preset Logic
        if preset == "Baseline (Natural Flow)": si, sd, rr = 0.0, 0, 0.5
        elif preset == "Severe Shock": si, sd, rr = 0.35, 2, 0.20
        elif preset == "Mild Shock": si, sd, rr = 0.15, 1, 0.40
        elif preset == "Policy Support": si, sd, rr = 0.35, 2, 0.45
        elif preset == "COVID-like Shock (2020)": si, sd, rr = 0.40, 3, 0.30
        else: si, sd, rr = 0.25, 2, 0.25
        
        with st.expander("Advanced Parameters", expanded=False):
            shock_intensity = st.slider(f"Shock Intensity", 0.0, 0.6, si, 0.05, key=f"{label}_si")
            shock_duration = st.slider(f"Duration (Years)", 1, 4, sd, key=f"{label}_sd")
            recovery_rate = st.slider(f"Recovery Rate", 0.1, 0.6, rr, 0.05, key=f"{label}_rr")
        
        POLICY_OPTIONS = ["None", "Youth Employment Boost", "SME Support Package", "Rural Job Guarantee"]
        policy_name = st.selectbox(f"Apply Policy", POLICY_OPTIONS, index=0, key=f"{label}_policy")
        
        return shock_intensity, shock_duration, recovery_rate, policy_name

    si_a, sd_a, rr_a, policy_a = scenario_controls("Scenario A", 0)
    st.markdown("---")
    si_b, sd_b, rr_b, policy_b = scenario_controls("Scenario B", 1)
    
    st.markdown("### ℹ️ About")
    st.info("This system uses a structural labor market model with rule-based AI for prescriptive analytics.")

# =========================
# Main Execution
# =========================

# Helper to fetch data
def fetch_scenario(si, sd, rr, pol):
    payload = {
        "shock_intensity": si,
        "shock_duration": sd,
        "recovery_rate": rr,
        "forecast_horizon": forecast_horizon,
        "policy_name": pol if pol != "None" else None,
    }
    res = requests.post(API_URL, json=payload)
    res.raise_for_status()
    return res.json()

def fetch_baseline():
    return fetch_scenario(0.0, 0, 0.0, "None")

# Run Simulation
try:
    with st.spinner("Running Advanced Simulation Models..."):
        baseline_data = fetch_baseline()
        scen_a_data = fetch_scenario(si_a, sd_a, rr_a, policy_a)
        scen_b_data = fetch_scenario(si_b, sd_b, rr_b, policy_b)

    # DataFrames
    baseline_df = pd.DataFrame(baseline_data["baseline"])
    scen_a_df = pd.DataFrame(scen_a_data["scenario"])
    scen_b_df = pd.DataFrame(scen_b_data["scenario"])
    
    # Indices
    idx_a = scen_a_data.get("indices", {})
    idx_b = scen_b_data.get("indices", {})

    # =========================
    # 1. Top-Level Metrics (Modern Cards)
    # =========================
    st.markdown("### 📊 Executive Summary")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size:1rem; color:#64748B;">📉 Baseline (Natural)</h3>
            <h2 style="margin:0; font-size:2rem; color:#1E293B;">{round(baseline_df['Predicted_Unemployment'].max(), 2)}%</h2>
            <p style="margin:0; font-size:0.8rem; color:#64748B;">Peak in {baseline_df.loc[baseline_df['Predicted_Unemployment'].idxmax(), 'Year']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        delta_a = round(scen_a_df['Scenario_Unemployment'].max() - baseline_df['Predicted_Unemployment'].max(), 2)
        st.metric("Scenario A Peak", f"{round(scen_a_df['Scenario_Unemployment'].max(), 2)}%", delta=f"{delta_a}%", delta_color="inverse")
    with col_m3:
        delta_b = round(scen_b_df['Scenario_Unemployment'].max() - baseline_df['Predicted_Unemployment'].max(), 2)
        st.metric("Scenario B Peak", f"{round(scen_b_df['Scenario_Unemployment'].max(), 2)}%", delta=f"{delta_b}%", delta_color="inverse")
    with col_m4:
        st.metric("Forecast Horizon", f"{forecast_horizon} Years")

    # =========================
    # 2. Interactive Comparison Chart (Plotly)
    # =========================
    st.markdown("### 📈 Scenario Trajectory Comparison")
    
    # Combined Plot with Plotly
    fig_main = go.Figure()
    
    # Baseline (Natural Flow)
    fig_main.add_trace(go.Scatter(
        x=baseline_df['Year'], 
        y=baseline_df['Predicted_Unemployment'],
        mode='lines',
        name='Baseline (Natural Flow)',
        line=dict(color='#94A3B8', width=3, dash='dash')
    ))
    
    # Scenario A
    fig_main.add_trace(go.Scatter(
        x=scen_a_df['Year'], 
        y=scen_a_df['Scenario_Unemployment'],
        mode='lines+markers',
        name='Scenario A',
        line=dict(color='#3B82F6', width=4)
    ))
    
    # Scenario B
    fig_main.add_trace(go.Scatter(
        x=scen_b_df['Year'], 
        y=scen_b_df['Scenario_Unemployment'],
        mode='lines+markers',
        name='Scenario B',
        line=dict(color='#EF4444', width=4)
    ))
    
    fig_main.update_layout(
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    st.plotly_chart(fig_main, use_container_width=True)

    # =========================
    # 3. Deep Dive Tabs
    # =========================
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 Sector Heatmap", "🤖 AI Advisor", "⚠️ Risk Analysis", "📅 Story Mode", "💰 Budget & ROI"])

    # --- TAB 1: Sector Heatmap ---
    with tab1:
        st.markdown("#### Relative Sector Stress Index (RSSI)")
        st.write("Identifies which sectors are most vulnerable to the simulated economic shock.")
        
        col_h1, col_h2 = st.columns(2)
        
        def plot_heatmap(data, title):
            if "sector_impact" in data:
                df = pd.DataFrame(data["sector_impact"])
                fig = px.bar(df, x="Sector", y="Stress_Score", color="Stress_Score",
                             color_continuous_scale="Reds", title=title,
                             text="Resilience_Badge",
                             hover_data=["Resilience_Score"])
                fig.update_layout(template="plotly_white")
                return fig
            return None

        with col_h1:
            st.plotly_chart(plot_heatmap(scen_a_data, "Scenario A: Sector Stress"), use_container_width=True)
        with col_h2:
            st.plotly_chart(plot_heatmap(scen_b_data, "Scenario B: Sector Stress"), use_container_width=True)

    # --- TAB 2: AI Advisor ---
    with tab2:
        col_ai_l, col_ai_r = st.columns([1, 3])
        with col_ai_l:
            if lottie_robot:
                st_lottie(lottie_robot, height=200)
        
        with col_ai_r:
            st.markdown("#### 🧠 AI Career & Policy Intelligence")
            st.info("Rule-based AI analyzes sector shifts to recommend skills and policy interventions.")
            
            with st.expander("Scenario A: Strategic Advice", expanded=True):
                if "career_advice" in scen_a_data:
                    adv = scen_a_data["career_advice"]
                    st.write(f"**Insight:** {adv['narrative']}")
                    st.markdown(f"**🚀 Growth Areas:** `{', '.join(adv['growth_sectors'])}`")
                    st.markdown(f"**💎 Key Skills:** `{', '.join(adv['recommended_skills'])}`")
            
            with st.expander("Scenario B: Strategic Advice", expanded=False):
                if "career_advice" in scen_b_data:
                    adv = scen_b_data["career_advice"]
                    st.write(f"**Insight:** {adv['narrative']}")
                    st.markdown(f"**🚀 Growth Areas:** `{', '.join(adv['growth_sectors'])}`")

    # --- TAB 3: Risk Analysis ---
    with tab3:
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.subheader("Scenario A Risk Profile")
            st.metric("Recovery Quality Index (RQI)", idx_a.get("rqi_label", "N/A"))
            st.metric("Early Warning Signal", idx_a.get("early_warning", "N/A"))
            
            # Sensitivity Tool
            st.markdown("##### 🎛️ Sensitivity Check")
            sens_val = st.slider("Test Recovery Rate (+/- 10%)", -0.1, 0.1, 0.0, 0.01, key="sens_a")
            
            # Recalculate if sensitivity is applied
            if sens_val != 0:
                st.caption(f"Re-simulating with adjustment: {sens_val:+}")
                with st.spinner("Updating Scenario A..."):
                    scen_a_data = fetch_scenario(si_a, sd_a, rr_a + sens_val, policy_a)
                    # Update indices for display
                    idx_a = scen_a_data.get("indices", {})
                    # Update RQI display
                    st.metric("New RQI", idx_a.get("rqi_label", "N/A"))

        
        with col_r2:
            st.subheader("Scenario B Risk Profile")
            st.metric("Recovery Quality Index (RQI)", idx_b.get("rqi_label", "N/A"))
            st.metric("Early Warning Signal", idx_b.get("early_warning", "N/A"))

    # --- TAB 4: Story Mode ---
    with tab4:
        st.markdown("#### 📅 Year-by-Year Economic Narrative")
        
        col_s1, col_s2 = st.columns(2)
        
        def render_story(data, name):
            st.subheader(name)
            if "story" in data:
                for event in data["story"]:
                    # Modern Timeline HTML
                    st.markdown(f"""
                    <div class="timeline-item">
                        <div class="timeline-year">{event['year']} {event['icon']}</div>
                        <div>{event['description']}</div>
                        <div style="font-size: 0.8rem; color: #64748B;">Unemployment: {event['value']}%</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No story data.")

        with col_s1:
            render_story(scen_a_data, "Scenario A Timeline")
        with col_s2:
            render_story(scen_b_data, "Scenario B Timeline")

    # --- TAB 5: Budget & ROI ---
    with tab5:
        st.markdown("#### 💰 Policy Budget & Impact Estimator")
        st.info("Hypothetical cost-benefit analysis for decision support.")
        
        col_b1, col_b2 = st.columns(2)
        
        def calculate_roi(scenario_data, policy_name):
            # Mock Logic for Budget
            base_cost = 0
            if policy_name == "Youth Employment Boost": base_cost = 5000 # Cr
            elif policy_name == "SME Support Package": base_cost = 12000
            elif policy_name == "Rural Job Guarantee": base_cost = 15000
            
            # Cost scales with shock intensity
            shock_factor = 1.0 + (scenario_data["indices"].get("shock_intensity", 0.0) * 2)
            estimated_cost = base_cost * shock_factor
            
            # Benefit: "Jobs Saved" (Mock: Delta in peak unemployment * 500M labor force / 100)
            # This is a rough proxy
            unemp_delta = max(0, baseline_df['Predicted_Unemployment'].max() - pd.DataFrame(scenario_data["scenario"])['Scenario_Unemployment'].max())
            jobs_saved = (unemp_delta / 100) * 500000000 # 500 Million Labor Force
            
            return estimated_cost, jobs_saved

        with col_b1:
            st.subheader("Scenario A Investment")
            if policy_a != "None":
                cost_a, jobs_a = calculate_roi(scen_a_data, policy_a)
                st.metric("Estimated Budget", f"₹{cost_a:,.0f} Cr")
                st.metric("Potential Jobs Saved", f"{jobs_a:,.0f}")
                if cost_a > 0 and jobs_a > 0:
                    st.metric("Cost per Job Saved", f"₹{cost_a*10000000/jobs_a:,.0f}")
            else:
                st.write("No policy intervention selected.")
                
        with col_b2:
            st.subheader("Scenario B Investment")
            if policy_b != "None":
                cost_b, jobs_b = calculate_roi(scen_b_data, policy_b)
                st.metric("Estimated Budget", f"₹{cost_b:,.0f} Cr")
                st.metric("Potential Jobs Saved", f"{jobs_b:,.0f}")
                if cost_b > 0 and jobs_b > 0:
                    st.metric("Cost per Job Saved", f"₹{cost_b*10000000/jobs_b:,.0f}")
            else:
                st.write("No policy intervention selected.")

except Exception as e:
    st.error(f"⚠️ Simulation Error: {e}")
    st.warning("Ensure the backend API is running: `uvicorn src.api:app --reload`")
    if lottie_warning:
        st_lottie(lottie_warning, height=200)

