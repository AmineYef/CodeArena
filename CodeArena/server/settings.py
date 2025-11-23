
SERVER_HOST = 'localhost'
SERVER_PORT = 5000
MAX_CLIENTS = 50

# Configuration du contest
DEFAULT_CONTEST_DURATION = 1800  # 30 minutes en secondes
CONTEST_PROBLEMS = ['P1', 'P2', 'P3']

# Configuration des workers
NUM_WORKERS = 4  # Nombre de processus workers
WORKER_TIMEOUT = 5  # Timeout en secondes pour l'exécution de code

# Configuration de l'évaluation
EXECUTION_TIMEOUT = 3  # Timeout pour l'exécution d'un programme (secondes)
COMPILATION_TIMEOUT = 10  # Timeout pour la compilation

# Système de points
POINTS_CORRECT = 100
POINTS_WRONG_ANSWER = -10
POINTS_TIMEOUT = -20
POINTS_COMPILATION_ERROR = -5
POINTS_RUNTIME_ERROR = -10

# Langages supportés
SUPPORTED_LANGUAGES = ['python', 'cpp', 'java']

# Chemins des compilateurs
PYTHON_EXECUTABLE = 'python3'
CPP_COMPILER = 'g++'
JAVA_COMPILER = 'javac'
JAVA_RUNNER = 'java'

# Options de compilation
CPP_COMPILE_FLAGS = ['-std=c++17', '-O2']
JAVA_COMPILE_FLAGS = []

# Chemins des dossiers
PROBLEMS_DIR = 'problems'
SUBMISSIONS_DIR = 'data/submissions'
LOGS_DIR = 'data/logs'

# Configuration du dashboard
DASHBOARD_HOST = 'localhost'
DASHBOARD_PORT = 8080
DASHBOARD_DEBUG = True

# Configuration du logging
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'data/logs/codearena.log'

# Limites de sécurité
MAX_CODE_LENGTH = 50000  # Nombre maximum de caractères dans le code
MAX_OUTPUT_LENGTH = 10000  # Nombre maximum de caractères dans l'output
MAX_MEMORY_USAGE = 256 * 1024 * 1024  # 256 MB