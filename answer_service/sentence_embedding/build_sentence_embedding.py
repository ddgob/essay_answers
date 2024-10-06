"""
Module for handling the setup, updating, and building of a CMake project 
that integrates with pybind11. This module provides functionality to:
- Retrieve the pybind11 include path dynamically
- Update the `CMakeLists.txt` file to reflect the correct include path
- Rebuild the project using `cmake` and `make`

It is designed to automate the integration of pybind11 into CMake-based 
projects by programmatically modifying the `CMakeLists.txt` file and 
triggering the build process.

Functions:
    - get_pybind11_include_path: Retrieves the pybind11 include path
    - update_cmake_file: Updates the CMakeLists.txt with the pybind11 
      path
    - build_project: Builds the project by running cmake and make
    - main: Orchestrates the update and build process
"""
import subprocess
import os
import shutil
from typing import Optional, List

# Path to your CMakeLists.txt file and build directory
cmake_file_path: str = 'answer_service/sentence_embedding/CMakeLists.txt'
build_dir: str = 'answer_service/sentence_embedding/build'

def get_pybind11_include_path() -> Optional[str]:
    """
    Retrieve the base path of pybind11 without the '/include' directory
    and without the '-I/' prefix.
    
    Returns:
        The cleaned base path to pybind11, or None if an error occurs.
    """

    try:
        result: subprocess.CompletedProcess = subprocess.run(
            ['python', '-m', 'pybind11', '--includes'],
            capture_output=True, text=True, check=False
        )
        includes_paths: List[str] = result.stdout.strip().split()

        for path in includes_paths:
            if "pybind11" in path:
                base_path: str = path.replace('-I', '').replace('/include', '')
                return base_path
        return None
    except Exception as e:
        print(f"Error getting pybind11 include path: {e}")
        return None

def update_cmake_file(base_path: str) -> None:
    """
    Add or update the set(CMAKE_PREFIX_PATH ...) line in the 
    CMakeLists.txt file to reflect the given base path.

    Args:
        base_path: The base path for pybind11 to add or update in the 
        CMake file.
    """

    set_command: str = f'set(CMAKE_PREFIX_PATH "{base_path}")\n'

    if not os.path.exists(cmake_file_path):
        print(f"{cmake_file_path} does not exist.")
        return

    with open(cmake_file_path, 'r', encoding='utf-8') as file:
        cmake_contents: List[str] = file.readlines()

    prefix_path_exists: bool = False
    for index, line in enumerate(cmake_contents):
        if line.startswith('set(CMAKE_PREFIX_PATH'):
            prefix_path_exists = True
            existing_path: str = line.split('"')[1]
            if existing_path == base_path:
                message = (
                    "The correct CMAKE_PREFIX_PATH is already set in " 
                    f"{cmake_file_path}"
                )
                print(message)
            else:
                cmake_contents[index] = set_command
                print(f"Updated CMAKE_PREFIX_PATH in {cmake_file_path}")
            break

    if not prefix_path_exists:
        with open(cmake_file_path, 'w', encoding='utf-8') as file:
            for line in cmake_contents:
                file.write(line)
                if line.startswith('project'):
                    file.write(set_command)
            print(f"Added {set_command.strip()} to {cmake_file_path}")
    else:
        with open(cmake_file_path, 'w', encoding='utf-8') as file:
            file.writelines(cmake_contents)

def build_project() -> None:
    """
    Rebuild the project by removing the old build directory, 
    creating a new one, and running the `cmake` and `make` commands.
    """

    if os.path.exists(build_dir):
        print(f"Removing existing build directory: {build_dir}")
        shutil.rmtree(build_dir)

    os.makedirs(build_dir)
    print(f"Created build directory: {build_dir}")

    try:
        os.chdir(build_dir)
        print(f"Running cmake in {build_dir}")
        subprocess.run(['cmake', '..'], check=True)
        print("Running make")
        subprocess.run(['make'], check=True)
        print("Build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
    finally:
        os.chdir('../../..')

def main() -> None:
    """
    Main entry point for the script. It retrieves the pybind11 path, 
    updates the CMakeLists.txt if needed, and triggers the build 
    process.
    """

    base_path: Optional[str] = get_pybind11_include_path()
    if base_path:
        update_cmake_file(base_path)
        build_project()
    else:
        print("Failed to get the pybind11 include path.")

if __name__ == "__main__":
    main()
