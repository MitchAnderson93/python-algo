import os
import sys
import subprocess
import argparse
from art import text2art

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run the CLI application.")
parser.add_argument('--logs', action='store_true', help="Enable debug mode")
args = parser.parse_args()

# Set the DEBUG environment variable based on the --log flag
if args.logs:
    os.environ['DEBUG'] = 'true'
else:
    os.environ['DEBUG'] = 'false'

# Import the db_path from common
from system.common import db_path, log_message

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
        log_message("Error: system/setup.py not found.") 

def run_update_script():
    """Run the update logic in system/setup.py."""
    setup_path = os.path.join(os.path.dirname(__file__), "system", "setup.py")
    if os.path.exists(setup_path):
        subprocess.run(["python", setup_path])
    else:
        log_message("Error: system/setup.py not found.")

def list_tasks():
    """List all .py files in the ./tasks/ directory."""
    tasks_dir = os.path.join(os.path.dirname(__file__), "tasks")
    if not os.path.exists(tasks_dir):
        log_message("Error: tasks directory not found.")
        return []

    tasks = [f for f in os.listdir(tasks_dir) if f.endswith('.py')]
    return tasks

def run_task(task_name):
    """Run a specified task from the ./tasks/ directory."""
    tasks_dir = os.path.join(os.path.dirname(__file__), "tasks")
    task_path = os.path.join(tasks_dir, task_name)
    if os.path.exists(task_path):
        subprocess.run(["python", task_path])
    else:
        log_message(f"Error: {task_name} not found in tasks directory.")

# Main functions
def display_menu(database_exists):
    """Display the appropriate menu based on database existence."""
    heading = text2art("PythonAlgo Tools", font="small")
    print(heading)
    if database_exists:
        print("1. Update Data Source")
        print("2. List and Run Tasks")
        print("3. Exit")
    else:
        print("1. Build New Data Source")
        print("\nYou need to build a data source to access more features.")

def main():
    while True:
        database_exists = check_database()
        display_menu(database_exists)
        choice = input("Enter your choice: ").strip()

        if not database_exists:
            if choice == "1":
                user_input = input("This will create a new database. Proceed? (Y/N): ").strip().lower()
                if user_input in ["y", "yes", ""]:
                    run_setup_script()
                else:
                    print("Skipping setup. Exiting...")
                    break
            else:
                print("Invalid choice. You need to build a data source first.")
        else:
            if choice == "1":
                log_message("Updating data source...")
                run_update_script()

            elif choice == "2":
                tasks = list_tasks()
                if tasks:
                    print("\nAvailable tasks:")
                    for i, task in enumerate(tasks, 1):
                        print(f"{i}. {task}")

                    task_input = input("\nEnter the number of the task you want to run: ").strip()
                    if task_input.isdigit() and 1 <= int(task_input) <= len(tasks):
                        run_task(tasks[int(task_input) - 1])
                    else:
                        print("Invalid selection.")
                else:
                    print("No tasks available.")

            elif choice == "3":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()