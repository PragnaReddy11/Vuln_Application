import json
import sys

RESULT_JSON_PATH = "/home/student/gr8scope/semgrep/"

def check_scan_errors(scan: dict):
    if len(scan.get("errors")) != 0:
        print("Scan failed with errors.")
        return
    print("Scan successfully executed.")

def check_paths_scanned(scan: dict):
    paths_scanned = scan.get("paths").get("scanned")
    if len(paths_scanned) == 1 and paths_scanned[0].endswith("app.py"):
        print("Code was successfully scanned.")
        return
    print("Wrong file was scanned with semgrep.")

def check_results(scan: dict):
    results = scan.get("results")
    if len(results) > 0 and results[0].get("check_id").endswith("sql-injection"):
        print("SQL injection was successfully detected. Hooray!")
        return
    print("Failed to detect SQL injection.")

if __name__ == "__main__":
    with open(RESULT_JSON_PATH, "r") as f:
        scan = json.load(f)
        check_scan_errors(scan)
        check_paths_scanned(scan)
        check_results(scan)

