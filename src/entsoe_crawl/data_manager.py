"""
Quản lý logic lấy dữ liệu thông minh - kiểm tra xem dữ liệu đã lấy chưa
"""
import os
import pandas as pd
import logging

from config import (
    API_KEY, START, END, COUNTRY_CODE,
    GENERATION_TYPES, DATA_DIRECTORIES, FETCH_CONFIG,
    FORECAST_SUPPORTED_ZONES
)
from electricmap_crawl.data_fetcher import DataFetcher
from utils import save_series, save_dataframe, file_exists, get_file_size, ensure_dir

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataManager:
    """
    Quản lý quá trình lấy dữ liệu từ ENTSO-E
    - Kiểm tra dữ liệu đã có chưa
    - Chỉ lấy dữ liệu còn thiếu
    - Lưu dữ liệu một cách có tổ chức
    """

    def __init__(self, force_fetch: bool = False):
        """
        Khởi tạo DataManager

        Args:
            force_fetch: Nếu True, lấy lại tất cả dữ liệu (bỏ qua kiểm tra)
        """
        self.fetcher = DataFetcher(API_KEY)
        self.force_fetch = force_fetch
        self.fetch_report = {}

    def check_data_exists(self, file_path: str, min_size_bytes: int = 1000) -> bool:
        """
        Kiểm tra file dữ liệu có tồn tại và có nội dung không

        Args:
            file_path: Đường dẫn file (sẽ tự động thêm COUNTRY_CODE vào tên)
            min_size_bytes: Kích thước tối thiểu (bytes) để coi là có dữ liệu

        Returns:
            True nếu file tồn tại và có dung lượng đủ, False nếu không
        """
        # Thêm country_code vào file_path để check đúng file
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        actual_file_path = os.path.join(dir_name, f"{COUNTRY_CODE}_{name_without_ext}.csv")

        if not file_exists(actual_file_path):
            return False

        size = get_file_size(actual_file_path)
        return size >= min_size_bytes

    def process_generation_actual(self) -> None:
        """
        Xử lý lấy dữ liệu Generation Actual
        """
        logger.info("=" * 50)
        logger.info("Processing Generation Actual Data")
        logger.info("=" * 50)

        if not FETCH_CONFIG.get("generation_actual", True):
            logger.info("Generation Actual is disabled in config")
            return

        output_dir = DATA_DIRECTORIES["generation_actual"]
        ensure_dir(output_dir)

        # Lấy dữ liệu generation types
        data_dict = self.fetcher.fetch_generation_actual(
            COUNTRY_CODE, START, END, GENERATION_TYPES
        )

        for fname, data in data_dict.items():
            file_path = os.path.join(output_dir, f"{fname}.csv")

            if not self.force_fetch and self.check_data_exists(file_path):
                logger.info(f"✓ {fname}.csv already exists, skipping")
                self.fetch_report[f"generation_actual/{fname}"] = "SKIPPED"
            elif data is not None:
                save_series(data, file_path, country_code=COUNTRY_CODE)
                logger.info(f"✓ Saved {COUNTRY_CODE}_{fname}.csv")
                self.fetch_report[f"generation_actual/{fname}"] = "SUCCESS"
            else:
                logger.warning(f"✗ Failed to fetch {fname}")
                self.fetch_report[f"generation_actual/{fname}"] = "FAILED"

    def process_generation_forecast(self) -> None:
        """
        Xử lý lấy dữ liệu Generation Forecast
        Chỉ fetch forecast cho các zones được hỗ trợ
        """
        logger.info("=" * 50)
        logger.info("Processing Generation Forecast Data")
        logger.info("=" * 50)

        if not FETCH_CONFIG.get("generation_forecast", True):
            logger.info("Generation Forecast is disabled in config")
            return

        # Kiểm tra xem zone hiện tại có hỗ trợ forecast không
        if COUNTRY_CODE not in FORECAST_SUPPORTED_ZONES:
            logger.warning(f"⚠ {COUNTRY_CODE} is not in FORECAST_SUPPORTED_ZONES, skipping forecast")
            return

        output_dir = DATA_DIRECTORIES["generation_forecast"]
        ensure_dir(output_dir)

        # Solar forecast
        file_path = os.path.join(output_dir, "solar_forecast.csv")

        if not self.force_fetch and self.check_data_exists(file_path):
            logger.info("✓ solar_forecast.csv already exists, skipping")
            self.fetch_report["generation_forecast/solar_forecast"] = "SKIPPED"
        else:
            data = self.fetcher.fetch_solar_forecast(COUNTRY_CODE, START, END)
            if data is not None:
                save_series(data, file_path, country_code=COUNTRY_CODE)
                logger.info(f"✓ Saved {COUNTRY_CODE}_solar_forecast.csv")
                self.fetch_report["generation_forecast/solar_forecast"] = "SUCCESS"
            else:
                logger.warning("✗ Failed to fetch solar_forecast")
                self.fetch_report["generation_forecast/solar_forecast"] = "FAILED"

        # Wind forecast
        file_path = os.path.join(output_dir, "wind_forecast.csv")

        if not self.force_fetch and self.check_data_exists(file_path):
            logger.info("✓ wind_forecast.csv already exists, skipping")
            self.fetch_report["generation_forecast/wind_forecast"] = "SKIPPED"
        else:
            data = self.fetcher.fetch_wind_forecast(COUNTRY_CODE, START, END)
            if data is not None:
                save_series(data, file_path, country_code=COUNTRY_CODE)
                logger.info(f"✓ Saved {COUNTRY_CODE}_wind_forecast.csv")
                self.fetch_report["generation_forecast/wind_forecast"] = "SUCCESS"
            else:
                logger.warning("✗ Failed to fetch wind_forecast")
                self.fetch_report["generation_forecast/wind_forecast"] = "FAILED"

    def process_load(self) -> None:
        """
        Xử lý lấy dữ liệu Load (Actual & Forecast)
        """
        logger.info("=" * 50)
        logger.info("Processing Load Data")
        logger.info("=" * 50)

        # Load Actual
        if FETCH_CONFIG.get("load_actual", True):
            output_dir = DATA_DIRECTORIES["load_actual"]
            ensure_dir(output_dir)
            file_path = os.path.join(output_dir, "total_load_actual.csv")

            if not self.force_fetch and self.check_data_exists(file_path):
                logger.info("✓ total_load_actual.csv already exists, skipping")
                self.fetch_report["load/total_load_actual"] = "SKIPPED"
            else:
                data = self.fetcher.fetch_load_actual(COUNTRY_CODE, START, END)
                if data is not None:
                    save_series(data, file_path, country_code=COUNTRY_CODE)
                    logger.info(f"✓ Saved {COUNTRY_CODE}_total_load_actual.csv")
                    self.fetch_report["load/total_load_actual"] = "SUCCESS"
                else:
                    logger.warning("✗ Failed to fetch load_actual")
                    self.fetch_report["load/total_load_actual"] = "FAILED"

        # Load Forecast
        if FETCH_CONFIG.get("load_forecast", True):
            output_dir = DATA_DIRECTORIES["load_forecast"]
            ensure_dir(output_dir)
            file_path = os.path.join(output_dir, "total_load_forecast.csv")

            if not self.force_fetch and self.check_data_exists(file_path):
                logger.info("✓ total_load_forecast.csv already exists, skipping")
                self.fetch_report["load/total_load_forecast"] = "SKIPPED"
            else:
                data = self.fetcher.fetch_load_forecast(COUNTRY_CODE, START, END)
                if data is not None:
                    save_series(data, file_path, country_code=COUNTRY_CODE)
                    logger.info(f"✓ Saved {COUNTRY_CODE}_total_load_forecast.csv")
                    self.fetch_report["load/total_load_forecast"] = "SUCCESS"
                else:
                    logger.warning("✗ Failed to fetch load_forecast")
                    self.fetch_report["load/total_load_forecast"] = "FAILED"

    def process_capacity(self) -> None:
        """
        Xử lý lấy dữ liệu Capacity
        """
        logger.info("=" * 50)
        logger.info("Processing Capacity Data")
        logger.info("=" * 50)

        if not FETCH_CONFIG.get("installed_capacity", True):
            logger.info("Capacity is disabled in config")
            return

        output_dir = DATA_DIRECTORIES["capacity"]
        ensure_dir(output_dir)

        # Installed capacity
        file_path = os.path.join(output_dir, "installed_capacity.csv")

        if not self.force_fetch and self.check_data_exists(file_path):
            logger.info("✓ installed_capacity.csv already exists, skipping")
            self.fetch_report["capacity/installed_capacity"] = "SKIPPED"
        else:
            data = self.fetcher.fetch_installed_capacity(COUNTRY_CODE, START, END)
            if data is not None:
                save_dataframe(data, file_path, country_code=COUNTRY_CODE)
                logger.info(f"✓ Saved {COUNTRY_CODE}_installed_capacity.csv")
                self.fetch_report["capacity/installed_capacity"] = "SUCCESS"
            else:
                logger.warning("✗ Failed to fetch installed_capacity")
                self.fetch_report["capacity/installed_capacity"] = "FAILED"

        # Unavailable capacity (optional - disabled by default)
        if FETCH_CONFIG.get("unavailability", True):
            file_path = os.path.join(output_dir, "unavailable_capacity.csv")

            if not self.force_fetch and self.check_data_exists(file_path):
                logger.info("✓ unavailable_capacity.csv already exists, skipping")
                self.fetch_report["capacity/unavailable_capacity"] = "SKIPPED"
            else:
                data = self.fetcher.fetch_unavailable_capacity(COUNTRY_CODE, START, END)
                if data is not None:
                    save_dataframe(data, file_path, country_code=COUNTRY_CODE)
                    logger.info(f"✓ Saved {COUNTRY_CODE}_unavailable_capacity.csv")
                    self.fetch_report["capacity/unavailable_capacity"] = "SUCCESS"
                else:
                    logger.warning("✗ Failed to fetch unavailable_capacity")
                    self.fetch_report["capacity/unavailable_capacity"] = "FAILED"

    def process_prices(self) -> None:
        """
        Xử lý lấy dữ liệu Prices
        """
        logger.info("=" * 50)
        logger.info("Processing Price Data")
        logger.info("=" * 50)

        if not FETCH_CONFIG.get("prices_day_ahead", True):
            logger.info("Prices is disabled in config")
            return

        output_dir = DATA_DIRECTORIES["prices"]
        ensure_dir(output_dir)

        file_path = os.path.join(output_dir, "day_ahead_price.csv")

        if not self.force_fetch and self.check_data_exists(file_path):
            logger.info("✓ day_ahead_price.csv already exists, skipping")
            self.fetch_report["prices/day_ahead_price"] = "SKIPPED"
        else:
            data = self.fetcher.fetch_day_ahead_prices(COUNTRY_CODE, START, END)
            if data is not None:
                save_series(data, file_path, country_code=COUNTRY_CODE)
                logger.info(f"✓ Saved {COUNTRY_CODE}_day_ahead_price.csv")
                self.fetch_report["prices/day_ahead_price"] = "SUCCESS"
            else:
                logger.warning("✗ Failed to fetch day_ahead_prices")
                self.fetch_report["prices/day_ahead_price"] = "FAILED"

    def process_metadata(self) -> None:
        """
        Xử lý tạo dữ liệu Calendar/Metadata
        """
        logger.info("=" * 50)
        logger.info("Processing Metadata")
        logger.info("=" * 50)

        if not FETCH_CONFIG.get("zone_metadata", True):
            logger.info("Zone metadata is disabled in config")
            return

        output_dir = DATA_DIRECTORIES["metadata"]
        ensure_dir(output_dir)

        # Calendar file
        file_path = os.path.join(output_dir, "calendar.csv")

        if not self.force_fetch and self.check_data_exists(file_path):
            logger.info("✓ calendar.csv already exists, skipping")
            self.fetch_report["metadata/calendar"] = "SKIPPED"
        else:
            try:
                calendar = pd.date_range(start=START, end=END, freq="h", tz="UTC")
                calendar_df = pd.DataFrame({
                    "timestamp": calendar,
                    "hour": calendar.hour,
                    "day_of_week": calendar.dayofweek,
                    "day": calendar.day,
                    "month": calendar.month,
                    "year": calendar.year,
                    "is_weekend": calendar.dayofweek >= 5
                })

                save_dataframe(calendar_df, file_path)
                logger.info("✓ Saved calendar.csv")
                self.fetch_report["metadata/calendar"] = "SUCCESS"
            except Exception as e:
                logger.error(f"Error creating calendar: {e}")
                self.fetch_report["metadata/calendar"] = "FAILED"

        # Zone metadata file (info về COUNTRY_CODE)
        if FETCH_CONFIG.get("resolution_check", True):
            try:
                zone_info = {
                    "country_code": [COUNTRY_CODE],
                    "fetch_date": [pd.Timestamp.now(tz="UTC")],
                    "data_start": [START],
                    "data_end": [END],
                    "is_forecast_supported": [COUNTRY_CODE in FORECAST_SUPPORTED_ZONES]
                }
                zone_df = pd.DataFrame(zone_info)
                zone_path = os.path.join(output_dir, f"{COUNTRY_CODE}_info.csv")
                save_dataframe(zone_df, zone_path)
                logger.info(f"✓ Saved {COUNTRY_CODE}_info.csv")
            except Exception as e:
                logger.warning(f"Warning saving zone info: {e}")

    def fetch_all(self) -> None:
        """
        Lấy toàn bộ dữ liệu
        """
        logger.info("\n")
        logger.info("=" * 50)
        logger.info(" STARTING DATA FETCH ".center(50))
        logger.info(f"Force Fetch: {str(self.force_fetch):6} ".ljust(50))
        logger.info("=" * 50)
        logger.info("\n")

        self.process_generation_actual()
        self.process_generation_forecast()
        self.process_load()
        self.process_capacity()
        self.process_prices()
        self.process_metadata()

        self.print_report()

    def print_report(self) -> None:
        """
        In báo cáo kết quả lấy dữ liệu
        """
        logger.info("\n")
        logger.info("=" * 50)
        logger.info(" FETCH REPORT ".center(50))
        logger.info("=" * 50)

        success_count = sum(1 for v in self.fetch_report.values() if v == "SUCCESS")
        skipped_count = sum(1 for v in self.fetch_report.values() if v == "SKIPPED")
        failed_count = sum(1 for v in self.fetch_report.values() if v == "FAILED")

        for key, status in sorted(self.fetch_report.items()):
            symbol = "OK" if status == "SUCCESS" else ("SKIP" if status == "SKIPPED" else "FAIL")
            status_text = f"[{symbol}] {status:8}".ljust(18)
            logger.info(f" {key:30} {status_text}")

        logger.info("=" * 50)
        logger.info(f" Total: {success_count} SUCCESS, {skipped_count} SKIPPED, {failed_count} FAILED".ljust(50))
        logger.info("=" * 50)
