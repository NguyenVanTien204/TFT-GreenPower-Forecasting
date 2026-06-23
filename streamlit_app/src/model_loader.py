import json
import torch
import streamlit as st
from pathlib import Path
from pytorch_forecasting import TimeSeriesDataSet, TemporalFusionTransformer
from pytorch_forecasting.data import GroupNormalizer
from pytorch_forecasting.metrics import QuantileLoss

@st.cache_resource
def load_model_and_dataset(df):
    """
    Load the TFT model and create the TimeSeriesDataSet for Vietnam.
    """
    base_dir = Path("c:/Users/ADMIN/Downloads/MODEL_TFT")
    ckpt_path = base_dir / 'checkpoint' / 'tft_vn_v3_best.ckpt'
    config_path = base_dir / 'checkpoint' / 'tft_vn_v3_config.json'
    
    if not ckpt_path.exists():
        ckpt_path = Path("checkpoint/tft_vn_v3_best.ckpt")
        config_path = Path("checkpoint/tft_vn_v3_config.json")
        
    with open(config_path, 'r') as f:
        cfg = json.load(f)
        
    # PyTorch 2.6 safety
    try:
        torch.serialization.add_safe_globals([GroupNormalizer, QuantileLoss])
    except Exception:
        pass
        
    # Create dataset
    # Filter columns to only those that exist
    static_cats = [c for c in cfg['static_categoricals'] if c in df.columns]
    known_reals = [c for c in cfg['time_varying_known_reals'] if c in df.columns]
    unknown_reals = [c for c in cfg['time_varying_unknown_reals'] if c in df.columns]
    
    # Validation cutoff (last 12 months)
    training_cutoff = int(df['time_idx'].max()) - 12
    
    dataset = TimeSeriesDataSet(
        df[df['time_idx'] <= training_cutoff],
        time_idx='time_idx',
        target=cfg['target'],
        group_ids=cfg['group_ids'],
        min_encoder_length=cfg['max_encoder_length'] // 2,
        max_encoder_length=cfg['max_encoder_length'],
        min_prediction_length=1,
        max_prediction_length=cfg['max_prediction_length'],
        static_categoricals=static_cats,
        static_reals=[],
        time_varying_known_categoricals=['series'],
        time_varying_known_reals=known_reals,
        time_varying_unknown_categoricals=[],
        time_varying_unknown_reals=unknown_reals,
        target_normalizer=GroupNormalizer(
            groups=cfg['group_ids'],
            transformation='softplus',
        ),
        add_relative_time_idx=True,
        add_target_scales=True,
        add_encoder_length=True,
        allow_missing_timesteps=True,
    )
    
    # Create validation dataset which contains all data for prediction
    validation_dataset = TimeSeriesDataSet.from_dataset(
        dataset, df, predict=True, stop_randomization=True
    )
    
    # Load model
    model = TemporalFusionTransformer.load_from_checkpoint(
        ckpt_path,
        map_location=torch.device('cpu') # Use CPU for inference in Streamlit
    )
    
    return model, validation_dataset, cfg
