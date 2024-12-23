import os
import sys
import subprocess
import argparse

# Add the project root to sys.path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run the CLI application.")
parser.add_argument('--debug', action='store_true', help="Enable debug mode")
args = parser.parse_args()

# Set the DEBUG environment variable based on the --debug flag
if args.debug:
    os.environ['DEBUG'] = 'true'
else:
    os.environ['DEBUG'] = 'false'

# Import the db_path from common
from system.common import db_path

# Setup functions
def check_database():
    """Check if the SQLite database exists."""
    return os.path.exists(db_path)

def run_setup_script():
    """Run the system/setup.py script."""
    setup_path = os.path.join(os.path.dirname(__file__), "system", "setup.py")
    if os.path.exists(setup_path):
        subprocess.run(["python", setup_path])
    else:
        print("Error: system/setup.py not found.")

def run_update_script():
    """Run the update logic in system/setup.py."""
    setup_path = os.path.join(os.path.dirname(__file__), "system", "setup.py")
    if os.path.exists(setup_path):
        subprocess.run(["python", setup_path])
    else:
        print("Error: system/setup.py not found.")

# Main functions
def main():
    # Check if the database exists
    if check_database():
        print("\nDatabase found at './db.sqlite'.")
        user_input = input("Do you want to update the database? This will fetch new stock metrics (Y/N): ").strip().lower()
        if user_input in ["y", "yes", ""]:
            run_update_script()
        else:
            print("\nProceeding without updating the database.")
    else:
        print("\nDatabase not found at './db.sqlite'.")
        user_input = input("Do you want to setup a new project? This will create the database (Y/N): ").strip().lower()
        if user_input in ["y", "yes", ""]:
            run_setup_script()
        else:
            print("Exiting...")
            return

    print("\nProcess complete. Exiting...")

if __name__ == "__main__":
    main()