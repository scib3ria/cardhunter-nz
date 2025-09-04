import re
import time
from functools import wraps

def retry_sync(max_attempts=3, backoff_factor=1.0):
    """
    Retry a synchronous function up to `max_attempts` times
    with a delay between attempts.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    sleep_time = backoff_factor * (2 ** (attempt - 1))
                    print(f"[RETRY] {func.__name__} failed: {e}. Retrying in {sleep_time:.1f}s...")
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def clean_price(value):
    if isinstance(value, (int, float)):
        return float(value)
    value = str(value).replace('$', '').replace(',', '').replace('*', '').replace('!', '').strip()
    try:
        return float(value)
    except ValueError:
        return 0.0

def clean_quantity(value):
    if isinstance(value, int):
        return value
    value = str(value).strip()
    # Handle cases like '8+' by removing non-digit characters
    value = re.sub(r'\D+', '', value)
    try:
        return int(value)
    except ValueError:
        return 0
