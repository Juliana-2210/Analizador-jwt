# utils.py
import time
def now_ts() -> int:
    return int(time.time())

def make_standard_header(alg: str = "HS256") -> dict:
    return {"alg": alg, "typ": "JWT"}
