
#  Configuration Serveur


SERVER_HOST = 'localhost'
SERVER_PORT = 5000
MAX_CLIENTS = 50


#  Configuration Contest


DEFAULT_CONTEST_DURATION = 1800  # 30 minutes
MIN_PROBLEMS = 1
MAX_PROBLEMS = 10

# Difficultés supportées par les problèmes
SUPPORTED_DIFFICULTIES = ['easy', 'medium', 'hard']


#  Configuration Workers


NUM_WORKERS = 4
WORKER_TIMEOUT = 5


#  Configuration Évaluation


EXECUTION_TIMEOUT = 3
COMPILATION_TIMEOUT = 10
MAX_MEMORY_USAGE = 256 * 1024 * 1024  # 256 MB


#  Système de points


POINTS_CORRECT = 100
POINTS_WRONG_ANSWER = -10
POINTS_TIMEOUT = -20
POINTS_COMPILATION_ERROR = -5
POINTS_RUNTIME_ERROR = -10


#  Langages Supportés


SUPPORTED_LANGUAGES = ['python', 'cpp', 'java']

PYTHON_EXECUTABLE = 'python3'
CPP_COMPILER = 'g++'
JAVA_COMPILER = 'javac'
JAVA_RUNNER = 'java'

CPP_COMPILE_FLAGS = ['-std=c++17', '-O2']
JAVA_COMPILE_FLAGS = []


#  Dossiers Importants


PROBLEMS_DIR = 'problems'
SUBMISSIONS_DIR = 'data/submissions'
LOGS_DIR = 'data/logs'


#  Dashboard

DASHBOARD_HOST = 'localhost'
DASHBOARD_PORT = 8080
DASHBOARD_DEBUG = True


#  Logging


LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'data/logs/codearena.log'


#  Sécurité


MAX_CODE_LENGTH = 50000
MAX_OUTPUT_LENGTH = 10000
