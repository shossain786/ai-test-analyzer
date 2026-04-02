from fastapi import FastAPI

app = FastAPI()

def classify_failure(message: str):
    if "NoSuchElement" in message:
        return "Locator Issue"
    elif "Timeout" in message:
        return "Performance Issue"
    elif "AssertionError" in message:
        return "Assertion Issue"
    elif "500" in message:
        return "Server Issue"
    elif "ConnectionError" in message:
        return "Network Issue"
    return "Unknown"

@app.post("/analyze")
def analyze(log: dict):
    if log.get("type") == "success":
        return {"status": "Passed"}

    category = classify_failure(log.get("message", ""))
    return {
        "status": "Failed",
        "category": category
    }