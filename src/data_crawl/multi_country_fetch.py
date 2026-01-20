"""
Script ví dụ để fetch dữ liệu cho nhiều quốc gia
"""
import pandas as pd
from data_manager import DataManager
import config

# Cấu hình
START_DATE = pd.Timestamp("2024-01-01", tz="UTC")
END_DATE = pd.Timestamp("2024-12-31", tz="UTC")

# Danh sách quốc gia cần fetch
COUNTRIES = [
    "DE_LU",  # Germany-Luxembourg
    "FR",     # France
    "ES",     # Spain
    "IT",     # Italy
    "GB",     # Great Britain
]

def fetch_multi_country():
    """
    Fetch dữ liệu cho nhiều quốc gia
    """
    print("\n" + "="*70)
    print("MULTI-COUNTRY DATA FETCH".center(70))
    print("="*70)
    print(f"\nCountries: {', '.join(COUNTRIES)}")
    print(f"Period: {START_DATE.date()} to {END_DATE.date()}")
    print("\n" + "="*70 + "\n")

    results = {}

    for country in COUNTRIES:
        print(f"\n{'='*70}")
        print(f"Fetching data for {country}".center(70))
        print(f"{'='*70}\n")

        # Cập nhật config
        config.COUNTRY_CODE = country
        config.START = START_DATE
        config.END = END_DATE

        try:
            # Tạo manager và fetch (không force, chỉ lấy dữ liệu còn thiếu)
            manager = DataManager(force_fetch=False)
            manager.fetch_all()

            # Lưu kết quả
            success_count = sum(1 for v in manager.fetch_report.values() if v == "SUCCESS")
            skipped_count = sum(1 for v in manager.fetch_report.values() if v == "SKIPPED")
            failed_count = sum(1 for v in manager.fetch_report.values() if v == "FAILED")

            results[country] = {
                "success": success_count,
                "skipped": skipped_count,
                "failed": failed_count
            }

        except Exception as e:
            print(f"\n❌ Error fetching data for {country}: {e}")
            results[country] = {
                "success": 0,
                "skipped": 0,
                "failed": 0,
                "error": str(e)
            }

    # In tổng kết
    print("\n" + "="*70)
    print("SUMMARY REPORT".center(70))
    print("="*70 + "\n")

    for country, stats in results.items():
        if "error" in stats:
            print(f"{country:8} - ❌ ERROR: {stats['error']}")
        else:
            print(f"{country:8} - ✅ SUCCESS: {stats['success']:2d} | "
                  f"⊘ SKIPPED: {stats['skipped']:2d} | "
                  f"❌ FAILED: {stats['failed']:2d}")

    print("\n" + "="*70)
    total_success = sum(s.get("success", 0) for s in results.values())
    total_skipped = sum(s.get("skipped", 0) for s in results.values())
    total_failed = sum(s.get("failed", 0) for s in results.values())

    print("\nTotal across all countries:")
    print(f"  SUCCESS: {total_success}")
    print(f"  SKIPPED: {total_skipped}")
    print(f"  FAILED:  {total_failed}")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    fetch_multi_country()
