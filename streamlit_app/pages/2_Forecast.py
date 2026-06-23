import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))
from src.data_loader import load_and_preprocess_data
from src.model_loader import load_model_and_dataset
from src.predictor import run_inference

st.set_page_config(page_title="Forecast", page_icon="🔮", layout="wide")

st.title("🔮 Generation Forecast")

@st.cache_data
def get_data():
    return load_and_preprocess_data()

try:
    with st.spinner("Loading data..."):
        df = get_data()
        
    with st.spinner("Loading Temporal Fusion Transformer model..."):
        model, validation_dataset, cfg = load_model_and_dataset(df)
        
    with st.spinner("Running inference..."):
        res_df, history_df = run_inference(model, validation_dataset, df)
        
    st.success("Inference completed!")
    
    # UI Controls
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Controls")
        selected_series = st.selectbox("Select Energy Source", res_df['series'].unique())
        show_history = st.slider("Historical months to show", min_value=6, max_value=60, value=24)
        
    with col2:
        st.subheader(f"{selected_series} Forecast (Next 6 Months)")
        
        # Filter data for selected series
        series_history = history_df[history_df['series'] == selected_series].sort_values('time_idx')
        series_forecast = res_df[res_df['series'] == selected_series].sort_values('time_idx')
        
        # We need to map time_idx back to dates for the future predictions where actual date might be missing
        last_date = series_history['date'].max()
        last_time_idx = series_history['time_idx'].max()
        
        # Impute missing dates in forecast
        for idx, row in series_forecast.iterrows():
            if pd.isnull(row['date']):
                months_ahead = row['time_idx'] - last_time_idx
                series_forecast.at[idx, 'date'] = last_date + pd.DateOffset(months=months_ahead)
                
        # Limit history
        plot_history = series_history.tail(show_history)
        
        # Color mapping
        colors = {
            "Coal": "#607D8B",
            "Gas": "#FF7043",
            "Hydro": "#29B6F6",
            "Solar": "#FDD835",
            "Wind": "#66BB6A"
        }
        color = colors.get(selected_series, "#FFFFFF")
        
        # Plotly figure
        fig = go.Figure()
        
        # Historical actuals
        fig.add_trace(go.Scatter(
            x=plot_history['date'], 
            y=plot_history['actual'],
            mode='lines+markers',
            name='Historical Actual',
            line=dict(color=color, width=2)
        ))
        
        # Connect last history point to first forecast point for continuity
        if not plot_history.empty and not series_forecast.empty:
            connect_df = pd.concat([plot_history.tail(1), series_forecast.head(1)])
            # We use the actual value for the connection point
            fig.add_trace(go.Scatter(
                x=[plot_history.tail(1)['date'].iloc[0], series_forecast.head(1)['date'].iloc[0]],
                y=[plot_history.tail(1)['actual'].iloc[0], series_forecast.head(1)['pred_q50'].iloc[0]],
                mode='lines',
                line=dict(color=color, width=2, dash='dash'),
                showlegend=False
            ))
            
        # Forecast Median (Q50)
        fig.add_trace(go.Scatter(
            x=series_forecast['date'], 
            y=series_forecast['pred_q50'],
            mode='lines+markers',
            name='Forecast (Median)',
            line=dict(color=color, width=2, dash='dash')
        ))
        
        # Confidence Intervals (Q10-Q90)
        fig.add_trace(go.Scatter(
            x=list(series_forecast['date']) + list(series_forecast['date'])[::-1],
            y=list(series_forecast['q90']) + list(series_forecast['q10'])[::-1],
            fill='toself',
            fillcolor=color.replace(')', ', 0.2)').replace('rgb', 'rgba') if 'rgb' in color else f"rgba(102, 187, 106, 0.2)",
            line=dict(color='rgba(255,255,255,0)'),
            name='80% Confidence Interval (Q10-Q90)',
            hoverinfo="skip"
        ))
        
        # Confidence Intervals (Q25-Q75)
        fig.add_trace(go.Scatter(
            x=list(series_forecast['date']) + list(series_forecast['date'])[::-1],
            y=list(series_forecast['q75']) + list(series_forecast['q25'])[::-1],
            fill='toself',
            fillcolor=color.replace(')', ', 0.3)').replace('rgb', 'rgba') if 'rgb' in color else f"rgba(102, 187, 106, 0.4)",
            line=dict(color='rgba(255,255,255,0)'),
            name='50% Confidence Interval (Q25-Q75)',
            hoverinfo="skip"
        ))
        
        # If there are actuals in the forecast period (for validation)
        forecast_with_actuals = series_forecast.dropna(subset=['actual'])
        if not forecast_with_actuals.empty:
            fig.add_trace(go.Scatter(
                x=forecast_with_actuals['date'], 
                y=forecast_with_actuals['actual'],
                mode='markers',
                name='True Value (Validation)',
                marker=dict(color='#EF5350', size=8, symbol='x')
            ))
            
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified",
            xaxis_title="Date",
            yaxis_title="Generation (TWh)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data Table
        st.subheader("Forecast Values")
        display_df = series_forecast[['date', 'actual', 'q10', 'q25', 'pred_q50', 'q75', 'q90']].copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m')
        display_df = display_df.rename(columns={
            'date': 'Month',
            'actual': 'Actual (TWh)',
            'q10': 'P10',
            'q25': 'P25',
            'pred_q50': 'Median Forecast',
            'q75': 'P75',
            'q90': 'P90'
        })
        st.dataframe(display_df.style.format(formatter={col: "{:.3f}" for col in display_df.columns if col != 'Month'}))

except Exception as e:
    st.error(f"Error during forecasting: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
