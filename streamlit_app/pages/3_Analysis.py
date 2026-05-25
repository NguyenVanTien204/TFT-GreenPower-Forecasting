import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))
from src.data_loader import load_and_preprocess_data
from src.model_loader import load_model_and_dataset
from src.predictor import run_inference
from src.metrics import calculate_metrics

st.set_page_config(page_title="Model Analysis", page_icon="📈", layout="wide")

st.title("📈 Model Analysis & Evaluation")

def get_data_and_inference():
    df = load_and_preprocess_data()
    model, validation_dataset, cfg = load_model_and_dataset(df)
    res_df, _ = run_inference(model, validation_dataset, df)
    return res_df, model, validation_dataset, cfg

try:
    with st.spinner("Calculating metrics..."):
        res_df, model, validation_dataset, cfg = get_data_and_inference()
        metrics_df = calculate_metrics(res_df)
        
    st.success("Evaluation completed!")
    
    st.markdown("### Performance Metrics (Validation Set)")
    st.markdown("The following metrics are calculated on the validation set (last 12 months).")
    
    # Display metrics table
    st.dataframe(metrics_df.style.highlight_min(subset=['MAE', 'RMSE', 'SMAPE', 'WAPE'], color='#2E7D32'))
    
    # Bar chart for WAPE and SMAPE
    st.markdown("### Error Metrics by Energy Source")
    
    # Filter out 'Overall' for the chart
    chart_df = metrics_df[metrics_df['Series'] != 'Overall']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_smape = px.bar(chart_df, x='Series', y='SMAPE', text='SMAPE',
                           title="SMAPE by Source (Lower is better)",
                           color='Series',
                           color_discrete_map={
                               "Coal": "#607D8B",
                               "Gas": "#FF7043",
                               "Hydro": "#29B6F6",
                               "Solar": "#FDD835",
                               "Wind": "#66BB6A"
                           })
        fig_smape.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig_smape.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        st.plotly_chart(fig_smape, use_container_width=True)
        
    with col2:
        fig_wape = px.bar(chart_df, x='Series', y='WAPE', text='WAPE',
                          title="WAPE by Source (Lower is better)",
                          color='Series',
                          color_discrete_map={
                              "Coal": "#607D8B",
                              "Gas": "#FF7043",
                              "Hydro": "#29B6F6",
                              "Solar": "#FDD835",
                              "Wind": "#66BB6A"
                          })
        fig_wape.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig_wape.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        st.plotly_chart(fig_wape, use_container_width=True)
        
    st.markdown("### TFT Architecture Details")
    st.info("The Temporal Fusion Transformer intrinsically selects the most relevant variables for prediction.")
    
    st.json({
        "Max Encoder Length": cfg['max_encoder_length'],
        "Max Prediction Length": cfg['max_prediction_length'],
        "Hidden Size": cfg['hidden_size'],
        "Phase 1 LR": cfg['phase1_lr'],
        "Phase 2 LR": cfg['phase2_lr']
    })

except Exception as e:
    st.error(f"Error during evaluation: {str(e)}")
