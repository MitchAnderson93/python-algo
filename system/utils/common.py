import os 

# Shared utilities
def log_message(message):
    if os.getenv('DEBUG', 'false').lower() == 'true':
        print(f"[LOG]: {message}")