# TFT v3 — Summary Tables

Date: 2026-05-09

This file contains three tables for inclusion in a scientific report: (1) list of countries used in the multi-country pretraining dataset; (2) full parameter table for the pre-trained TFT v3; (3) full parameter table for the VN fine-tuned TFT v3.

---

## 1) Countries (training set)

Source: [data/processed/tft_premodel_dataset_20.csv](data/processed/tft_premodel_dataset_20.csv#L1)

| Country |
|---|
| Australia |
| Austria |
| Chile |
| Colombia |
| Czechia |
| France |
| Germany |
| Kazakhstan |
| Malaysia |
| Pakistan |
| Philippines |
| Poland |
| Serbia |
| South Africa |
| Spain |
| Sweden |
| Taiwan |
| Turkey |
| Ukraine |
| Viet Nam |

---

## 2) TFT v3 (pre-training) — Parameters

Source: [checkpoint/tft_v3_config.json](checkpoint/tft_v3_config.json#L1)

| Parameter | Value |
|---|---|
| version | tft_v3 |
| best_ckpt | D:\\WorkSpace\\Study\\NCKH\\checkpoint\\tft_v3_best.ckpt |
| best_val_loss | 0.20404371619224548 |
| stopped_epoch | 21 |
| max_encoder_length | 24 |
| max_prediction_length | 6 |
| target | generation_TWh |
| group_ids | ["entity", "series"] |
| target_normalizer | GroupNormalizer(softplus, groups=[entity,series]) |
| hidden_size | 128 |
| attention_head_size | 4 |
| dropout | 0.15 |
| hidden_continuous_size | 32 |
| lstm_layers | 2 |
| loss_quantiles | [0.1, 0.25, 0.5, 0.75, 0.9] |
| optimizer | adamw |
| train_entities | Australia, Austria, Chile, Colombia, Czechia, France, Germany, Kazakhstan, Malaysia, Pakistan, Philippines, Poland, Serbia, South Africa, Spain, Sweden, Taiwan, Turkey, Ukraine, Viet Nam |
| train_series | Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind |
| train_date_range | [2018-01-01, 2025-12-01] |
| static_categoricals | ["entity"] |
| time_varying_known_reals | time_idx, month, month_sin, month_cos, quarter, year |
| time_varying_unknown_reals | generation_TWh, temperature, solar, humidity, precipitation |

---

## 3) TFT VN v3 (fine-tune) — Parameters

Source: [checkpoint/tft_vn_v3_config.json](checkpoint/tft_vn_v3_config.json#L1)

| Parameter | Value |
|---|---|
| version | tft_vn_v3 |
| pretrained_from | checkpoint\\tft_v3_best.ckpt |
| best_ckpt | checkpoint\\tft_vn_v3_best.ckpt |
| best_val_loss | 0.517829179763794 |
| phase1_val_loss | 0.49076229333877563 |
| fine_tune_series | Coal, Gas, Hydro, Solar, Wind |
| max_encoder_length | 18 |
| max_prediction_length | 6 |
| target | generation_TWh |
| group_ids | ["entity", "series"] |
| target_normalizer | GroupNormalizer(softplus) |
| hidden_size | 128 |
| phase1_lr | 0.001 |
| phase2_lr | 1e-05 |
| static_categoricals | ["entity"] |
| time_varying_known_reals | time_idx, month, year |
| time_varying_unknown_reals | temperature, solar, humidity, precipitation, prec_zscore, precip_roll6, IPI_Value, CPI_Value, GDP_trillion, Oil_Price, FDI_disbursed, gas_price, castlecoal_price |

---

If you want these exported additionally as CSV or LaTeX tables for direct inclusion in your manuscript, tell me which format and I'll produce them.
