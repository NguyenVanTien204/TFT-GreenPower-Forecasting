import streamlit as st
import os

st.set_page_config(
    page_title="TFT Energy Forecasting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for GreenPower theme
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 5px solid #66BB6A;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #66BB6A;
    }
    .metric-label {
        font-size: 16px;
        color: #B0BEC5;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Vietnam Energy Forecasting")
st.subheader("Temporal Fusion Transformer (TFT) with Transfer Learning")

st.markdown("""
Welcome to the Vietnam GreenPower Forecasting Dashboard!

This application uses a fine-tuned Temporal Fusion Transformer (TFT) model to predict monthly electricity generation in Vietnam across 5 different energy sources:
- **Coal**
- **Gas**
- **Hydro**
- **Solar**
- **Wind**

### 👈 Navigation
Please use the sidebar to navigate through the app:
1. **📊 Overview**: Explore the dataset and model configuration.
2. **🔮 Forecast**: Generate interactive predictions and confidence intervals.
""")

st.info("💡 The model was pretrained on global energy data and fine-tuned specifically for Vietnam's energy sector.")
