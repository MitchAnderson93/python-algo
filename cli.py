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
    if (os.path.exists(setup_path)):
        subprocess.run(["python", setup_path])
    else:
        log_message("Error: system/setup.py not found.") 

def run_update_script():
    """Run the update logic in system/setup.py."""
    setup_path = os.path.join(os.path.dirname(__file__), "system", "setup.py")
    if (os.path.exists(setup_path)):
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

def list_reports():
    """List all .py files in the ./reports/ directory."""
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        log_message("Error: reports directory not found.")
        return []

    reports = [f for f in os.listdir(reports_dir) if f.endswith('.py')]
    return reports

def run_report(report_name):
    """Run a specified report from the ./reports/ directory."""
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    report_path = os.path.join(reports_dir, report_name)
    if os.path.exists(report_path):
        subprocess.run(["python", report_path])
    else:
        log_message(f"Error: {report_name} not found in reports directory.")

def list_libs():
    """List all directories in the ./system/lib/functions/ directory."""
    libs_dir = os.path.join(os.path.dirname(__file__), "system", "lib", "functions")
    if not os.path.exists(libs_dir):
        log_message("Error: libs directory not found.")
        return []

    libs = [d for d in os.listdir(libs_dir) if os.path.isdir(os.path.join(libs_dir, d))]
    return libs

def run_lib_script(lib_name):
    """Run a specified lib script from the ./system/lib/functions/ directory."""
    lib_path = os.path.join(os.path.dirname(__file__), "system", "lib", "functions", lib_name, "cli.py")
    if os.path.exists(lib_path):
        subprocess.run(["python", lib_path])
    else:
        log_message(f"Error: {lib_name} CLI script not found in lib directory.")

def run_function_script(lib_name):
    """Run a specified function script from the ./system/lib/functions/ directory."""
    lib_path = os.path.join(os.path.dirname(__file__), "system", "lib", "functions", lib_name, "cli.py")
    if os.path.exists(lib_path):
        # Print expected input format for the selected function
        subprocess.run(["python", lib_path, "--print-expected-input"])
        
        # Prompt user for input values
        user_input = input("Enter the values in the expected format: ").strip()
        input_values = user_input.split()
        
        # Run the function script with the provided input values
        subprocess.run(["python", lib_path] + input_values)
    else:
        log_message(f"Error: {lib_name} CLI script not found in functions directory.")

# Main functions
def display_menu(database_exists):
    """Display the appropriate menu based on database existence."""
    heading = text2art("Python Tools", font="small")
    print(heading)
    if database_exists:
        print("1. Tasks")
        print("2. Functions")
        print("3. Reports")
        print("4. Update data source (sqlite)")
        print("5. Exit")
    else:
        print("1. Build local data source (sqlite)")
        print("\nYou need to build a data source to access more features.")

def main():
    while True:
        database_exists = check_database()
        display_menu(database_exists)
        choice = input("Enter your choice: ").strip()

        if not database_exists:
            if choice == "1":
                user_input = input("This will create a new database (sqlite). Proceed? (Y/N): ").strip().lower()
                if user_input in ["y", "yes", ""]:
                    run_setup_script()
                else:
                    print("Skipping setup. Exiting...")
                    break
            else:
                print("Invalid choice. You need to build a data source first.")
        else:
            if choice == "4":
                log_message("Updating data source...")
                run_update_script()

            elif choice == "1":
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

            elif choice == "2":
                libs = list_libs()
                if libs:
                    print("\nAvailable functions:")
                    for i, lib in enumerate(libs, 1):
                        print(f"{i}. {lib}")

                    lib_input = input("\nEnter the number of the function you want to run: ").strip()
                    if lib_input.isdigit() and 1 <= int(lib_input) <= len(libs):
                        run_function_script(libs[int(lib_input) - 1])
                    else:
                        print("Invalid selection.")
                else:
                    print("No functions available.")

            elif choice == "3":
                reports = list_reports()
                if reports:
                    print("\nAvailable reports:")
                    for i, report in enumerate(reports, 1):
                        print(f"{i}. {report}")

                    report_input = input("\nEnter the number of the report you want to run: ").strip()
                    if report_input.isdigit() and 1 <= int(report_input) <= len(reports):
                        run_report(reports[int(report_input) - 1])
                    else:
                        print("Invalid selection.")
                else:
                    print("No reports available.")

            elif choice == "5":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()