import subprocess
import os
from server.settings import (
    CPP_COMPILER, CPP_COMPILE_FLAGS, JAVA_COMPILER, JAVA_COMPILE_FLAGS
)

class Compiler:

    @staticmethod
    def compile_cpp(source_path, output_path):
        try:
            cmd = [CPP_COMPILER] + CPP_COMPILE_FLAGS + [source_path, "-o", output_path]
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return {"success": True, "error": ""}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.output.decode()}

    @staticmethod
    def compile_java(source_path):
        try:
            cmd = [JAVA_COMPILER] + JAVA_COMPILE_FLAGS + [source_path]
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return {"success": True, "error": ""}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.output.decode()}
