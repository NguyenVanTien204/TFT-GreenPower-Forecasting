"""
Cấu hình chung cho dự án ENTSO-E Data
"""
import pandas as pd
import os
import dotenv

dotenv.load_dotenv()


# ENTSO-E API Configuration
API_KEY = os.getenv("API_KEY")

# Khoảng thời gian lấy dữ liệu
START = pd.Timestamp("2024-01-01", tz="UTC")
END = pd.Timestamp("2024-12-31", tz="UTC")

# Quốc gia / Bidding zone
COUNTRY_CODE = "DE_LU"  # Germany (Germany-Luxembourg bidding zone)

# Power System Resource (PSR) codes – ENTSO-E standard
PSR_TYPES = {
    "biomass": "B01",
    "fossil_gas": "B04",
    "fossil_hard_coal": "B05",
    "geothermal": "B09",

    "hydro_pumped_storage": "B10",
    "hydro_run_of_river": "B11",
    "hydro_reservoir": "B12",

    "marine": "B13",
    "nuclear": "B14",
    "other_renewable": "B15",

    "solar": "B16",
    "wind_offshore": "B18",
    "wind_onshore": "B19",

    "other": "B20"
}

RENEWABLE_PSR = {
    "solar": "B16",
    "wind_onshore": "B19",
    "wind_offshore": "B18",
    "hydro_run_of_river": "B11",
    "hydro_reservoir": "B12",
    "biomass": "B01"
}
FORECAST_PSR = {
    "solar": "B16",
    "wind_onshore": "B19",
    "wind_offshore": "B18"
}

# Countries with reliable wind/solar forecast
FORECAST_SUPPORTED_ZONES = [
    "DE_LU", "NL", "DK_1", "DK_2",
    "FR", "GB", "ES", "IT", "SE_3", "SE_4"
]

# Danh sách các quốc gia được hỗ trợ với dữ liệu đầy đủ
# Xem chi tiết trong DATA_AVAILABILITY.md
SUPPORTED_COUNTRIES = [
    # Western Europe (Full data from 2015)
    "DE_LU",  # Germany-Luxembourg
    "FR",     # France
    "NL",     # Netherlands
    "BE",     # Belgium
    "GB",     # Great Britain
    "CH",     # Switzerland
    "AT",     # Austria (separate from 2018)

    # Nordic Countries (Full data from 2015)
    "DK_1",   # Denmark West
    "DK_2",   # Denmark East
    "NO_1",   # Norway Zone 1
    "NO_2",   # Norway Zone 2
    "NO_3",   # Norway Zone 3
    "NO_4",   # Norway Zone 4
    "NO_5",   # Norway Zone 5
    "SE_1",   # Sweden Zone 1
    "SE_2",   # Sweden Zone 2
    "SE_3",   # Sweden Zone 3
    "SE_4",   # Sweden Zone 4
    "FI",     # Finland

    # Southern Europe (Good data from 2015)
    "ES",     # Spain
    "PT",     # Portugal
    "IT",     # Italy

    # Central/Eastern Europe (Good data from 2016+)
    "PL",     # Poland
    "CZ",     # Czech Republic
    "SK",     # Slovakia
    "HU",     # Hungary
    "SI",     # Slovenia
    "HR",     # Croatia
    "RO",     # Romania
    "BG",     # Bulgaria
    "GR",     # Greece

    # Baltic States (Good data from 2016+)
    "EE",     # Estonia
    "LV",     # Latvia
    "LT",     # Lithuania
]

# Đường dẫn thư mục cơ sở
BASE_DIR = "entsoe_data"

# Các loại dữ liệu generation (actual) - sử dụng PSR codes
GENERATION_TYPES = {
    "solar": "B16",
    "wind_onshore": "B19",
    "wind_offshore": "B18",
    "hydro_run_of_river": "B11",
    "hydro_reservoir": "B12",
    "hydro_pumped_generation": "B10",
    "biomass": "B01",
}

# Các loại dữ liệu forecast
FORECAST_TYPES = {
    "solar": "Solar",
    "wind": "Wind"
}

# Cấu trúc thư mục dữ liệu
DATA_DIRECTORIES = {
    "generation_actual": os.path.join(BASE_DIR, "generation_actual"),
    "generation_forecast": os.path.join(BASE_DIR, "generation_forecast"),
    "load": os.path.join(BASE_DIR, "load"),
    "capacity": os.path.join(BASE_DIR, "capacity"),
    "prices": os.path.join(BASE_DIR, "prices"),
    "metadata": os.path.join(BASE_DIR, "metadata")
}

# Cấu hình lấy dữ liệu
FETCH_CONFIG = {
    "generation_actual": True,
    "generation_forecast": True,

    "load_actual": True,
    "load_forecast": True,

    "prices_day_ahead": True,

    "installed_capacity": True,

    # rất nặng, bật khi cần
    "unavailability": False,

    # metadata & logging
    "zone_metadata": True,
    "resolution_check": True,
}

DATA_DIRECTORIES = {
    "generation_actual": f"{BASE_DIR}/generation/actual",
    "generation_forecast": f"{BASE_DIR}/generation/forecast",

    "load_actual": f"{BASE_DIR}/load/actual",
    "load_forecast": f"{BASE_DIR}/load/forecast",

    "prices": f"{BASE_DIR}/prices/day_ahead",
    "capacity": f"{BASE_DIR}/capacity",

    "logs": f"{BASE_DIR}/logs",
    "metadata": f"{BASE_DIR}/metadata"
}


