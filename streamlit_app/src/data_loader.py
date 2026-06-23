import pandas as pd
import numpy as np
from pathlib import Path

def load_and_preprocess_data():
    """
    Load Vietnam energy dataset and apply preprocessing matching the TFT transfer learning pipeline.
    """
    base_dir = Path("c:/Users/ADMIN/Downloads/MODEL_TFT")
    vn_data_path = base_dir / 'data' / 'processed' / 'VN_data' / 'vn_tft_ready.csv'
    
    if not vn_data_path.exists():
        # Fallback to relative path if running from a different directory
        vn_data_path = Path("data/processed/VN_data/vn_tft_ready.csv")
        
    df = pd.read_csv(vn_data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # 1. Filter series
    fine_tune_series = ['Coal', 'Gas', 'Hydro', 'Solar', 'Wind']
    df = df[df['series'].isin(fine_tune_series)].copy()
    
    # 2. Create prec_zscore
    mu = df.groupby('entity')['precipitation'].transform('mean')
    std = df.groupby('entity')['precipitation'].transform('std').replace(0, 1)
    df['prec_zscore'] = (df['precipitation'] - mu) / std
    
    # 3. Time idx
    df = df.sort_values(['entity', 'series', 'date'])
    df['time_idx'] = df.groupby(['entity', 'series'])['date'].rank(method='dense').astype(int) - 1
    
    # 4. Fill NaNs
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df.groupby(['entity', 'series'])[num_cols].transform(
        lambda x: x.interpolate(method='linear').bfill().ffill()
    )
    
    # 5. Lag economic variables
    economic_vars = [
        'IPI_Value', 'CPI_Value', 'GDP_trillion', 'Oil_Price', 
        'FDI_disbursed', 'gas_price', 'castlecoal_price'
    ]
    for var in economic_vars:
        if var in df.columns:
            df[var] = df.groupby(['entity', 'series'])[var].shift(1)
            
    # Bfill after shift
    existing_eco_vars = [v for v in economic_vars if v in df.columns]
    df[existing_eco_vars] = df.groupby(['entity', 'series'])[existing_eco_vars].transform(lambda x: x.bfill())
    
    # Ensure known/unknown reals match notebook
    df['precip_roll6'] = df.get('prec_roll_3', df['precipitation']) # fallback if prec_roll_3 missing
    
    return df
