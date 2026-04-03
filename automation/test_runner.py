import json
import random
import requests
import time
import logging
import time
import datetime

def call_api_with_retry(log, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post("http://ml-service:8000/analyze", json=log)
            return response.json()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return {"status": "Failed", "error": str(e)}

# ✅ Logging setup
logging.basicConfig(
    filename="/app/test_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

failures = [
    {"type": "element_not_found", "message": "NoSuchElementException"},
    {"type": "timeout", "message": "TimeoutException"},
    {"type": "assertion_error", "message": "Expected value mismatch"},
]

def run_test():
    return random.choice(failures + [{"type": "success"}])

if __name__ == "__main__":
    time.sleep(5)

    results = [run_test() for _ in range(5)]

    category_counts = {}
    final_results = []

    for log in results:
        if log.get("type") == "success":
            msg = "PASSED"
            print(f"{msg} ✅")
            logging.info(msg)
            continue

        try:
            result = call_api_with_retry(log)
            cat = result.get("category", "Unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1

            final_results.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "input": log,
                "output": result
            })

            print(result)
            logging.info(f"Input: {log} | Output: {result}")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
    
    total = len(results)
    passed = sum(1 for r in results if r.get("type") == "success")
    failed = total - passed

    summary = f"TOTAL: {total}, PASSED: {passed}, FAILED: {failed}"

    print(summary)
    logging.info(summary)
    print("Failure Categories:", category_counts)
    logging.info(f"Failure Categories: {category_counts}")

    with open("/app/final_results.json", "w") as f:
        json.dump(final_results, f, indent=4)