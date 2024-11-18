import json

RESULT_PATH = "/home/student/gr8scope/semgrep/results.json"

def check_scan_errors(scan: dict):
    if len(scan.get("errors")) != 0:
        print("❌ Check #1 - Semgrep scan failed with errors: 0 points.")
        return
    print("✅ Check #2 - Semgrep scan has no errors: +10 points.")

def check_paths_scanned(scan: dict):
    paths_scanned = scan.get("paths").get("scanned")
    if len(paths_scanned) == 1 and paths_scanned[0].endswith("app.py"):
        print("✅ Check #2 - Semgrep scanned app.py: +10 points.")
        return
    print("❌ Check #2 - Semgrep did not scan app.py: 0 points.")

def check_results(scan: dict):
    results = scan.get("results")
    if len(results) > 0 and results[0].get("check_id").endswith("sql-injection"):
        print("✅ Check #3 - Semgrep detected SQLi: +10 points.")
        return
    print("❌ Check #3 - Semgrep did not detect SQLi: 0 points.")

if __name__ == "__main__":
    with open(RESULT_PATH, "r") as f:
        scan = json.load(f)
        check_scan_errors(scan)
        check_paths_scanned(scan)
        check_results(scan)
