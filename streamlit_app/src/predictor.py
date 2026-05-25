import pandas as pd
import streamlit as st
import torch

@st.cache_data
def run_inference(_model, _validation_dataset, _df):
    """
    Run prediction on the validation dataset and format the output.
    """
    val_dataloader = _validation_dataset.to_dataloader(train=False, batch_size=32, num_workers=0)
    
    # Run prediction
    predictions = _model.predict(val_dataloader, mode="quantiles", return_x=True)
    
    quantiles = predictions.output
    x = predictions.x
    
    # Decode target series and entities
    # index maps batch index to entity and series
    decoded_idx = _validation_dataset.x_to_index(x)
    
    results = []
    
    for i in range(len(decoded_idx)):
        entity = decoded_idx.iloc[i]['entity']
        series = decoded_idx.iloc[i]['series']
        time_idx_start = int(x['decoder_time_idx'][i][0].item())
        
        # Predicted quantiles for the next 6 months
        pred_quantiles = quantiles[i].numpy() # Shape (6, 5) assuming max_prediction_length=6 and 5 quantiles
        
        for step in range(pred_quantiles.shape[0]):
            current_time_idx = time_idx_start + step
            
            # Find the actual date and value
            actual_row = _df[(_df['entity'] == entity) & (_df['series'] == series) & (_df['time_idx'] == current_time_idx)]
            
            if not actual_row.empty:
                date = actual_row['date'].iloc[0]
                actual = actual_row['generation_TWh'].iloc[0]
            else:
                date = None
                actual = None
                
            q10, q25, q50, q75, q90 = pred_quantiles[step]
            
            results.append({
                'entity': entity,
                'series': series,
                'time_idx': current_time_idx,
                'date': date,
                'actual': actual,
                'q10': q10,
                'q25': q25,
                'pred_q50': q50,
                'q75': q75,
                'q90': q90
            })
            
    res_df = pd.DataFrame(results)
    
    # Calculate historical data for plotting context
    history_df = _df[['entity', 'series', 'time_idx', 'date', 'generation_TWh']].copy()
    history_df = history_df.rename(columns={'generation_TWh': 'actual'})
    
    return res_df, history_df
