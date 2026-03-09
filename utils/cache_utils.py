import fastf1
import os
import logging

# Suppress FastF1 info logs
# logging.getLogger("fastf1").setLevel(logging.WARNING)

def set_cache(cache_dir: str):
    cache_path = os.path.join(os.getcwd(), cache_dir)
    os.makedirs(cache_path, exist_ok=True)
    fastf1.Cache.enable_cache(cache_path)