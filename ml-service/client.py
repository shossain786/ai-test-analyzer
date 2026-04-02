import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_DIR, "logs", "results.json")

with open(log_path) as f:
    logs = json.load(f)

for log in logs:
    if log.get("status") == "passed":
        print(f"{log['test_name']} → PASSED ✅")
        print("-" * 40)
        continue

    response = requests.post("http://127.0.0.1:8000/analyze", json=log)
    
    print(f"Test: {log['test_name']}")
    print(f"Error: {log['message']}")
    print(f"AI Result: {response.json()}")
    print("-" * 40)