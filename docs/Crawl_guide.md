# Hướng dẫn sử dụng ENTSO-E Data Crawler

## 📁 Cấu trúc dự án

```
NCKH/
├── config.py              # Cấu hình chung (API key, khoảng thời gian, etc.)
├── utils.py               # Các hàm tiện ích (lưu file, kiểm tra, etc.)
├── data_fetcher.py        # Class DataFetcher - fetch dữ liệu từ API
├── data_manager.py        # Class DataManager - quản lý logic lấy dữ liệu
├── main.py                # File chính - điều khiển quá trình
├── README.md              # File này
├── crawl.py               # File cũ (có thể xóa)
└── entsoe_data/           # Thư mục chứa dữ liệu
    ├── capacity/
    ├── generation_actual/
    ├── generation_forecast/
    ├── load/
    ├── metadata/
    └── prices/
```

## 🚀 Cách sử dụng

### Cấu hình API Key

Trước tiên, bạn cần đặt API key của ENTSO-E vào file `config.py`:

```python
API_KEY = "YOUR_ENTSOE_API_KEY"
```

### 1. Lấy dữ liệu (bỏ qua dữ liệu đã có)

```bash
python main.py
```

**Cách hoạt động:**
- Kiểm tra xem dữ liệu đã tồn tại chưa
- Chỉ lấy dữ liệu còn thiếu
- Giúp tiết kiệm thời gian và API quota

### 2. Lấy lại toàn bộ dữ liệu (buộc tải xuống)

```bash
python main.py --force
```

hoặc

```bash
python main.py -f
```

**Cách hoạt động:**
- Tải xuống lại toàn bộ dữ liệu
- Ghi đè dữ liệu cũ

## ⚙️ Tùy chỉnh cấu hình

Mở file `config.py` để tùy chỉnh:

### Thay đổi khoảng thời gian

```python
START = pd.Timestamp("2018-01-01", tz="UTC")
END = pd.Timestamp("2024-12-31", tz="UTC")
```

### Thay đổi quốc gia / Bidding Zone

```python
COUNTRY_CODE = "DE_LU"  # Germany-Luxembourg
```

**Các quốc gia được hỗ trợ đầy đủ:**

Xem chi tiết trong file `DATA_AVAILABILITY.md` để biết danh sách đầy đủ các country codes,
khoảng thời gian dữ liệu có sẵn, và data quality cho từng quốc gia.

**Một số ví dụ:**
- `DE_LU` - Germany-Luxembourg (từ 2018)
- `FR` - France
- `GB` - Great Britain
- `ES` - Spain
- `IT` - Italy
- `NL` - Netherlands
- `BE` - Belgium
- `NO_1`, `NO_2`, `NO_3`, `NO_4`, `NO_5` - Norway (5 zones)
- `SE_1`, `SE_2`, `SE_3`, `SE_4` - Sweden (4 zones)
- `DK_1`, `DK_2` - Denmark (2 zones)

**Lưu ý về Bidding Zones:**
- Một số bidding zones đã thay đổi theo thời gian
- Ví dụ: `DE_AT_LU` (trước 2018) → `DE_LU` + `AT` (từ 2018)
- Xem thêm trong `DATA_AVAILABILITY.md`

### Bật/tắt các loại dữ liệu

```python
FETCH_CONFIG = {
    "generation_actual": True,      # Lấy dữ liệu actual generation
    "generation_forecast": True,    # Lấy dữ liệu forecast generation
    "load_actual": True,            # Lấy dữ liệu actual load
    "load_forecast": True,          # Lấy dữ liệu forecast load
    "capacity": True,               # Lấy dữ liệu capacity
    "prices": True,                 # Lấy dữ liệu giá electricity
    "metadata": True                # Tạo dữ liệu calendar/metadata
}
```

## 📊 Các loại dữ liệu được hỗ trợ

### Generation - Actual
- Solar
- Wind Onshore
- Wind Offshore
- Hydro (Run-of-river, Reservoir, Pumped Storage Generation)
- Biomass
- Renewable Waste

**API Method**: `query_generation(country_code, start, end, psr_type)` → DataFrame

### Generation - Forecast
- Solar Forecast
- Wind Forecast

**API Method**: `query_wind_and_solar_forecast(country_code, start, end, psr_type)` → DataFrame

### Load
- Total Load Actual
- Total Load Forecast

**API Methods**:
- `query_load(country_code, start, end)` → DataFrame
- `query_load_forecast(country_code, start, end)` → DataFrame

### Capacity
- Installed Generation Capacity (year-based data)
- Unavailable Capacity

**API Methods**:
- `query_installed_generation_capacity(country_code, start, end, psr_type)` → DataFrame
- `query_unavailability_of_generation_units(country_code, start, end, docstatus)` → DataFrame

### Prices
- Day-Ahead Prices (SDAC - Single Day-Ahead Coupling)

**API Method**: `query_day_ahead_prices(country_code, start, end)` → Series

### Metadata
- Calendar (Hour, Day, Month, Year, Day of Week, Is Weekend)

## 🔍 Cách hoạt động

### DataFetcher Class
- Chứa tất cả các hàm fetch dữ liệu từ ENTSO-E API
- Mỗi hàm có error handling riêng
- Trả về dữ liệu hoặc None nếu có lỗi

### DataManager Class
- Quản lý logic lấy dữ liệu
- **Kiểm tra xem dữ liệu đã có chưa** trước khi lấy
- Chỉ lấy dữ liệu còn thiếu (chế độ thông minh)
- Lưu dữ liệu vào các file CSV
- In báo cáo chi tiết kết quả

## 📋 Báo cáo kết quả

Sau khi chạy xong, bạn sẽ thấy báo cáo như sau:

```
==================================================
              FETCH REPORT
==================================================
 generation_actual/solar          [OK] SUCCESS
 generation_actual/wind_onshore   [SKIP] SKIPPED
 generation_actual/hydro_pumped   [FAIL] FAILED
 ...
==================================================
 Total: 8 SUCCESS, 12 SKIPPED, 1 FAILED
==================================================
```

**Ý nghĩa:**
- ✓ **SUCCESS**: Dữ liệu đã được lấy thành công
- ⊘ **SKIPPED**: Dữ liệu đã tồn tại, không cần lấy lại
- ✗ **FAILED**: Có lỗi khi lấy dữ liệu

## 💾 File Naming Convention

**Quan trọng:** Từ phiên bản này, tất cả các file dữ liệu sẽ bao gồm **country code** trong tên:

```
{COUNTRY_CODE}_{data_type}.csv
```

**Ví dụ với COUNTRY_CODE = "DE_LU":**

```
entsoe_data/
├── generation_actual/
│   ├── DE_LU_solar.csv
│   ├── DE_LU_wind_onshore.csv
│   ├── DE_LU_wind_offshore.csv
│   ├── DE_LU_hydro_run_of_river.csv
│   └── ...
├── generation_forecast/
│   ├── DE_LU_solar_forecast.csv
│   └── DE_LU_wind_forecast.csv
├── load/
│   ├── DE_LU_total_load_actual.csv
│   └── DE_LU_total_load_forecast.csv
├── capacity/
│   ├── DE_LU_installed_capacity.csv
│   Data Availability & Country Codes

**📄 Xem file `DATA_AVAILABILITY.md`** để biết:
- Danh sách đầy đủ các country codes và bidding zones
- Khoảng thời gian dữ liệu có sẵn cho từng quốc gia
- Loại dữ liệu có sẵn (Generation, Load, Prices, Forecasts, etc.)
- Data quality và độ phân giải (15min, hourly)
- Lưu ý về bidding zone changes (DE_AT_LU → DE_LU + AT)
- Best practices khi fetch dữ liệu

### └── DE_LU_unavailable_capacity.csv
├── prices/
│   └── DE_LU_day_ahead_price.csv
└── metadata/
    └── calendar.csv  (không có country code vì là metadata chung)
```

**Lợi ích:**
- ✅ **Dễ tổng hợp:** Có thể lưu dữ liệu nhiều quốc gia trong cùng thư mục
- ✅ **Tránh ghi đè:** Khi đổi COUNTRY_CODE, dữ liệu cũ không bị mất
- ✅ **Rõ ràng:** Biết ngay dữ liệu của quốc gia nào

**Để lấy dữ liệu nhiều quốc gia:**

1. Sửa `COUNTRY_CODE` trong `config.py`
2. Chạy `python main.py`
3. Lặp lại cho các quốc gia khác

Ví dụ script tự động:

```python
# multi_country_fetch.py
from config import START, END
from data_manager import DataManager
import config

countries = ["DE_LU", "FR", "ES", "IT", "GB"]

for country in countries:
    print(f"\n{'='*50}")
    print(f"Fetching data for {country}")
    print(f"{'='*50}\n")

    # Cập nhật country code
    config.COUNTRY_CODE = country

    # Tạo manager và fetch
    manager = DataManager(force_fetch=False)
    manager.fetch_all()
```

## 🛠️ Mở rộng / Tùy chỉnh

### Thêm loại dữ liệu mới

1. Thêm hàm fetch trong `data_fetcher.py`
2. Thêm xử lý trong `data_manager.py`
3. Thêm vào `FETCH_CONFIG` trong `config.py`

### Thay đổi định dạng lưu file

Chỉnh sửa hàm `save_series()` hoặc `save_dataframe()` trong `utils.py`

## 📝 Ghi chú

- **Logic lấy dữ liệu không thay đổi** - tất cả logic từ `crawl.py` vẫn được giữ nguyên
- **Thêm khả năng kiểm tra thông minh** - chỉ lấy dữ liệu còn thiếu để tiết kiệm thời gian
- **Dễ bảo trì** - code được tổ chức thành các module nhỏ, dễ chỉnh sửa
- **Error handling tốt hơn** - mỗi lần fetch đều có xử lý lỗi riêng

## 🔐 Cảnh báo

- **Không commit file config với API key** - thêm `config.py` vào `.gitignore` nếu sử dụng Git
- **Tôn trọng API quota** - ENTSO-E có giới hạn API calls, dùng chế độ --force một cách hợp lý

## 📚 Tài liệu tham khảo

### ENTSO-E API & entsoe-py Library

Code này sử dụng thư viện **entsoe-py** (v0.7.8+) để giao tiếp với ENTSO-E Transparency Platform API.

**Thư viện**: [EnergieID/entsoe-py](https://github.com/EnergieID/entsoe-py)
**API Documentation**: [ENTSO-E API Guide](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)

### Lưu ý quan trọng về API

1. **Type hints chính xác**:
   - `query_generation()` → trả về **DataFrame** (không phải Series)
   - `query_wind_and_solar_forecast()` → trả về **DataFrame**
   - `query_load()` / `query_load_forecast()` → trả về **DataFrame**
   - `query_day_ahead_prices()` → trả về **Series**

2. **Named parameters**:
   - Bắt buộc phải dùng `country_code=`, `start=`, `end=` khi gọi API
   - Timestamp phải có timezone: `pd.Timestamp('2024-01-01', tz='UTC')`

3. **Giới hạn**:
   - Queries tự động được split nếu span > 1 năm (decorator `@year_limited`)
   - Một số queries giới hạn 100 documents (decorator `@documents_limited(100)`)

4. **Country codes**:
   - Dùng bidding zone codes: `'DE_LU'` (Germany-Luxembourg), `'FR'`, `'BE'`, etc.
   - Xem đầy đủ tại: [entsoe-py mappings.py](https://github.com/EnergieID/entsoe-py/blob/master/entsoe/mappings.py)

### API Methods được sử dụng

```python
# EntsoePandasClient methods
client.query_generation(country_code, start, end, psr_type) → pd.DataFrame
client.query_wind_and_solar_forecast(country_code, start, end, psr_type) → pd.DataFrame
client.query_load(country_code, start, end) → pd.DataFrame
client.query_load_forecast(country_code, start, end) → pd.DataFrame
client.query_installed_generation_capacity(country_code, start, end, psr_type) → pd.DataFrame
client.query_unavailability_of_generation_units(country_code, start, end, docstatus) → pd.DataFrame
client.query_day_ahead_prices(country_code, start, end) → pd.Series
```
