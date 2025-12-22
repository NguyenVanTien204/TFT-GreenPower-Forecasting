"""
File chính - Điều khiển quá trình lấy dữ liệu
"""
import sys
from data_manager import DataManager


def main():
    """
    Hàm chính

    Cách sử dụng:
        python main.py                # Lấy dữ liệu thiếu (bỏ qua dữ liệu đã có)
        python main.py --force        # Lấy lại tất cả dữ liệu
    """

    print("Starting ENTSO-E Data Fetcher...")

    # Kiểm tra arguments
    force_fetch = "--force" in sys.argv or "-f" in sys.argv

    if force_fetch:
        print("WARNING: Running in FORCE FETCH mode - all data will be re-downloaded")
        print("")

    # Tạo DataManager và lấy dữ liệu
    manager = DataManager(force_fetch=force_fetch)
    manager.fetch_all()

    print("\nData fetch completed!")


if __name__ == "__main__":
    main()
