# ENTSO-E Data Availability Guide

Hướng dẫn về các khu vực (bidding zones), country codes và dữ liệu khả dụng từ ENTSO-E Transparency Platform.

---

## 1. Country Codes & Bidding Zones

### 1.1. Các Quốc Gia Châu Âu Chính

| Country Code | Meaning | Timezone | Ghi chú |
|--------------|---------|----------|---------|
| **AL** | Albania, OST BZ/CA/MBA | Europe/Tirane | |
| **AT** | Austria, APG BZ/CA/MBA | Europe/Vienna | Tách từ DE_AT_LU từ 2018 |
| **BA** | Bosnia Herzegovina | Europe/Sarajevo | |
| **BE** | Belgium, Elia BZ/CA/MBA | Europe/Brussels | |
| **BG** | Bulgaria, ESO BZ/CA/MBA | Europe/Sofia | |
| **BY** | Belarus BZ/CA/MBA | Europe/Minsk | |
| **CH** | Switzerland, Swissgrid BZ/CA/MBA | Europe/Zurich | |
| **CY** | Cyprus, Cyprus TSO BZ/CA/MBA | Asia/Nicosia | |
| **CZ** | Czech Republic, CEPS BZ/CA/MBA | Europe/Prague | |
| **DE** | Germany | Europe/Berlin | Riêng từ 2018 |
| **DE_LU** | Germany-Luxembourg BZ/MBA | Europe/Berlin | Từ 2018 trở đi |
| **DE_AT_LU** | Germany-Austria-Luxembourg BZ | Europe/Berlin | Chỉ 2015-2018 |
| **DK** | Denmark | Europe/Copenhagen | |
| **DK_1** | DK1 BZ/MBA (West Denmark) | Europe/Copenhagen | |
| **DK_2** | DK2 BZ/MBA (East Denmark) | Europe/Copenhagen | |
| **EE** | Estonia, Elering BZ/CA/MBA | Europe/Tallinn | |
| **ES** | Spain, REE BZ/CA/MBA | Europe/Madrid | |
| **FI** | Finland, Fingrid BZ/CA/MBA | Europe/Helsinki | |
| **FR** | France, RTE BZ/CA/MBA | Europe/Paris | |
| **GB** | Great Britain, National Grid | Europe/London | |
| **GB_NIR** | Northern Ireland, SONI CA | Europe/Belfast | |
| **GR** | Greece, IPTO BZ/CA/MBA | Europe/Athens | |
| **HR** | Croatia, HOPS BZ/CA/MBA | Europe/Zagreb | |
| **HU** | Hungary, MAVIR CA/BZ/MBA | Europe/Budapest | |
| **IE_SEM** | Ireland (SEM) BZ/MBA | Europe/Dublin | |
| **IS** | Iceland | Atlantic/Reykjavik | Dữ liệu hạn chế |
| **IT** | Italy, IT CA/MBA | Europe/Rome | Nhiều sub-zones |
| **LT** | Lithuania, Litgrid BZ/CA/MBA | Europe/Vilnius | |
| **LU** | Luxembourg, CREOS CA | Europe/Luxembourg | |
| **LV** | Latvia, AST BZ/CA/MBA | Europe/Riga | |
| **MD** | Moldova, Moldelectica BZ/CA/MBA | Europe/Chisinau | |
| **ME** | Montenegro, CGES BZ/CA/MBA | Europe/Podgorica | |
| **MK** | North Macedonia, MEPSO BZ/CA/MBA | Europe/Skopje | |
| **MT** | Malta, Malta BZ/CA/MBA | Europe/Malta | |
| **NL** | Netherlands, TenneT NL BZ/CA/MBA | Europe/Amsterdam | |
| **PL** | Poland, PSE SA BZ/BZA/CA/MBA | Europe/Warsaw | |
| **PT** | Portugal, REN BZ/CA/MBA | Europe/Lisbon | |
| **RO** | Romania, Transelectrica BZ/CA/MBA | Europe/Bucharest | |
| **RS** | Serbia, EMS BZ/CA/MBA | Europe/Belgrade | |
| **RU** | Russia BZ/CA/MBA | Europe/Moscow | Dữ liệu hạn chế |
| **RU_KGD** | Kaliningrad BZ/CA/MBA | Europe/Kaliningrad | |
| **SE** | Sweden, Sweden MBA, SvK CA | Europe/Stockholm | 4 zones |
| **SE_1** | SE1 BZ/MBA (North Sweden) | Europe/Stockholm | |
| **SE_2** | SE2 BZ/MBA (North-Central) | Europe/Stockholm | |
| **SE_3** | SE3 BZ/MBA (South-Central) | Europe/Stockholm | |
| **SE_4** | SE4 BZ/MBA (South Sweden) | Europe/Stockholm | |
| **SI** | Slovenia, ELES BZ/CA/MBA | Europe/Ljubljana | |
| **SK** | Slovakia, SEPS BZ/CA/MBA | Europe/Bratislava | |
| **TR** | Turkey BZ/CA/MBA | Europe/Istanbul | |
| **UA** | Ukraine, Ukraine BZ, MBA | Europe/Kiev | |
| **XK** | Kosovo/XK CA/XK BZN | Europe/Rome | |

### 1.2. Các Zone Đặc Biệt của Ý (Italy)

Italy có nhiều bidding zones nội bộ:

| Code | Description |
|------|-------------|
| IT_CNOR | IT-Centre-North BZ |
| IT_CSUD | IT-Centre-South BZ |
| IT_SUD | IT-South BZ |
| IT_NORD | IT-North BZ |
| IT_SICI | IT-Sicily BZ |
| IT_SARD | IT-Sardinia BZ |
| IT_CALA | IT-Calabria BZ (từ 2021) |
| IT_BRNN | IT-Brindisi BZ |

### 1.3. Các Zone của Na Uy (Norway)

| Code | Description |
|------|-------------|
| NO_1 | NO1 BZ/MBA (Oslo) |
| NO_2 | NO2 BZ/MBA (Kristiansand) |
| NO_3 | NO3 BZ/MBA (Trondheim) |
| NO_4 | NO4 BZ/MBA (Tromsø) |
| NO_5 | NO5 BZ/MBA (Bergen) |

---

## 2. Khoảng Thời Gian Dữ Liệu

### 2.1. Dữ liệu Lịch Sử (Historical Data)

Dữ liệu lịch sử có sẵn từ ENTSO-E Transparency Platform tùy theo từng loại:

| Loại dữ liệu | Từ ngày | Độ phân giải | Ghi chú |
|--------------|---------|--------------|---------|
| **Generation Actual** | 2015-01-01 | 15min/1h | Phụ thuộc quốc gia |
| **Load Actual** | 2015-01-01 | 15min/1h | Đầy đủ nhất |
| **Day-Ahead Prices** | 2015-01-01 | 1h | Hầu hết các nước |
| **Wind & Solar Forecast** | 2015-01-01 | 15min/1h | Không phải tất cả |
| **Installed Capacity** | 2015-01-01 | Yearly | Cập nhật hàng năm |
| **Unavailable Capacity** | 2015-01-01 | Event-based | Documents |

### 2.2. Dữ Liệu Theo Quốc Gia

**Dữ liệu đầy đủ nhất (từ 2015):**
- Germany (DE, DE_LU)
- France (FR)
- Netherlands (NL)
- Belgium (BE)
- Great Britain (GB)
- Denmark (DK_1, DK_2)
- Norway (NO_1, NO_2, NO_3, NO_4, NO_5)
- Sweden (SE_1, SE_2, SE_3, SE_4)
- Finland (FI)
- Poland (PL)
- Czech Republic (CZ)
- Austria (AT)
- Switzerland (CH)
- Spain (ES)
- Portugal (PT)
- Italy (IT + sub-zones)

**Dữ liệu tốt (từ 2016-2017):**
- Hungary (HU)
- Romania (RO)
- Bulgaria (BG)
- Greece (GR)
- Slovakia (SK)
- Slovenia (SI)
- Croatia (HR)
- Estonia (EE)
- Latvia (LV)
- Lithuania (LT)

**Dữ liệu hạn chế (từ 2018 trở đi hoặc không đầy đủ):**
- Ireland (IE_SEM)
- Serbia (RS)
- Bosnia Herzegovina (BA)
- Montenegro (ME)
- North Macedonia (MK)
- Albania (AL)
- Turkey (TR)
- Cyprus (CY)
- Malta (MT)
- Moldova (MD)
- Ukraine (UA)
- Belarus (BY)

### 2.3. Thay Đổi Bidding Zones

**Quan trọng:** Một số bidding zones đã thay đổi theo thời gian:

| Thời gian | Old Zone | New Zones | Lý do |
|-----------|----------|-----------|-------|
| **2018-10-01** | DE_AT_LU | DE_LU + AT | Austria tách ra |
| **2021-01-01** | IT_CNOR, IT_CSUD, IT_SUD | Giữ nguyên + IT_CALA | Thêm Calabria zone |

**Khi fetch dữ liệu:**
- Trước 2018-10-01: Dùng `DE_AT_LU` cho Germany+Austria+Luxembourg
- Từ 2018-10-01: Dùng `DE_LU` (Germany+Luxembourg) và `AT` (Austria) riêng

---

## 3. Các Loại Dữ Liệu Có Sẵn

### 3.1. Generation (Actual)

**API Method:** `query_generation(country_code, start, end, psr_type)`

**PSR Types có sẵn:**
- `B01` - Biomass
- `B04` - Fossil Gas
- `B05` - Fossil Hard coal
- `B09` - Geothermal
- `B10` - Hydro Pumped Storage
- `B11` - Hydro Run-of-river and poundage
- `B12` - Hydro Water Reservoir
- `B13` - Marine
- `B14` - Nuclear
- `B15` - Other renewable
- `B16` - Solar
- `B18` - Wind Offshore
- `B19` - Wind Onshore
- `B20` - Other

**Độ phân giải:**
- 15 phút: DE, NL, BE, AT, CH, DK, NO, SE, FI
- 1 giờ: Hầu hết các nước khác

### 3.2. Load (Actual & Forecast)

**API Methods:**
- `query_load(country_code, start, end)` - Actual load
- `query_load_forecast(country_code, start, end)` - Day-ahead forecast

**Khả dụng:** Tất cả các nước trong ENTSO-E (từ 2015)

**Độ phân giải:**
- 15 phút: DE, NL, BE, AT, CH
- 1 giờ: Hầu hết các nước khác

### 3.3. Prices

**API Method:** `query_day_ahead_prices(country_code, start, end)`

**Khả dụng:** 
- Đầy đủ: Hầu hết các nước EU từ 2015
- Hạn chế: Các nước ngoài EU market coupling

**Độ phân giải:** 1 giờ (hourly)

### 3.4. Wind & Solar Forecast

**API Method:** `query_wind_and_solar_forecast(country_code, start, end, psr_type)`

**PSR Types:**
- `B16` - Solar
- `B18` - Wind Offshore
- `B19` - Wind Onshore

**Khả dụng:**
- Tốt: DE, NL, DK, ES, FR, GB, IT
- Trung bình: AT, BE, CH, PL, PT, SE
- Hạn chế hoặc không có: Các nước Đông Âu, Balkan

### 3.5. Installed Capacity

**API Method:** `query_installed_generation_capacity(country_code, start, end, psr_type=None)`

**Cập nhật:** Thường cập nhật hàng năm (1/1 mỗi năm)

**Khả dụng:** Hầu hết các nước từ 2015

### 3.6. Unavailable Capacity

**API Method:** `query_unavailability_of_generation_units(country_code, start, end, docstatus)`

**Format:** ZIP files chứa documents

**Khả dụng:** Tất cả các nước, real-time updates

---

## 4. Hạn Chế và Lưu Ý

### 4.1. Rate Limiting

ENTSO-E API có giới hạn:
- **400 requests/minute** per API key
- Documents limited: 100 documents per request (cho unavailability data)
- Year limited: Tự động chia nhỏ queries > 1 năm

### 4.2. Data Quality

**Cao nhất:**
- Germany (DE_LU)
- France (FR)
- Netherlands (NL)
- Belgium (BE)
- Nordic countries (DK, NO, SE, FI)

**Trung bình:**
- Central Europe (AT, CH, CZ, PL, SK, SI, HU)
- Southern Europe (ES, PT, IT, GR)

**Thấp hoặc thiếu:**
- Balkan countries
- Eastern Europe (ngoài Baltic states)

### 4.3. Missing Data

Một số gaps phổ biến:
- **Iceland (IS):** Rất ít dữ liệu trên ENTSO-E platform
- **Turkey (TR):** Chỉ một phần dữ liệu
- **UK Brexit period:** Một số gaps trong 2020-2021
- **Wind/Solar forecast:** Không phải tất cả countries đều publish

### 4.4. Resolution Changes

Một số quốc gia đã thay đổi độ phân giải:
- Nhiều nước chuyển từ 1h → 15min trong 2017-2019
- Check `df.index.freq` để xác định resolution

---

## 5. Best Practices

### 5.1. Chọn Country Code

1. **Check bidding zone history** trước khi fetch dữ liệu dài hạn
2. **Dùng DE_LU thay vì DE** cho Germany từ 2018
3. **Dùng AT riêng** cho Austria từ 2018
4. **Italy:** Dùng IT cho tổng, hoặc sub-zones cho chi tiết

### 5.2. Date Ranges

1. **Bắt đầu từ 2015-01-01** cho hầu hết dữ liệu
2. **Chia nhỏ queries:** 1 năm mỗi lần để tránh timeout
3. **Check availability** trước: Một số dữ liệu chỉ có từ 2016-2017

### 5.3. Error Handling

Common errors:
- **404 Not Found:** Country không có loại data này
- **503 Service Unavailable:** Server tạm thời bận
- **400 Bad Request:** Invalid country code hoặc date range

### 5.4. File Naming Convention

Khi lưu file, bao gồm country code:
```
{country_code}_{data_type}.csv
```

Ví dụ:
- `DE_LU_solar.csv`
- `FR_day_ahead_prices.csv`
- `NO_1_load_actual.csv`

---

## 6. Ví Dụ Sử Dụng

### 6.1. Germany (DE_LU)

```python
COUNTRY_CODE = "DE_LU"
START = pd.Timestamp("2020-01-01", tz="UTC")
END = pd.Timestamp("2024-12-31", tz="UTC")

# Available data:
# - All generation types (15min resolution)
# - Load actual & forecast (15min)
# - Day-ahead prices (hourly)
# - Wind & solar forecast (15min)
# - Installed capacity (yearly)
# - Unavailable capacity (real-time)
```

### 6.2. Nordic Countries

```python
# Norway: Split into 5 zones
for zone in ["NO_1", "NO_2", "NO_3", "NO_4", "NO_5"]:
    # Fetch data for each zone
    
# Sweden: 4 zones
for zone in ["SE_1", "SE_2", "SE_3", "SE_4"]:
    # Fetch data for each zone
    
# Denmark: 2 zones
for zone in ["DK_1", "DK_2"]:
    # Fetch data for each zone
```

### 6.3. Historical vs Current

```python
# Before October 2018
COUNTRY_CODE = "DE_AT_LU"
START = pd.Timestamp("2015-01-01", tz="UTC")
END = pd.Timestamp("2018-09-30", tz="UTC")

# After October 2018
COUNTRY_CODE = "DE_LU"  # Germany + Luxembourg
START = pd.Timestamp("2018-10-01", tz="UTC")
END = pd.Timestamp("2024-12-31", tz="UTC")

# Austria separate
COUNTRY_CODE = "AT"
START = pd.Timestamp("2018-10-01", tz="UTC")
END = pd.Timestamp("2024-12-31", tz="UTC")
```

---

## 7. Resources

- **ENTSO-E Transparency Platform:** https://transparency.entsoe.eu/
- **API Guide:** https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html
- **entsoe-py Documentation:** https://github.com/EnergieID/entsoe-py
- **Area Mappings:** https://github.com/EnergieID/entsoe-py/blob/master/entsoe/mappings.py

---

**Cập nhật:** Tháng 12/2025  
**Nguồn:** ENTSO-E Transparency Platform & entsoe-py library
