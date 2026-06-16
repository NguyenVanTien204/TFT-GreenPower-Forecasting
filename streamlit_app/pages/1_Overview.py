import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))
from src.data_loader import load_and_preprocess_data

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

st.title("📊 Dataset Overview")

# Load data
@st.cache_data
def get_data():
    return load_and_preprocess_data()

try:
    with st.spinner("Loading data..."):
        df = get_data()
        
    st.success("Data loaded successfully!")
    
    # Dataset statistics
    st.subheader("Vietnam Energy Generation (2019-2024)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Months", len(df['date'].unique()))
    col2.metric("Energy Sources", len(df['series'].unique()))
    col3.metric("Total Generation", f"{df['generation_TWh'].sum():.2f} TWh")
    
    # Plot historical data
    st.subheader("Historical Generation by Source")
    fig = px.line(df, x="date", y="generation_TWh", color="series", 
                  title="Monthly Electricity Generation in Vietnam",
                  labels={"generation_TWh": "Generation (TWh)", "date": "Date"},
                  color_discrete_map={
                      "Coal": "#607D8B",
                      "Gas": "#FF7043",
                      "Hydro": "#29B6F6",
                      "Solar": "#FDD835",
                      "Wind": "#66BB6A"
                  })
    fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data table
    st.subheader("Raw Data Preview")
    st.dataframe(df[['date', 'entity', 'series', 'generation_TWh', 'temperature', 'solar', 'precipitation']].head(100))

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Make sure the path to the dataset is correct.")
