import subprocess
import os
from server.settings import (
    PYTHON_EXECUTABLE, JAVA_RUNNER,
    EXECUTION_TIMEOUT, MAX_OUTPUT_LENGTH
)

class Executor:

    @staticmethod
    def run_python(code_path, input_path):
        try:
            result = subprocess.run(
                [PYTHON_EXECUTABLE, code_path],
                input=open(input_path, "r"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=EXECUTION_TIMEOUT,
                text=True
            )
            print("DEBUG EXECUTOR:", result.stdout, result.stderr)

            return result.stdout[:MAX_OUTPUT_LENGTH], result.stderr
        except subprocess.TimeoutExpired:
            return None, "TIMEOUT"

    @staticmethod
    def run_cpp(exec_path, input_path):
        try:
            result = subprocess.run(
                [exec_path],
                input=open(input_path, "r"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=EXECUTION_TIMEOUT,
                text=True
            )
            return result.stdout[:MAX_OUTPUT_LENGTH], result.stderr
        except subprocess.TimeoutExpired:
            return None, "TIMEOUT"

    @staticmethod
    def run_java(class_dir, class_name, input_path):
        try:
            result = subprocess.run(
                [JAVA_RUNNER, "-cp", class_dir, class_name],
                input=open(input_path, "r"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=EXECUTION_TIMEOUT,
                text=True
            )
            return result.stdout[:MAX_OUTPUT_LENGTH], result.stderr
        except subprocess.TimeoutExpired:
            return None, "TIMEOUT"
