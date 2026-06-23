# DÀN Ý CHI TIẾT: BÁO CÁO NGHIÊN CỨU KHOA HỌC

**Đề tài:** Ứng dụng mô hình Temporal Fusion Transformer (TFT) và Kỹ thuật Transfer Learning trong dự báo sản lượng điện năng tại Việt Nam.

---

## CHƯƠNG 1: GIỚI THIỆU TỔNG QUAN

**1.1. Lý do thực hiện đề tài**
- **1.1.1. Hiện trạng và Thách thức:** Phân tích bài toán cân bằng cung - cầu điện năng tại Việt Nam trong bối cảnh chuyển dịch năng lượng và gia tăng phụ tải. Sự cần thiết của các công cụ dự báo có độ chính xác cao để lập kế hoạch vận hành hệ thống điện quốc gia.
- **1.1.2. Thách thức "Điểm nghẽn dữ liệu":** Làm rõ vấn đề khan hiếm dữ liệu (Data Scarcity) nội địa. Đặc thù dữ liệu Việt Nam thường có tần suất thấp (tháng), chuỗi thời gian ngắn (khoảng 500 mẫu) và chịu nhiều nhiễu động từ biến động kinh tế vĩ mô.
- **1.1.3. Tính cần thiết của việc ứng dụng Deep Learning tiên tiến:** Nêu bật sự ưu việt của AI so với các mô hình thống kê cũ trong việc giải quyết tính phi tuyến và tích hợp nhiều nguồn dữ liệu (covariates).

**1.2. Mục tiêu và sản phẩm của nghiên cứu**
- **1.2.1. Mục tiêu khoa học:** Đề xuất và chứng minh tính hiệu quả của một Framework Transfer Learning (học chuyển giao) dành riêng cho bài toán chuỗi thời gian nhỏ.
- **1.2.2. Sản phẩm đạt được:** Một mô hình Hybrid (TFT-TL) hoàn chỉnh mã nguồn mở, các tập dữ liệu đã qua tiền xử lý, và báo cáo phân tích định lượng về tác động của các biến số kinh tế lên sản lượng điện.

**1.3. Phạm vi nghiên cứu**
- **1.3.1. Đối tượng dữ liệu:** Dữ liệu sản lượng điện thế giới (Ember Global - hàng chục nghìn mẫu) và dữ liệu nội địa Việt Nam (Vietnam Monthly - 500 mẫu từ 2019-2025).
- **1.3.2. Giả định và Ràng buộc kỹ thuật:** Giới hạn dự báo ở tần suất tháng (Monthly forecasting). Giả định cấu trúc vật lý của hệ thống năng lượng toàn cầu có sự tương đồng nhất định để thực hiện Transfer Learning.

**1.4. Tính ứng dụng và đóng góp của đề tài:** 
- Đóng góp về mặt phương pháp luận (xử lý Data Scarcity).
- Đóng góp thực tiễn cho EVN/A0 trong công tác lập phương thức vận hành hệ thống điện trung và dài hạn.

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ

**2.1. Cơ sở lý thuyết về dự báo chuỗi thời gian (Time Series Forecasting)**
- **2.1.1. Các phương pháp truyền thống:** Đánh giá ưu nhược điểm của ARIMA, SARIMA, ETS (chỉ hoạt động tốt trên chuỗi tuyến tính, khó tích hợp biến ngoại sinh).
- **2.1.2. Deep Learning trong dự báo năng lượng:** Quá trình tiến hóa từ RNN, LSTM, GRU đến kiến trúc Transformer.

**2.2. Lý thuyết chuyên sâu về Temporal Fusion Transformer (TFT)**
- **2.2.1. Kiến trúc Multi-head Attention:** Khả năng nắm bắt các phụ thuộc dài hạn (long-term dependencies) trong chuỗi thời gian.
- **2.2.2. Mạng chọn lọc biến số (Variable Selection Network - VSN):** Cơ chế lọc bỏ nhiễu và gán trọng số tự động cho các biến đầu vào (đóng vai trò cực kỳ quan trọng khi thêm biến kinh tế Việt Nam).
- **2.2.3. Gating mechanisms (GRN - Gated Residual Network):** Cơ chế bỏ qua các thành phần không cần thiết để mô hình linh hoạt với các tập dữ liệu có độ phức tạp khác nhau.

**2.3. Kỹ thuật Transfer Learning cho dữ liệu chuỗi thời gian**
- **2.3.1. Khái niệm Domain Adaptation:** Ánh xạ từ Source Domain (Điện năng thế giới) sang Target Domain (Điện năng Việt Nam).
- **2.3.2. Chiến lược Pre-training và Fine-tuning:** Cơ chế đóng băng (Freezing) trọng số và tinh chỉnh (Fine-tuning) với tốc độ học (Learning Rate) nhỏ.

**2.4. Công nghệ và Phương pháp tiếp cận**
- **2.4.1. Công nghệ sử dụng:** Python, PyTorch Forecasting (thư viện chuyên dụng cho TFT), PyTorch Lightning, Pandas, Optuna (Tối ưu hóa siêu tham số).
- **2.4.2. Các chỉ số đánh giá mô hình:** Định nghĩa và công thức toán học của MAE, RMSE, MAPE.

---

## CHƯƠNG 3: THIẾT KẾ HỆ THỐNG VÀ KIẾN TRÚC MÔ HÌNH

**3.1. Sơ đồ luồng dữ liệu tổng quát (Data Pipeline):** Trực quan hóa quy trình từ thu thập, làm sạch, biến đổi dữ liệu (ETL) đến khi đưa vào huấn luyện mô hình.

**3.2. Thiết kế kiến trúc Pre-training (Giai đoạn 1 - Học nền tảng)**
- **3.2.1. Cấu trúc đầu vào:** Tập dữ liệu Ember với các biến chung (Nhiệt độ, Bức xạ, Lượng mưa, Sản lượng).
- **3.2.2. Mục tiêu của lớp Encoder:** Giúp mô hình nội suy được quy luật vật lý cơ bản: "Thời tiết ảnh hưởng thế nào đến nhu cầu điện và năng lượng tái tạo".

**3.3. Thiết kế chiến lược Transfer Learning (Giai đoạn 2 - Cá nhân hóa)**
- **3.3.1. Cơ chế đóng băng lớp (Layer Freezing):** Giữ cố định các lớp Attention đã học được quy luật từ giai đoạn 1.
- **3.3.2. Mở khóa và tích hợp (Unfreezing & Integration):** Chỉ mở khóa cấu trúc VSN để mô hình tiếp thu thêm 10-15 biến ngoại sinh đặc thù của Việt Nam.

**3.4. Cấu trúc biến số (Feature Logic)**
- Thiết kế phân tách rõ ràng giữa: Biến tĩnh (Static Covariates), Biến động đã biết trước (Known Future Covariates - VD: Ngày lễ, Tháng), Biến động không biết trước (Unknown Future Covariates - VD: Nhiệt độ dự báo, GDP dự báo).

**3.5. Đặc tả hợp đồng dữ liệu (Data Contract):** Định nghĩa rõ cấu trúc file `vn_tft_ready.csv` và `tft_premodel_dataset_EDA.csv` (kiểu dữ liệu, định dạng thời gian, danh sách cột).

---

## CHƯƠNG 4: NỘI DUNG THỰC HIỆN VÀ THỰC NGHIỆM CHI TIẾT

**4.1. Kỹ thuật dữ liệu (Data Engineering & EDA)**
- **4.1.1. Hợp nhất đa nguồn:** Kết nối dữ liệu từ `merged_electric_weather_data.csv` (Thế giới) và `full_vietnam_monthly_merger.csv` (Việt Nam).
- **4.1.2. Phân tích EDA (dựa trên `EDA_new_data.ipynb` & `EDA_VN_data.ipynb`):** Phát hiện tính mùa vụ kép (mùa hè miền Bắc và mùa khô miền Nam). Xử lý Missing Values.

**4.2. Xây dựng bộ đặc trưng (Feature Engineering cho Việt Nam)**
- **4.2.1. Nhóm biến thời tiết:** Nhiệt độ trung bình, độ ẩm, số giờ nắng.
- **4.2.2. Nhóm biến kinh tế vĩ mô:** Chỉ số GDP, Chỉ số giá tiêu dùng (CPI), Chỉ số sản xuất công nghiệp (IIP).
- **4.2.3. Nhóm biến chính sách:** Biến giả (Dummy variables) đại diện cho chính sách giá điện FIT (điện mặt trời/điện gió), các kỳ nghỉ Lễ Tết.

**4.3. Quá trình huấn luyện Pre-training (Thực thi trên `trainTFT_v3.ipynb`)**
- Khởi tạo DataLoaders cho hàng chục nghìn dòng. Thiết lập thông số: `max_encoder_length`, `max_prediction_length`.
- Quá trình giảm Loss trên tập validation của thế giới.

**4.4. Quá trình Transfer Learning và Fine-tuning (Thực thi trên `transfer_learning_v3.ipynb`)**
- **4.4.1. Kỹ thuật chống quá khớp (Regularization) trên tập nhỏ (500 mẫu):** Sử dụng Dropout cao hơn, Weight Decay.
- **4.4.2. Điều chỉnh Learning Rate:** Sử dụng `ReduceLROnPlateau` scheduler với tốc độ học ban đầu rất nhỏ (VD: 1e-4 hoặc 1e-5) để không phá vỡ tri thức đã học.

---

## CHƯƠNG 5: KẾT QUẢ VÀ ĐÁNH GIÁ

**5.1. Kết quả huấn luyện và độ hội tụ (Loss Curves)**
- Trình bày biểu đồ Loss (Training vs Validation) cho cả 2 giai đoạn. Chứng minh việc Fine-tuning giúp mô hình hội tụ nhanh hơn học từ đầu.

**5.2. So sánh hiệu năng dự báo (Benchmarking)**
- **5.2.1. Đánh giá Ablation Study:** Bảng so sánh 3 kịch bản: TFT thuần túy (Không TL), TFT + TL (Không biến kinh tế), TFT + TL + Biến kinh tế.
- **5.2.2. So sánh với Baseline:** Đánh giá sự vượt trội của TFT so với các mô hình truyền thống (LSTM, ARIMA) qua MAPE và RMSE.

**5.3. Trực quan hóa kết quả dự báo (Forecasting Visualization)**
- **5.3.1. Khớp chuỗi thời gian:** Biểu đồ đường so sánh giữa giá trị thực tế (Actual) và dự báo (Prediction) tại Việt Nam.
- **5.3.2. Đánh giá vùng tin cậy:** Khả năng dự báo khoảng (Prediction Intervals - VD: p10, p50, p90) để đánh giá rủi ro cực đoan.

**5.4. AI giải thích được (Explainable AI - XAI)**
- **5.4.1. Tầm quan trọng của biến số (Feature Importance):** Trích xuất trọng số từ Variable Selection Network để xem biến nào (Nhiệt độ, IIP hay Lễ Tết) đóng góp mạnh nhất vào dự báo.
- **5.4.2. Phân tích Attention Weights:** Biểu đồ Attention cho thấy mô hình "nhìn" vào tháng nào trong quá khứ để dự đoán tháng tương lai.

---

## CHƯƠNG 6: KẾT LUẬN – HƯỚNG PHÁT TRIỂN

**6.1. Tổng kết kết quả:** 
- Khẳng định mô hình TFT kết hợp Transfer Learning đã giải quyết xuất sắc bài toán Data Scarcity tại Việt Nam. Độ chính xác cải thiện X% so với Baseline.

**6.2. Các hạn chế của nghiên cứu:** 
- Độ trễ của dữ liệu kinh tế vĩ mô (thường công bố chậm).
- Khó nắm bắt các cú sốc phi tuyến cực hạn (như đại dịch Covid-19).

**6.3. Hướng phát triển tương lai:** 
- Mở rộng dự báo ngắn hạn (Intra-day, hourly forecasting).
- Tích hợp dữ liệu không gian trực tiếp từ hình ảnh vệ tinh.
- Kết hợp dự báo vào các bài toán tối ưu vận hành thị trường điện lực.

---
## TÀI LIỆU THAM KHẢO
## PHỤ LỤC
- Mã nguồn triển khai.
- Bảng mô tả từ điển dữ liệu (Data Dictionary).
