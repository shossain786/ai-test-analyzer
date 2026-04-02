import json
import random
import requests
import time

failures = [
    {"type": "element_not_found", "message": "NoSuchElementException"},
    {"type": "timeout", "message": "TimeoutException"},
    {"type": "assertion_error", "message": "Expected value mismatch"},
]

def run_test():
    return random.choice(failures + [{"type": "success"}])

if __name__ == "__main__":
    time.sleep(5)  # wait for ml-service

    results = [run_test() for _ in range(5)]

    for log in results:
        if log.get("type") == "success":
            print("PASSED ✅")
            continue

        response = requests.post("http://ml-service:8000/analyze", json=log)
        print(response.json())