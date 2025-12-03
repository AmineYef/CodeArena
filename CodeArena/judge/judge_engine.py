

# import subprocess
# import tempfile
# import os
# import sys
# import shutil
# import threading

# TIME_LIMIT = 2      # seconds

# class JudgeEngine:

#     def __init__(self, problems_dir="problems"):
#         self.problems_dir = problems_dir

#     def judge(self, task):

#         problem = task["problem_id"]
#         language = task["language"]
#         code = task["code"]

#         # Paths
#         problem_path = os.path.join(self.problems_dir, problem)
#         input_file = os.path.join(problem_path, "input.txt")
#         output_file = os.path.join(problem_path, "output.txt")

#         # Sanity check
#         if not os.path.exists(input_file):
#             return {"verdict": "INPUT_FILE_MISSING"}

#         if not os.path.exists(output_file):
#             return {"verdict": "OUTPUT_FILE_MISSING"}

#         # Temporary sandbox
#         with tempfile.TemporaryDirectory() as tmp:

#             # Copy test files
#             shutil.copy(input_file, tmp + "/input.txt")
#             shutil.copy(output_file, tmp + "/expected.txt")

#             # Write user code
#             code_path = os.path.join(tmp, "solution")
#             with open(code_path, "w") as f:
#                 f.write(code)

#             input_data = open(tmp + "/input.txt").read()
#             expected = open(tmp + "/expected.txt").read().strip()

#             # Dispatch by language
#             if language == "python":
#                 return self._run_python(code_path, input_data, expected)

#             elif language == "cpp":
#                 exe_path = os.path.join(tmp, "a.exe")
#                 return self._run_cpp(code_path, exe_path, input_data, expected)

#             else:
#                 return {"verdict": "LANGUAGE_NOT_SUPPORTED"}


#     # ------------------ PYTHON --------------------

#     def _run_python(self, code_path, input_data, expected):
#         try:
#             proc = subprocess.Popen(
#                 [sys.executable, code_path],
#                 stdin=subprocess.PIPE,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )

#             # timeout
#             timer = threading.Timer(TIME_LIMIT, proc.kill)
#             timer.start()

#             out, err = proc.communicate(input_data)
#             timer.cancel()

#             if proc.returncode != 0:
#                 return {"verdict": "RUNTIME_ERROR", "error": err.strip()}

#             output = out.strip()

#             if output == expected:
#                 return {"verdict": "OK"}

#             return {
#                 "verdict": "WRONG_ANSWER",
#                 "output": output,
#                 "expected": expected
#             }

#         except Exception as e:
#             return {"verdict": "SYSTEM_ERROR", "error": str(e)}


#     # ------------------ C++ --------------------

#     def _run_cpp(self, code_path, exe_path, input_data, expected):

#         # compile
#         p = subprocess.run(["g++", code_path, "-o", exe_path],
#                            capture_output=True, text=True)

#         if p.returncode != 0:
#             return {"verdict": "COMPILATION_ERROR", "error": p.stderr}

#         try:
#             proc = subprocess.Popen(
#                 [exe_path],
#                 stdin=subprocess.PIPE,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )

#             timer = threading.Timer(TIME_LIMIT, proc.kill)
#             timer.start()

#             out, err = proc.communicate(input_data)
#             timer.cancel()

#             if proc.returncode != 0:
#                 return {"verdict": "RUNTIME_ERROR", "error": err}

#             output = out.strip()

#             if output == expected:
#                 return {"verdict": "OK"}

#             return {
#                 "verdict": "WRONG_ANSWER",
#                 "output": output,
#                 "expected": expected
#             }

#         except Exception as e:
#             return {"verdict": "SYSTEM_ERROR", "error": str(e)}




import subprocess
import tempfile
import os
import sys
import shutil
import threading

TIME_LIMIT = 2  # seconds


class JudgeEngine:

    def __init__(self, problems_dir="problems"):
        self.problems_dir = problems_dir

    def judge(self, task):

        problem = task["problem_id"]
        language = task["language"]
        code = task["code"]

        # Paths
        problem_path = os.path.join(self.problems_dir, problem)
        input_file = os.path.join(problem_path, "input.txt")
        output_file = os.path.join(problem_path, "output.txt")

        # Check file existence
        if not os.path.exists(input_file):
            return {"verdict": "INPUT_FILE_MISSING"}

        if not os.path.exists(output_file):
            return {"verdict": "OUTPUT_FILE_MISSING"}

        with tempfile.TemporaryDirectory() as tmp:

            # Copy tests
            shutil.copy(input_file, tmp + "/input.txt")
            shutil.copy(output_file, tmp + "/expected.txt")

            # Choose proper user code filename
            if language == "cpp":
                code_path = os.path.join(tmp, "solution.cpp")
            elif language == "java":
                code_path = os.path.join(tmp, "Main.java")
            else:  # Python
                code_path = os.path.join(tmp, "solution.py")

            # Save user code
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Load input & expected outputs
            with open(tmp + "/input.txt", encoding="utf-8") as f:
                input_data = f.read()

            with open(tmp + "/expected.txt", encoding="utf-8") as f:
                expected = f.read().strip()

            # Language dispatch
            if language == "python":
                return self._run_python(code_path, input_data, expected)

            elif language == "cpp":
                exe_path = os.path.join(tmp, "solution.exe")
                return self._run_cpp(code_path, exe_path, input_data, expected)

            elif language == "java":
                return self._run_java(code_path, tmp, input_data, expected)

            else:
                return {"verdict": "LANGUAGE_NOT_SUPPORTED"}

    # ------------------ PYTHON ------------------

    def _run_python(self, code_path, input_data, expected):
        try:
            proc = subprocess.Popen(
                [sys.executable, code_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            timer = threading.Timer(TIME_LIMIT, proc.kill)
            timer.start()

            out, err = proc.communicate(input_data)
            timer.cancel()

            if proc.returncode != 0:
                return {"verdict": "RUNTIME_ERROR", "error": err.strip()}

            if out.strip() == expected:
                return {"verdict": "OK"}

            return {"verdict": "WRONG_ANSWER", "output": out.strip(), "expected": expected}

        except Exception as e:
            return {"verdict": "SYSTEM_ERROR", "error": str(e)}

    # ------------------ C++ ------------------

    def _run_cpp(self, code_path, exe_path, input_data, expected):

        # compile
        p = subprocess.run(["g++", code_path, "-o", exe_path],
                           capture_output=True, text=True)

        if p.returncode != 0:
            return {"verdict": "COMPILATION_ERROR", "error": p.stderr}

        try:
            proc = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            timer = threading.Timer(TIME_LIMIT, proc.kill)
            timer.start()

            out, err = proc.communicate(input_data)
            timer.cancel()

            if proc.returncode != 0:
                return {"verdict": "RUNTIME_ERROR", "error": err}

            if out.strip() == expected:
                return {"verdict": "OK"}

            return {"verdict": "WRONG_ANSWER", "output": out.strip(), "expected": expected}

        except Exception as e:
            return {"verdict": "SYSTEM_ERROR", "error": str(e)}

    # ------------------ JAVA ------------------

    def _run_java(self, code_path, workdir, input_data, expected):
        # compile Java
        p = subprocess.run(["javac", code_path],
                           capture_output=True, text=True)

        if p.returncode != 0:
            return {"verdict": "COMPILATION_ERROR", "error": p.stderr}

        try:
            proc = subprocess.Popen(
                ["java", "-cp", workdir, "Main"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            timer = threading.Timer(TIME_LIMIT, proc.kill)
            timer.start()

            out, err = proc.communicate(input_data)
            timer.cancel()

            if proc.returncode != 0:
                return {"verdict": "RUNTIME_ERROR", "error": err}

            if out.strip() == expected:
                return {"verdict": "OK"}

            return {"verdict": "WRONG_ANSWER", "output": out.strip(), "expected": expected}

        except Exception as e:
            return {"verdict": "SYSTEM_ERROR", "error": str(e)}
