from common import os, sys, processed_path, datetime
from utils.common import log_message

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Initial setup code
current_date = datetime.now().strftime("%Y%m%d")
folder_path = os.path.join(processed_path, current_date)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

log_message("Initial setup completed.")

# Call the custom setup script
custom_setup_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../custom_setup/custom_setup.py"))
if os.path.exists(custom_setup_path):
    log_message("Custom setup script found. Running custom setup...")
    exec(open(custom_setup_path).read())
else:
    log_message("Custom setup script not found.")