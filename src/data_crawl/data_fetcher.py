"""
Các hàm fetch dữ liệu từ ENTSO-E API
Cập nhật theo entsoe-py v0.7.8+ documentation (2025)
"""
import pandas as pd
from entsoe import EntsoePandasClient
from typing import Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """
    Lớp để fetch dữ liệu từ ENTSO-E API
    Sử dụng EntsoePandasClient từ thư viện entsoe-py
    """

    def __init__(self, api_key: str):
        """
        Khởi tạo DataFetcher

        Args:
            api_key: ENTSO-E API key
        """
        self.client = EntsoePandasClient(api_key=api_key)

    def fetch_generation_actual(
        self,
        country_code: str,
        start: pd.Timestamp,
        end: pd.Timestamp,
        gen_types: Dict[str, str]
    ) -> Dict[str, pd.DataFrame]:
        """
        Lấy dữ liệu Generation Actual cho các loại nguồn năng lượng
        API Method: query_generation() returns DataFrame

        Args:
            country_code: Mã nước (bidding zone code)
            start: Ngày bắt đầu (with timezone)
            end: Ngày kết thúc (with timezone)
            gen_types: Dict tên file -> psr_type (e.g., "Solar", "Wind Onshore")

        Returns:
            Dict tên file -> DataFrame với dữ liệu generation
        """
        results = {}

        for fname, gen_type in gen_types.items():
            try:
                logger.info(f"Fetching actual generation: {gen_type}")
                data = self.client.query_generation(
                    country_code=country_code,
                    start=start,
                    end=end,
                    psr_type=gen_type
                )
                results[fname] = data
            except Exception as e:
                logger.error(f"Error fetching {gen_type}: {str(e)[:200]}")
                results[fname] = None

        return results

    def fetch_solar_forecast(
        self,
        country_code: str,
        start: pd.Timestamp,
        end: pd.Timestamp
    ) -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu Solar Forecast
        API Method: query_wind_and_solar_forecast() returns DataFrame

        Args:
            country_code: Mã nước
            start: Ngày bắt đầu
            end: Ngày kết thúc

        Returns:
            DataFrame với dữ liệu forecast hoặc None nếu có lỗi
        """
        try:
            logger.info("Fetching solar forecast")
            data = self.client.query_wind_and_solar_forecast(
                country_code=country_code,
                start=start,
                end=end,
                psr_type="B16"  # Solar PSR code
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching solar forecast: {str(e)[:200]}")
            return None

    def fetch_wind_forecast(
        self,
        country_code: str,
        start: pd.Timestamp,
        end: pd.Timestamp
    ) -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu Wind Forecast
        API Method: query_wind_and_solar_forecast() returns DataFrame

        Args:
            country_code: Mã nước
            start: Ngày bắt đầu
            end: Ngày kết thúc

        Returns:
            DataFrame với dữ liệu forecast hoặc None nếu có lỗi
        """
        try:
            logger.info("Fetching wind forecast")
            data = self.client.query_wind_and_solar_forecast(
                country_code=country_code,
                start=start,
                end=end,
                psr_type="B19"  # Wind Onshore PSR code
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching wind forecast: {str(e)[:200]}")
            return None

    def fetch_load_actual(
        self,
        country_code: str,
        start: pd.Timestamp,
        end: pd.Timestamp
    ) -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu Load Actual
        API Method: query_load() returns DataFrame

        Args:
            country_code: Mã nước
            start: Ngày bắt đầu
            end: Ngày kết thúc

        Returns:
            DataFrame với dữ liệu load hoặc None nếu có lỗi
        """
        try:
            logger.info("Fetching total load actual")
            data = self.client.query_load(
                country_code=country_code,
                start=start,
                end=end
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching load actual: {str(e)[:200]}")
            return None

    def fetch_load_forecast(
        self,
        country_code: str,
        start: pd.Timestamp,
        end: pd.Timestamp
    ) -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu Load Forecast
        API Method: query_load_forecast() returns DataFrame

        Args:
            country_code: Mã nước
            start: Ngày bắt đầu
            end: Ngày kết thúc

        Returns:
            DataFrame với dữ liệu forecast hoặc None nếu có lỗi
        """
        try:
            logger.info("Fetching total load forecast")
            data = self.client.query_load_forecast(
                country_code=country_code,
                start=start,
                end=end
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching load forecast: {str(e)[:200]}")
            return None

    def fetch_installed_capacity(
        self,
        country_code: str,
        start: pd.Timestamp,
        end: pd.Timestamp
    ) -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu Installed Generation Capacity
        API Method: query_installed_generation_capacity() returns DataFrame
        Note: Kết quả luôn theo năm (year-based data)

        Args:
            country_code: Mã nước
            start: Ngày bắt đầu
            end: Ngày kết thúc

        Returns:
            DataFrame với dữ liệu capacity hoặc None nếu có lỗi
        """
        try:
            logger.info("Fetching installed generation capacity")
            data = self.client.query_installed_generation_capacity(
                country_code=country_code,
                start=start,
                end=end,
                psr_type=None  # None = tất cả loại generation
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching installed capacity: {str(e)[:200]}")
            return None

    def fetch_unavailable_capacity(
        self,
        country_code: str,
        start: pd.Timestamp,
        end: pd.Timestamp
    ) -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu Unavailability of Generation Units
        API Method: query_unavailability_of_generation_units() returns DataFrame

        Args:
            country_code: Mã nước
            start: Ngày bắt đầu
            end: Ngày kết thúc

        Returns:
            DataFrame với dữ liệu unavailability hoặc None nếu có lỗi
        """
        try:
            logger.info("Fetching unavailable capacity")
            data = self.client.query_unavailability_of_generation_units(
                country_code=country_code,
                start=start,
                end=end,
                docstatus=None,  # None = tất cả status
                periodstartupdate=None,
                periodendupdate=None
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching unavailable capacity: {str(e)[:200]}")
            return None

    def fetch_day_ahead_prices(
        self,
        country_code: str,
        start: pd.Timestamp,
        end: pd.Timestamp
    ) -> Optional[pd.Series]:
        """
        Lấy dữ liệu Day-Ahead Prices (SDAC - Single Day-Ahead Coupling)
        API Method: query_day_ahead_prices() returns Series
        Note: Trả về giá SDAC với resolution chuẩn (60min trước 2025-10-01, 15min sau đó)

        Args:
            country_code: Mã nước
            start: Ngày bắt đầu
            end: Ngày kết thúc

        Returns:
            Series với dữ liệu giá hoặc None nếu có lỗi
        """
        try:
            logger.info("Fetching day-ahead prices")
            data = self.client.query_day_ahead_prices(
                country_code=country_code,
                start=start,
                end=end
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching day-ahead prices: {str(e)[:200]}")
            return None

