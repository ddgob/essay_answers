"""
This module provides a class for checking code quality using mypy and 
pytest.

It searches for Python files in the current directory and its 
subdirectories, runs type checks with mypy, and runs tests with pytest.
"""

import subprocess
import os
import re

class CodeQualityChecker:
    """
    A class to check the code quality of Python files using mypy and 
    pytest.

    This class encapsulates the logic for finding Python files, running
    type checks with mypy, and executing tests with pytest. It provides
    methods to perform these operations and handles the output of each
    command.
    """

    def __init__(self):
        """Initialize the CodeQualityChecker instance."""
        self.py_files = []

    def find_python_files(self):
        """
        Find all Python (.py) files in the current directory and 
        subdirectories.

        This method searches the directory tree starting from the 
        current directory and stores the paths of all found Python files
        in the instance variable `self.py_files`.
        """
        print("Searching for Python files...")
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py'):
                    self.py_files.append(os.path.join(root, file))

    def run_mypy(self):
        """
        Run mypy on the found Python files.

        This method executes mypy on all the Python files found in the
        directory. It checks for type errors and outputs the results.

        Returns:
            bool: True if mypy succeeded, False otherwise.
        """
        self.find_python_files()

        if self.py_files:
            print(f"Running mypy on {len(self.py_files)} file(s)...")
            result = subprocess.run(['mypy'] + self.py_files, capture_output=True,
                                    text=True, check=False
                                    )

            # Check if mypy succeeded
            if result.returncode != 0:
                print("mypy failed, aborting commit.")
                print(result.stdout)
                print(result.stderr)
                return False
            else:
                print("mypy completed successfully. Typing is correct!")
        else:
            print("No Python files found.")
        return True

    def run_pytest(self):
        """
        Run pytest to check the tests.

        This method executes pytest to run all tests in the current 
        project and outputs the results.

        Returns:
            bool: True if pytest succeeded, False otherwise.
        """
        print("Running pytest...")
        result = subprocess.run(['pytest'], capture_output=True, text=True)

        # Check if pytest succeeded
        if result.returncode != 0:
            print("pytest failed, aborting commit.")
            print(result.stdout)
            print(result.stderr)
            return False
        else:
            passed_tests = re.search(r"(\d+) passed", result.stdout)
            if passed_tests:
                num_passed = passed_tests.group(1)
                print(f"pytest completed successfully. All {num_passed} tests passed!")
            else:
                print("pytest completed successfully. No tests were run.")
        return True

    def run_checks(self):
        """
        Run both mypy and pytest checks together.

        This method executes mypy and pytest in sequence. It reports
        whether both checks passed successfully.

        If either mypy or pytest fails, an appropriate message is 
        printed and the process is aborted.
        """
        
        if self.run_mypy() and self.run_pytest():
            print("All checks passed successfully.")
        else:
            print("One or more checks failed.")

if __name__ == "__main__":
    checker = CodeQualityChecker()
    checker.run_checks()
