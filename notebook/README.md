# Quy tắc đặt tên notebook

Mỗi notebook cần tiền tố mã (prefix) để phản ánh mục đích chính. Cấu trúc: `[Mã][Số thứ tự]_[Tên_ngắn_gọn].ipynb` (dùng dấu gạch dưới, tiếng Anh hoặc không dấu, ngắn gọn). Ví dụ: `M01_weather_fetch.ipynb`.

## Bảng mã
| Mã (Prefix) | Ý nghĩa    | Tên đầy đủ                  | Nội dung thực hiện                                                       |
|-------------|------------|-----------------------------|-------------------------------------------------------------------------|
| M           | Mining     | Data Acquisition            | Thu thập dữ liệu từ API, Web scraping, SQL...                           |
| S           | Synthesis  | Data Integration            | Gộp nhiều nguồn dữ liệu, xử lý format thô.                             |
| P           | Processing | Cleaning/Pre-processing     | Xử lý giá trị thiếu (NA), nhiễu, chuẩn hóa kiểu dữ liệu.               |
| E           | EDA        | Exploratory Data Analysis   | Phân tích thống kê, vẽ biểu đồ tìm quy luật.                           |
| F           | Feature    | Feature Engineering         | Tạo biến mới, mã hóa (One-hot), Scaling.                               |
| T           | Training   | Model Training              | Huấn luyện mô hình, tinh chỉnh tham số (Tuning).                       |
| V           | Validation | Evaluation/Validation       | Đánh giá mô hình trên tập test, vẽ nhãn, tính metric.                  |

## Ví dụ đặt tên
- `M01_weather_fetch.ipynb`: thu thập dữ liệu thời tiết.
- `S01_energy_merge.ipynb`: hợp nhất dữ liệu năng lượng từ nhiều nguồn.
- `P01_clean_load.ipynb`: làm sạch dữ liệu tải điện.
- `E01_load_trends.ipynb`: EDA xu hướng tải điện.
- `F01_feature_build.ipynb`: tạo đặc trưng cho mô hình.
- `T01_model_baseline.ipynb`: huấn luyện mô hình baseline.
- `V01_eval_report.ipynb`: đánh giá và tổng hợp kết quả.
