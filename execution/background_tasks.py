import concurrent.futures
from typing import Callable, Any

# GLOBAL TACTICAL EXECUTOR
# This pool handles all non-blocking cloud missions in the background.
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

def run_in_background(func: Callable, *args, **kwargs) -> None:
    """
    Executes a function in the background thread pool without blocking the main engine flow.
    """
    try:
        _executor.submit(func, *args, **kwargs)
    except Exception as e:
        print(f"[BackgroundTask] ⚠️ Failed to queue background mission: {e}")
