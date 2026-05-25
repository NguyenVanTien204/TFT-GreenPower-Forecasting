import numpy as np
import pandas as pd

def smape(y_true, y_pred):
    return 2.0 * np.mean(np.abs(y_pred - y_true) / (np.abs(y_pred) + np.abs(y_true) + 1e-8))

def wape(y_true, y_pred):
    return np.sum(np.abs(y_true - y_pred)) / (np.sum(np.abs(y_true)) + 1e-8)

def calculate_metrics(res_df):
    """
    Calculate MAE, RMSE, SMAPE, WAPE from the prediction results.
    """
    metrics = []
    
    # Drop rows where actual is NaN (future predictions without ground truth)
    df_eval = res_df.dropna(subset=['actual']).copy()
    
    if df_eval.empty:
        return pd.DataFrame()
        
    for series in df_eval['series'].unique():
        series_data = df_eval[df_eval['series'] == series]
        
        y_true = series_data['actual'].values
        y_pred = series_data['pred_q50'].values
        
        mae = np.mean(np.abs(y_true - y_pred))
        rmse = np.sqrt(np.mean((y_true - y_pred)**2))
        smap = smape(y_true, y_pred)
        wap = wape(y_true, y_pred)
        
        metrics.append({
            'Series': series,
            'MAE': round(mae, 4),
            'RMSE': round(rmse, 4),
            'SMAPE': round(smap, 4),
            'WAPE': round(wap, 4)
        })
        
    # Overall
    y_true_all = df_eval['actual'].values
    y_pred_all = df_eval['pred_q50'].values
    
    metrics.append({
        'Series': 'Overall',
        'MAE': round(np.mean(np.abs(y_true_all - y_pred_all)), 4),
        'RMSE': round(np.sqrt(np.mean((y_true_all - y_pred_all)**2)), 4),
        'SMAPE': round(smape(y_true_all, y_pred_all), 4),
        'WAPE': round(wape(y_true_all, y_pred_all), 4)
    })
    
    return pd.DataFrame(metrics)
