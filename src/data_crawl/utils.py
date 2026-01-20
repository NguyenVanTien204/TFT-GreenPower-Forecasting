"""
Các hàm utility cho xử lý dữ liệu
"""
import os
import pandas as pd
from typing import Union


def ensure_dir(path: str) -> None:
    """
    Tạo thư mục nếu nó chưa tồn tại

    Args:
        path: Đường dẫn thư mục
    """
    os.makedirs(path, exist_ok=True)


def save_series(series: Union[pd.Series, pd.DataFrame], path: str, country_code: str = None) -> None:
    """
    Lưu pandas Series hoặc DataFrame thành file CSV

    Args:
        series: Pandas Series hoặc DataFrame cần lưu
        path: Đường dẫn file lưu
        country_code: Mã quốc gia (nếu có sẽ thêm vào tên file)
    """
    # Nếu có country_code, thêm vào tên file
    if country_code:
        dir_name = os.path.dirname(path)
        file_name = os.path.basename(path)
        name_without_ext = os.path.splitext(file_name)[0]
        path = os.path.join(dir_name, f"{country_code}_{name_without_ext}.csv")

    ensure_dir(os.path.dirname(path))

    # Nếu là DataFrame, lưu trực tiếp
    if isinstance(series, pd.DataFrame):
        if series.index.name is None:
            series.index.name = "timestamp"
        series.to_csv(path)
    # Nếu là Series, chuyển sang DataFrame
    else:
        series_df = series.to_frame(name="value")
        series_df.index.name = "timestamp"
        series_df.to_csv(path)


def save_dataframe(df: pd.DataFrame, path: str, country_code: str = None) -> None:
    """
    Lưu pandas DataFrame thành file CSV

    Args:
        df: Pandas DataFrame cần lưu
        path: Đường dẫn file lưu
        country_code: Mã quốc gia (nếu có sẽ thêm vào tên file)
    """
    # Nếu có country_code, thêm vào tên file
    if country_code:
        dir_name = os.path.dirname(path)
        file_name = os.path.basename(path)
        name_without_ext = os.path.splitext(file_name)[0]
        path = os.path.join(dir_name, f"{country_code}_{name_without_ext}.csv")

    ensure_dir(os.path.dirname(path))
    df.to_csv(path)


def file_exists(path: str) -> bool:
    """
    Kiểm tra file có tồn tại không

    Args:
        path: Đường dẫn file

    Returns:
        True nếu file tồn tại, False nếu không
    """
    return os.path.isfile(path)


def get_file_size(path: str) -> int:
    """
    Lấy kích thước file (bytes)

    Args:
        path: Đường dẫn file

    Returns:
        Kích thước file (bytes), hoặc 0 nếu file không tồn tại
    """
    if file_exists(path):
        return os.path.getsize(path)
    return 0
