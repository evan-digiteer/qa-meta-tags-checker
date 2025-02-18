from src.config import Config
from src.meta_checker import MetaChecker
from src.report_generator import ReportGenerator
import time

def main():
    checker = MetaChecker()
    results = []
    start_time = time.time()
    total_urls = len(Config.URLS)

    print(f"Starting meta tags check for {total_urls} URLs...")
    
    try:
        for i, url in enumerate(Config.URLS, 1):
            url = url.strip()
            print(f"\nChecking {url}")
            result = checker.check_meta_tags(url)
            results.append(result)
            print(f"Progress: {(i/total_urls)*100:.0f}%")
    finally:
        checker.close()

    elapsed_time = time.time() - start_time
    print(f"\nAll URLs processed in {elapsed_time:.2f} seconds")

    print("Generating report...")
    report_generator = ReportGenerator()
    report_path = report_generator.generate_report(results)
    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    main()
