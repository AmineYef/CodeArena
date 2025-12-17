import subprocess
import tempfile
import os
import sys
import shutil
import threading

TIME_LIMIT = 2 


class JudgeEngine:

    def __init__(self, problems_dir="problems"):
        self.problems_dir = problems_dir

    def judge(self, task):
        """
        Juge une soumission avec validation complète
        
        Returns:
            dict avec 'verdict' et éventuellement 'error', 'output', 'expected'
        """
        
        problem = task.get("problem_id")
        language = task.get("language")
        code = task.get("code")
        

        if not all([problem, language, code]):
            return {"verdict": "INVALID_SUBMISSION", "error": "Paramètres manquants"}

        supported_languages = ['python', 'cpp', 'java']
        if language not in supported_languages:
            return {
                "verdict": "LANGUAGE_NOT_SUPPORTED",
                "error": f"Langage '{language}' non supporté. Utilisez: {', '.join(supported_languages)}"
            }
        

        if len(code.strip()) == 0:
            return {"verdict": "EMPTY_CODE", "error": "Le code est vide"}
        

        if len(code) > 50000:
            return {"verdict": "CODE_TOO_LONG", "error": "Le code dépasse 50000 caractères"}

        problem_path = os.path.join(self.problems_dir, problem)

        if not os.path.exists(problem_path):
            return {"verdict": "PROBLEM_NOT_FOUND", "error": f"Problème '{problem}' introuvable"}
        
        input_file = os.path.join(problem_path, "input.txt")
        output_file = os.path.join(problem_path, "output.txt")

        if not os.path.exists(input_file):
            return {"verdict": "INPUT_FILE_MISSING", "error": "Fichier input.txt manquant"}

        if not os.path.exists(output_file):
            return {"verdict": "OUTPUT_FILE_MISSING", "error": "Fichier output.txt manquant"}
        with tempfile.TemporaryDirectory() as tmp:
            try:
                shutil.copy(input_file, os.path.join(tmp, "input.txt"))
                shutil.copy(output_file, os.path.join(tmp, "expected.txt"))

                if language == "cpp":
                    code_path = os.path.join(tmp, "solution.cpp")
                elif language == "java":
                    code_path = os.path.join(tmp, "Main.java")
                else:  
                    code_path = os.path.join(tmp, "solution.py")

                with open(code_path, "w", encoding="utf-8") as f:
                    f.write(code)

                with open(os.path.join(tmp, "input.txt"), encoding="utf-8") as f:
                    input_data = f.read()

                with open(os.path.join(tmp, "expected.txt"), encoding="utf-8") as f:
                    expected = f.read().strip()

                if language == "python":
                    return self._run_python(code_path, input_data, expected)

                elif language == "cpp":
                    exe_path = os.path.join(tmp, "solution.exe")
                    return self._run_cpp(code_path, exe_path, input_data, expected)

                elif language == "java":
                    return self._run_java(code_path, tmp, input_data, expected)

                else:
                    return {"verdict": "LANGUAGE_NOT_SUPPORTED"}
                    
            except Exception as e:
                return {"verdict": "SYSTEM_ERROR", "error": f"Erreur système: {str(e)}"}


    def _run_python(self, code_path, input_data, expected):
        """Exécute et évalue du code Python"""
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

            try:
                out, err = proc.communicate(input_data, timeout=TIME_LIMIT)
            except subprocess.TimeoutExpired:
                proc.kill()
                return {"verdict": "TIMEOUT", "error": f"Le programme a dépassé {TIME_LIMIT} secondes"}
            finally:
                timer.cancel()


            if proc.returncode != 0:
                return {"verdict": "RUNTIME_ERROR", "error": err.strip()[:1000]}


            output_lines = [line.strip() for line in out.strip().split('\n') if line.strip()]
            expected_lines = [line.strip() for line in expected.strip().split('\n') if line.strip()]

            if output_lines == expected_lines:
                return {"verdict": "OK"}

            return {
                "verdict": "WRONG_ANSWER",
                "output": out.strip()[:500],
                "expected": expected[:500]
            }

        except Exception as e:
            return {"verdict": "SYSTEM_ERROR", "error": str(e)}


    def _run_cpp(self, code_path, exe_path, input_data, expected):
        """Compile et exécute du code C++"""
        
        try:
            compile_result = subprocess.run(
                ["g++", code_path, "-o", exe_path, "-std=c++17", "-O2"],
                capture_output=True,
                text=True,
                timeout=10
            )
        except subprocess.TimeoutExpired:
            return {"verdict": "COMPILATION_ERROR", "error": "Compilation trop longue (>10s)"}
        except FileNotFoundError:
            return {"verdict": "SYSTEM_ERROR", "error": "Compilateur g++ non trouvé"}

        if compile_result.returncode != 0:
            return {
                "verdict": "COMPILATION_ERROR",
                "error": compile_result.stderr.strip()[:1000]
            }
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

            try:
                out, err = proc.communicate(input_data, timeout=TIME_LIMIT)
            except subprocess.TimeoutExpired:
                proc.kill()
                return {"verdict": "TIMEOUT", "error": f"Le programme a dépassé {TIME_LIMIT} secondes"}
            finally:
                timer.cancel()

            if proc.returncode != 0:
                return {"verdict": "RUNTIME_ERROR", "error": err.strip()[:1000]}

            output_lines = [line.strip() for line in out.strip().split('\n') if line.strip()]
            expected_lines = [line.strip() for line in expected.strip().split('\n') if line.strip()]
            
            if output_lines == expected_lines:
                return {"verdict": "OK"}

            return {
                "verdict": "WRONG_ANSWER",
                "output": out.strip()[:500],
                "expected": expected[:500]
            }

        except Exception as e:
            return {"verdict": "SYSTEM_ERROR", "error": str(e)}


    def _run_java(self, code_path, workdir, input_data, expected):
        """Compile et exécute du code Java"""
        
        try:
            compile_result = subprocess.run(
                ["javac", code_path],
                capture_output=True,
                text=True,
                timeout=10
            )
        except subprocess.TimeoutExpired:
            return {"verdict": "COMPILATION_ERROR", "error": "Compilation trop longue (>10s)"}
        except FileNotFoundError:
            return {"verdict": "SYSTEM_ERROR", "error": "Compilateur javac non trouvé"}

        if compile_result.returncode != 0:
            return {
                "verdict": "COMPILATION_ERROR",
                "error": compile_result.stderr.strip()[:1000]
            }


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

            try:
                out, err = proc.communicate(input_data, timeout=TIME_LIMIT)
            except subprocess.TimeoutExpired:
                proc.kill()
                return {"verdict": "TIMEOUT", "error": f"Le programme a dépassé {TIME_LIMIT} secondes"}
            finally:
                timer.cancel()

            if proc.returncode != 0:
                return {"verdict": "RUNTIME_ERROR", "error": err.strip()[:1000]}
            output_lines = [line.strip() for line in out.strip().split('\n') if line.strip()]
            expected_lines = [line.strip() for line in expected.strip().split('\n') if line.strip()]
            if output_lines == expected_lines:
                return {"verdict": "OK"}
            return {
                "verdict": "WRONG_ANSWER",
                "output": out.strip()[:500],
                "expected": expected[:500]
            }
        except Exception as e:
            return {"verdict": "SYSTEM_ERROR", "error": str(e)}