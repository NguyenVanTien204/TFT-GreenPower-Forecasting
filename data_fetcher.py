import requests
import pandas as pd
from datetime import datetime, timedelta
import dotenv
import time

def fetch_historical_load(zone, start_date, end_date, api_key, granularity="hourly"):
    """
    Lấy dữ liệu Total Load từ Electricity Maps API v3 theo vòng lặp.
    Tham số granularity có thể nhận các giá trị: 
    '5_minutes', '15_minutes', 'hourly', 'daily', 'monthly', 'quarterly', 'yearly'
    """
    base_url = "https://api.electricitymaps.com/v3/total-load/past-range"
    headers = {"auth-token": api_key}
    
    all_data = []
    
    # Chuyển đổi string sang object datetime
    current_start = pd.to_datetime(start_date)
    final_end = pd.to_datetime(end_date)
    
    # Điều chỉnh khoảng thời gian (chunk) cho mỗi lần gọi API dựa trên độ phân giải
    # Hourly tối đa 10 ngày, Daily tối đa 100 ngày
    if granularity in ['5_minutes', '15_minutes', 'hourly']:
        days_per_request = 10
    else:
        days_per_request = 100 # Cho daily, monthly, yearly...
    
    while current_start < final_end:
        current_end = current_start + timedelta(days=days_per_request)
        if current_end > final_end:
            current_end = final_end
            
        params = {
            "zone": zone,
            "start": current_start.strftime('%Y-%m-%dT%H:%MZ'),
            "end": current_end.strftime('%Y-%m-%dT%H:%MZ'),
            "temporalGranularity": granularity
        }
        
        print(f"Đang lấy dữ liệu ({granularity}) từ {params['start']} đến {params['end']}...")
        
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status() 
            
            data = response.json().get('data', [])
            if data:
                all_data.extend(data)
            
            time.sleep(0.5) 
            
        except Exception as e:
            print(f"Lỗi tại khoảng thời gian {current_start}: {e}")
            break
            
        current_start = current_end

    if not all_data:
        print("Không tìm thấy dữ liệu.")
        return pd.DataFrame()
        
    df = pd.DataFrame(all_data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime').reset_index(drop=True)
    
    # --- THỐNG KÊ DỮ LIỆU ---
    # Đếm số lượng dựa trên cột isEstimated
    total_records = len(df)
    # Trong API, isEstimated trả về giá trị boolean
    real_data_count = len(df[df['isEstimated'] == False])
    estimated_data_count = len(df[df['isEstimated'] == True])
    
    print("\n" + "="*30)
    print(f"KẾT THÚC THU THẬP DỮ LIỆU ({zone})")
    print(f"- Tổng số dòng thu được: {total_records}")
    print(f"- Số dòng dữ liệu THẬT (Measured): {real_data_count}")
    print(f"- Số dòng dữ liệu GIẢ LẬP/ƯỚC TÍNH (Estimated): {estimated_data_count}")
    
    # Cảnh báo nếu dữ liệu giả lập chiếm tỷ lệ quá cao
    if total_records > 0 and (estimated_data_count / total_records) > 0.5:
        print("CẢNH BÁO: Hơn 50% dữ liệu là giả lập (Estimated). Hãy cân nhắc khi dùng cho mô hình TFT.")
    print("="*30 + "\n")
    
    return df

# --- THIẾT LẬP THÔNG SỐ ---
# Đảm bảo bạn đã lưu API Key vào file .env hoặc thay trực tiếp vào đây
API_KEY = dotenv.get_key(dotenv.find_dotenv(), "ELECTRIC_MAP_API_KEY") or "YOUR_API_KEY_HERE"
ZONE = "DE" 
START = "2024-01-01"
END = "2024-12-31" 
# Bạn có thể thay thành 'daily', 'monthly', 'yearly' tùy nhu cầu
GRANULARITY = "daily" 

df_load = fetch_historical_load(ZONE, START, END, API_KEY, granularity=GRANULARITY)

# Lưu và kiểm tra
if not df_load.empty:
    filename = f"load_data_{ZONE}_{GRANULARITY}.csv"
    df_load.to_csv(filename, index=False)
    print(f"Đã lưu dữ liệu vào file: {filename}")
