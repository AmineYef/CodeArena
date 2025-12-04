# from flask import Flask, render_template, request, jsonify, redirect, url_for
# import sys
# import os

# # Ajouter le chemin parent pour importer les modules server
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from server.settings import DASHBOARD_HOST, DASHBOARD_PORT
# from server.contest_manager import ContestManager
# from server.contest_factory import ContestFactory
# from server.leaderboard import Leaderboard
# from server.queue_manager import TaskQueue
# import json
# import uuid
# import time

# app = Flask(__name__)

# # ========================================
# # VARIABLES GLOBALES (partagées)
# # ========================================
# contests = {}  # {contest_id: {info}}
# active_contest_id = None
# leaderboard_instance = Leaderboard()
# queue_instance = TaskQueue()

# # Simuler des workers
# workers_status = [
#     {"id": 1, "status": "idle", "task": None},
#     {"id": 2, "status": "idle", "task": None},
#     {"id": 3, "status": "idle", "task": None},
#     {"id": 4, "status": "idle", "task": None},
# ]

# submissions_log = []

# # ========================================
# # ROUTES - PAGE D'ACCUEIL
# # ========================================

# @app.route('/')
# def index():
#     """Page d'accueil avec navigation"""
#     return render_template('index.html')


# # ========================================
# # ROUTES - CONTESTS (PARTICIPANTS)
# # ========================================

# @app.route('/contests')
# def contests_list():
#     """Liste des contests disponibles - ACCESSIBLE À TOUS"""
#     return render_template('contests_list.html', contests=contests)


# @app.route('/contest/<contest_id>/join', methods=['GET', 'POST'])
# def join_contest(contest_id):
#     """Rejoindre un contest"""
#     if request.method == 'POST':
#         username = request.form.get('username', 'Anonymous')
#         return redirect(url_for('contest_dashboard', contest_id=contest_id, username=username))
    
#     contest = contests.get(contest_id)
#     if not contest:
#         return "Contest non trouvé", 404
    
#     return render_template('join_contest.html', contest=contest, contest_id=contest_id)


# @app.route('/contest/<contest_id>/dashboard')
# def contest_dashboard(contest_id):
#     """Dashboard du contest pour un participant"""
#     username = request.args.get('username', 'Anonymous')
#     contest = contests.get(contest_id)
    
#     if not contest:
#         return "Contest non trouvé", 404
    
#     # Créer une version numérotée des problèmes
#     problems_numbered = []
#     for idx, problem_id in enumerate(contest['problems'], 1):
#         problems_numbered.append({
#             'number': idx,
#             'id': problem_id
#         })
    
#     return render_template('contest_dashboard.html', 
#                          contest=contest, 
#                          contest_id=contest_id,
#                          username=username,
#                          problems_numbered=problems_numbered)


# @app.route('/contest/<contest_id>/problem/<problem_number>')
# def problem_view(contest_id, problem_number):
#     """Afficher un problème avec éditeur de code"""
#     username = request.args.get('username', 'Anonymous')
#     contest = contests.get(contest_id)
    
#     if not contest:
#         return "Contest non trouvé", 404
    
#     # Convertir le numéro en ID de problème
#     try:
#         problem_index = int(problem_number) - 1
#         if problem_index < 0 or problem_index >= len(contest['problems']):
#             return "Problème non trouvé", 404
        
#         problem_id = contest['problems'][problem_index]
#     except (ValueError, IndexError):
#         return "Problème non trouvé", 404
    
#     # Charger l'énoncé du problème
#     problem_path = os.path.join('problems', problem_id)
#     statement_path = os.path.join(problem_path, 'statement.md')
    
#     statement = ""
#     if os.path.exists(statement_path):
#         with open(statement_path, 'r', encoding='utf-8') as f:
#             statement = f.read()
    
#     # Charger les métadonnées
#     meta_path = os.path.join(problem_path, 'meta.json')
#     meta = {}
#     if os.path.exists(meta_path):
#         with open(meta_path, 'r') as f:
#             meta = json.load(f)
    
#     return render_template('problem.html',
#                          contest_id=contest_id,
#                          problem_number=problem_number,
#                          problem_id=problem_id,
#                          statement=statement,
#                          meta=meta,
#                          username=username)


# @app.route('/contest/<contest_id>/leaderboard')
# def leaderboard_view(contest_id):
#     """Afficher le leaderboard du contest"""
#     contest = contests.get(contest_id)
#     if not contest:
#         return "Contest non trouvé", 404
    
#     return render_template('leaderboard.html', 
#                          contest=contest,
#                          contest_id=contest_id)


# # ========================================
# # ROUTES - CREATOR
# # ========================================

# @app.route('/creator', methods=['GET', 'POST'])
# def creator():
#     """Interface créateur de contest"""
#     if request.method == 'POST':
#         duration = int(request.form.get('duration', 15))
#         difficulty = request.form.get('difficulty', 'easy')
#         num_problems = int(request.form.get('num_problems', 3))
        
#         # Créer le contest
#         contest_id = str(uuid.uuid4())[:8].upper()
        
#         factory = ContestFactory()
#         try:
#             problems = factory.generate_contest(num_problems, difficulty)
            
#             contests[contest_id] = {
#                 'id': contest_id,
#                 'duration': duration * 60,  # convertir en secondes
#                 'difficulty': difficulty,
#                 'num_problems': num_problems,
#                 'problems': problems,
#                 'remaining_time': duration * 60,
#                 'active': True,
#                 'created_at': time.time()
#             }
            
#             global active_contest_id
#             active_contest_id = contest_id
            
#             return render_template('contest_created.html', 
#                                  contest_id=contest_id, 
#                                  contest=contests[contest_id])
#         except ValueError as e:
#             return f"Erreur : {str(e)}", 400
    
#     return render_template('creator.html')


# @app.route('/creator/contests')
# def creator_contests():
#     """Liste des contests créés"""
#     return render_template('creator_contests.html', contests=contests)


# # ========================================
# # ROUTES - ADMIN DASHBOARD
# # ========================================

# @app.route('/admin/workers')
# def admin_workers():
#     """Vue des workers multiprocessing"""
#     return render_template('admin_workers.html')


# @app.route('/admin/activity')
# def admin_activity():
#     """Vue de l'activité du serveur"""
#     return render_template('admin_activity.html')


# @app.route('/admin/logs')
# def admin_logs():
#     """Logs du système"""
#     return render_template('admin_logs.html')


# # ========================================
# # API ENDPOINTS (JSON)
# # ========================================

# @app.route('/api/contests')
# def api_contests():
#     """API : Liste des contests"""
#     return jsonify(list(contests.values()))


# @app.route('/api/contest/<contest_id>')
# def api_contest(contest_id):
#     """API : Détails d'un contest"""
#     contest = contests.get(contest_id)
#     if not contest:
#         return jsonify({"error": "Contest non trouvé"}), 404
#     return jsonify(contest)


# @app.route('/api/contest/<contest_id>/leaderboard')
# def api_leaderboard(contest_id):
#     """API : Leaderboard d'un contest"""
#     return jsonify(leaderboard_instance.get_leaderboard())


# @app.route('/api/workers')
# def api_workers():
#     """API : État des workers"""
#     return jsonify(workers_status)


# @app.route('/api/queue')
# def api_queue():
#     """API : Taille de la queue"""
#     return jsonify({"size": queue_instance.size()})


# @app.route('/api/logs')
# def api_logs():
#     """API : Derniers logs"""
#     return jsonify(submissions_log[-20:])  # 20 derniers logs


# @app.route('/api/submit', methods=['POST'])
# def api_submit():
#     """API : Soumettre du code"""
#     data = request.json
    
#     username = data.get('username')
#     problem_id = data.get('problem_id')
#     language = data.get('language')
#     code = data.get('code')
#     contest_id = data.get('contest_id')
    
#     if not all([problem_id, language, code, username, contest_id]):
#         return jsonify({"error": "Données manquantes"}), 400
    
#     # Vérifier que le contest existe
#     contest = contests.get(contest_id)
#     if not contest:
#         return jsonify({"error": "Contest non trouvé"}), 404
    
#     # Ajouter à la queue (simulation)
#     submission_id = str(uuid.uuid4())[:8]
    
#     submission = {
#         "id": submission_id,
#         "username": username,
#         "problem_id": problem_id,
#         "language": language,
#         "status": "pending",
#         "timestamp": time.time(),
#         "contest_id": contest_id
#     }
    
#     submissions_log.append(submission)
    
#     # TODO: Envoyer au vrai serveur TCP ici
#     # Pour l'instant, simuler un résultat
#     import random
#     import threading
    
#     def simulate_verdict():
#         time.sleep(2)  # Simuler le temps de traitement
        
#         verdicts = ["OK", "WRONG_ANSWER", "TIMEOUT", "RUNTIME_ERROR"]
#         verdict = random.choice(verdicts)
        
#         # Mettre à jour le leaderboard
#         leaderboard_instance.update(username, verdict)
        
#         # Mettre à jour le status
#         for sub in submissions_log:
#             if sub['id'] == submission_id:
#                 sub['status'] = verdict
#                 sub['verdict'] = verdict
#                 break
    
#     threading.Thread(target=simulate_verdict, daemon=True).start()
    
#     # Simuler un worker qui prend la tâche
#     for worker in workers_status:
#         if worker["status"] == "idle":
#             worker["status"] = "running"
#             worker["task"] = f"{problem_id} ({username})"
            
#             def reset_worker():
#                 time.sleep(2)
#                 worker["status"] = "idle"
#                 worker["task"] = None
            
#             threading.Thread(target=reset_worker, daemon=True).start()
#             break
    
#     return jsonify({
#         "success": True,
#         "submission_id": submission_id,
#         "message": "Soumission reçue et en cours d'évaluation"
#     })


# @app.route('/api/submission/<submission_id>/status')
# def api_submission_status(submission_id):
#     """API : Statut d'une soumission"""
#     for sub in submissions_log:
#         if sub['id'] == submission_id:
#             return jsonify(sub)
    
#     return jsonify({"error": "Soumission non trouvée"}), 404


# # ========================================
# # LANCEMENT DU SERVEUR
# # ========================================

# if __name__ == '__main__':
#     print(f"🚀 Dashboard démarré sur http://{DASHBOARD_HOST}:{DASHBOARD_PORT}")
#     print(f"📊 Pages disponibles :")
#     print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/ (Accueil)")
#     print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/contests (Liste contests)")
#     print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/creator (Créer un contest)")
#     print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/admin/workers (Workers)")
    
#     app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT, debug=True)



# from flask import Flask, render_template, request, jsonify, redirect, url_for
# import sys
# import os
# import markdown

# # Ajouter le chemin parent pour importer les modules server
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from server.settings import DASHBOARD_HOST, DASHBOARD_PORT
# from server.contest_manager import ContestManager
# from server.contest_factory import ContestFactory
# from server.leaderboard import Leaderboard
# from server.queue_manager import TaskQueue
# import json
# import uuid
# import time

# app = Flask(__name__)

# # ========================================
# # FILTRE MARKDOWN PERSONNALISÉ
# # ========================================
# @app.template_filter('markdown')
# def markdown_filter(text):
#     """Convertit le markdown en HTML"""
#     return markdown.markdown(text, extensions=['extra', 'codehilite', 'fenced_code'])

# # ========================================
# # VARIABLES GLOBALES (partagées)
# # ========================================
# contests = {}  # {contest_id: {info}}
# active_contest_id = None
# leaderboard_instance = Leaderboard()
# queue_instance = TaskQueue()

# # Simuler des workers
# workers_status = [
#     {"id": 1, "status": "idle", "task": None},
#     {"id": 2, "status": "idle", "task": None},
#     {"id": 3, "status": "idle", "task": None},
#     {"id": 4, "status": "idle", "task": None},
# ]

# submissions_log = []

# # ========================================
# # ROUTES - PAGE D'ACCUEIL
# # ========================================

# @app.route('/')
# def index():
#     """Page d'accueil avec navigation"""
#     return render_template('index.html')


# # ========================================
# # ROUTES - CONTESTS (PARTICIPANTS)
# # ========================================

# @app.route('/contests')
# def contests_list():
#     """Liste des contests disponibles - ACCESSIBLE À TOUS"""
#     return render_template('contests_list.html', contests=contests)


# @app.route('/contest/<contest_id>/join', methods=['GET', 'POST'])
# def join_contest(contest_id):
#     """Rejoindre un contest"""
#     if request.method == 'POST':
#         username = request.form.get('username', 'Anonymous')
#         return redirect(url_for('contest_dashboard', contest_id=contest_id, username=username))
    
#     contest = contests.get(contest_id)
#     if not contest:
#         return "Contest non trouvé", 404
    
#     return render_template('join_contest.html', contest=contest, contest_id=contest_id)


# @app.route('/contest/<contest_id>/dashboard')
# def contest_dashboard(contest_id):
#     """Dashboard du contest pour un participant"""
#     username = request.args.get('username', 'Anonymous')
#     contest = contests.get(contest_id)
    
#     if not contest:
#         return "Contest non trouvé", 404
    
#     # Créer une version numérotée des problèmes
#     problems_numbered = []
#     for idx, problem_id in enumerate(contest['problems'], 1):
#         problems_numbered.append({
#             'number': idx,
#             'id': problem_id
#         })
    
#     return render_template('contest_dashboard.html', 
#                          contest=contest, 
#                          contest_id=contest_id,
#                          username=username,
#                          problems_numbered=problems_numbered)


# @app.route('/contest/<contest_id>/problem/<problem_number>')
# def problem_view(contest_id, problem_number):
#     """Afficher un problème avec éditeur de code"""
#     username = request.args.get('username', 'Anonymous')
#     contest = contests.get(contest_id)
    
#     if not contest:
#         return "Contest non trouvé", 404
    
#     # Convertir le numéro en ID de problème
#     try:
#         problem_index = int(problem_number) - 1
#         if problem_index < 0 or problem_index >= len(contest['problems']):
#             return "Problème non trouvé", 404
        
#         problem_id = contest['problems'][problem_index]
#     except (ValueError, IndexError):
#         return "Problème non trouvé", 404
    
#     # Charger l'énoncé du problème
#     problem_path = os.path.join('problems', problem_id)
#     statement_path = os.path.join(problem_path, 'statement.md')
    
#     statement = ""
#     if os.path.exists(statement_path):
#         with open(statement_path, 'r', encoding='utf-8') as f:
#             statement = f.read()
    
#     # Charger les métadonnées
#     meta_path = os.path.join(problem_path, 'meta.json')
#     meta = {}
#     if os.path.exists(meta_path):
#         with open(meta_path, 'r') as f:
#             meta = json.load(f)
    
#     return render_template('problem.html',
#                          contest_id=contest_id,
#                          problem_number=problem_number,
#                          problem_id=problem_id,
#                          statement=statement,
#                          meta=meta,
#                          username=username)


# @app.route('/contest/<contest_id>/leaderboard')
# def leaderboard_view(contest_id):
#     """Afficher le leaderboard du contest"""
#     contest = contests.get(contest_id)
#     if not contest:
#         return "Contest non trouvé", 404
    
#     return render_template('leaderboard.html', 
#                          contest=contest,
#                          contest_id=contest_id)


# # ========================================
# # ROUTES - CREATOR
# # ========================================

# @app.route('/creator', methods=['GET', 'POST'])
# def creator():
#     """Interface créateur de contest"""
#     if request.method == 'POST':
#         duration = int(request.form.get('duration', 15))
#         difficulty = request.form.get('difficulty', 'easy')
#         num_problems = int(request.form.get('num_problems', 3))
        
#         # Créer le contest
#         contest_id = str(uuid.uuid4())[:8].upper()
        
#         factory = ContestFactory()
#         try:
#             problems = factory.generate_contest(num_problems, difficulty)
            
#             contests[contest_id] = {
#                 'id': contest_id,
#                 'duration': duration * 60,  # convertir en secondes
#                 'difficulty': difficulty,
#                 'num_problems': num_problems,
#                 'problems': problems,
#                 'remaining_time': duration * 60,
#                 'active': True,
#                 'created_at': time.time()
#             }
            
#             global active_contest_id
#             active_contest_id = contest_id
            
#             return render_template('contest_created.html', 
#                                  contest_id=contest_id, 
#                                  contest=contests[contest_id])
#         except ValueError as e:
#             return f"Erreur : {str(e)}", 400
    
#     return render_template('creator.html')


# @app.route('/creator/contests')
# def creator_contests():
#     """Liste des contests créés"""
#     return render_template('creator_contests.html', contests=contests)


# # ========================================
# # ROUTES - ADMIN DASHBOARD
# # ========================================

# @app.route('/admin/workers')
# def admin_workers():
#     """Vue des workers multiprocessing"""
#     return render_template('admin_workers.html')


# @app.route('/admin/activity')
# def admin_activity():
#     """Vue de l'activité du serveur"""
#     return render_template('admin_activity.html')


# @app.route('/admin/logs')
# def admin_logs():
#     """Logs du système"""
#     return render_template('admin_logs.html')


# # ========================================
# # API ENDPOINTS (JSON)
# # ========================================

# @app.route('/api/contests')
# def api_contests():
#     """API : Liste des contests"""
#     return jsonify(list(contests.values()))


# @app.route('/api/contest/<contest_id>')
# def api_contest(contest_id):
#     """API : Détails d'un contest"""
#     contest = contests.get(contest_id)
#     if not contest:
#         return jsonify({"error": "Contest non trouvé"}), 404
#     return jsonify(contest)


# @app.route('/api/contest/<contest_id>/leaderboard')
# def api_leaderboard(contest_id):
#     """API : Leaderboard d'un contest"""
#     return jsonify(leaderboard_instance.get_leaderboard())


# @app.route('/api/workers')
# def api_workers():
#     """API : État des workers"""
#     return jsonify(workers_status)


# @app.route('/api/queue')
# def api_queue():
#     """API : Taille de la queue"""
#     return jsonify({"size": queue_instance.size()})


# @app.route('/api/logs')
# def api_logs():
#     """API : Derniers logs"""
#     return jsonify(submissions_log[-20:])  # 20 derniers logs


# @app.route('/api/submit', methods=['POST'])
# def api_submit():
#     """API : Soumettre du code"""
#     data = request.json
    
#     username = data.get('username')
#     problem_id = data.get('problem_id')
#     language = data.get('language')
#     code = data.get('code')
#     contest_id = data.get('contest_id')
    
#     if not all([problem_id, language, code, username, contest_id]):
#         return jsonify({"error": "Données manquantes"}), 400
    
#     # Vérifier que le contest existe
#     contest = contests.get(contest_id)
#     if not contest:
#         return jsonify({"error": "Contest non trouvé"}), 404
    
#     # Ajouter à la queue (simulation)
#     submission_id = str(uuid.uuid4())[:8]
    
#     submission = {
#         "id": submission_id,
#         "username": username,
#         "problem_id": problem_id,
#         "language": language,
#         "status": "pending",
#         "timestamp": time.time(),
#         "contest_id": contest_id
#     }
    
#     submissions_log.append(submission)
    
#     # TODO: Envoyer au vrai serveur TCP ici
#     # Pour l'instant, simuler un résultat
#     import random
#     import threading
    
#     def simulate_verdict():
#         time.sleep(2)  # Simuler le temps de traitement
        
#         verdicts = ["OK", "WRONG_ANSWER", "TIMEOUT", "RUNTIME_ERROR"]
#         verdict = random.choice(verdicts)
        
#         # Mettre à jour le leaderboard
#         leaderboard_instance.update(username, verdict)
        
#         # Mettre à jour le status
#         for sub in submissions_log:
#             if sub['id'] == submission_id:
#                 sub['status'] = verdict
#                 sub['verdict'] = verdict
#                 break
    
#     threading.Thread(target=simulate_verdict, daemon=True).start()
    
#     # Simuler un worker qui prend la tâche
#     for worker in workers_status:
#         if worker["status"] == "idle":
#             worker["status"] = "running"
#             worker["task"] = f"{problem_id} ({username})"
            
#             def reset_worker():
#                 time.sleep(2)
#                 worker["status"] = "idle"
#                 worker["task"] = None
            
#             threading.Thread(target=reset_worker, daemon=True).start()
#             break
    
#     return jsonify({
#         "success": True,
#         "submission_id": submission_id,
#         "message": "Soumission reçue et en cours d'évaluation"
#     })


# @app.route('/api/submission/<submission_id>/status')
# def api_submission_status(submission_id):
#     """API : Statut d'une soumission"""
#     for sub in submissions_log:
#         if sub['id'] == submission_id:
#             return jsonify(sub)
    
#     return jsonify({"error": "Soumission non trouvée"}), 404


# # ========================================
# # LANCEMENT DU SERVEUR
# # ========================================

# if __name__ == '__main__':
#     print(f"🚀 Dashboard démarré sur http://{DASHBOARD_HOST}:{DASHBOARD_PORT}")
#     print(f"📊 Pages disponibles :")
#     print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/ (Accueil)")
#     print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/contests (Liste contests)")
#     print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/creator (Créer un contest)")
#     print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/admin/workers (Workers)")
    
#     app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT, debug=True)



from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os
import markdown

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.settings import DASHBOARD_HOST, DASHBOARD_PORT
from server.contest_manager import ContestManager
from server.contest_factory import ContestFactory
from server.leaderboard import Leaderboard
from server.queue_manager import TaskQueue
import json
import uuid
import time

app = Flask(__name__)

# ========================================
# FILTRE MARKDOWN PERSONNALISÉ
# ========================================
@app.template_filter('markdown')
def markdown_filter(text):
    """Convertit le markdown en HTML"""
    return markdown.markdown(text, extensions=['extra', 'codehilite', 'fenced_code'])

# ========================================
# VARIABLES GLOBALES (partagées)
# ========================================
contests = {}
active_contest_id = None
leaderboard_instance = Leaderboard()
queue_instance = TaskQueue()

# Suivre les problèmes résolus par utilisateur
solved_problems = {}  # {username: {contest_id: {problem_id: True}}}

workers_status = [
    {"id": 1, "status": "idle", "task": None},
    {"id": 2, "status": "idle", "task": None},
    {"id": 3, "status": "idle", "task": None},
    {"id": 4, "status": "idle", "task": None},
]

submissions_log = []

# ========================================
# FONCTIONS UTILITAIRES
# ========================================

def is_problem_solved(username, contest_id, problem_id):
    """Vérifie si un problème est résolu par un utilisateur"""
    if username not in solved_problems:
        return False
    if contest_id not in solved_problems[username]:
        return False
    return solved_problems[username].get(problem_id, False)

def mark_problem_solved(username, contest_id, problem_id):
    """Marque un problème comme résolu"""
    if username not in solved_problems:
        solved_problems[username] = {}
    if contest_id not in solved_problems[username]:
        solved_problems[username][contest_id] = {}
    solved_problems[username][contest_id][problem_id] = True

def get_user_stats(username, contest_id):
    """Récupère les statistiques d'un utilisateur pour un contest"""
    if username not in solved_problems or contest_id not in solved_problems[username]:
        return {"solved": 0, "total": 0}
    
    contest = contests.get(contest_id)
    if not contest:
        return {"solved": 0, "total": 0}
    
    solved_count = sum(1 for pid in contest['problems'] 
                      if solved_problems[username][contest_id].get(pid, False))
    
    return {
        "solved": solved_count,
        "total": len(contest['problems'])
    }

# ========================================
# ROUTES - PAGE D'ACCUEIL
# ========================================

@app.route('/')
def index():
    return render_template('index.html')

# ========================================
# ROUTES - CONTESTS (PARTICIPANTS)
# ========================================

@app.route('/contests')
def contests_list():
    return render_template('contests_list.html', contests=contests)

@app.route('/contest/<contest_id>/join', methods=['GET', 'POST'])
def join_contest(contest_id):
    if request.method == 'POST':
        username = request.form.get('username', 'Anonymous')
        return redirect(url_for('contest_dashboard', contest_id=contest_id, username=username))
    
    contest = contests.get(contest_id)
    if not contest:
        return "Contest non trouvé", 404
    
    return render_template('join_contest.html', contest=contest, contest_id=contest_id)

@app.route('/contest/<contest_id>/dashboard')
def contest_dashboard(contest_id):
    username = request.args.get('username', 'Anonymous')
    contest = contests.get(contest_id)
    
    if not contest:
        return "Contest non trouvé", 404
    
    # Créer une version numérotée avec statut résolu
    problems_numbered = []
    for idx, problem_id in enumerate(contest['problems'], 1):
        solved = is_problem_solved(username, contest_id, problem_id)
        problems_numbered.append({
            'number': idx,
            'id': problem_id,
            'solved': solved
        })
    
    # Statistiques utilisateur
    stats = get_user_stats(username, contest_id)
    
    return render_template('contest_dashboard.html', 
                         contest=contest, 
                         contest_id=contest_id,
                         username=username,
                         problems_numbered=problems_numbered,
                         user_stats=stats)

@app.route('/contest/<contest_id>/problem/<problem_number>')
def problem_view(contest_id, problem_number):
    username = request.args.get('username', 'Anonymous')
    contest = contests.get(contest_id)
    
    if not contest:
        return "Contest non trouvé", 404
    
    try:
        problem_index = int(problem_number) - 1
        if problem_index < 0 or problem_index >= len(contest['problems']):
            return "Problème non trouvé", 404
        
        problem_id = contest['problems'][problem_index]
    except (ValueError, IndexError):
        return "Problème non trouvé", 404
    
    # Vérifier si le problème est déjà résolu
    already_solved = is_problem_solved(username, contest_id, problem_id)
    
    problem_path = os.path.join('problems', problem_id)
    statement_path = os.path.join(problem_path, 'statement.md')
    
    statement = ""
    if os.path.exists(statement_path):
        with open(statement_path, 'r', encoding='utf-8') as f:
            statement = f.read()
    
    meta_path = os.path.join(problem_path, 'meta.json')
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            meta = json.load(f)
    
    return render_template('problem.html',
                         contest_id=contest_id,
                         problem_number=problem_number,
                         problem_id=problem_id,
                         statement=statement,
                         meta=meta,
                         username=username,
                         already_solved=already_solved)

@app.route('/contest/<contest_id>/leaderboard')
def leaderboard_view(contest_id):
    contest = contests.get(contest_id)
    if not contest:
        return "Contest non trouvé", 404
    
    return render_template('leaderboard.html', 
                         contest=contest,
                         contest_id=contest_id)

# ========================================
# ROUTES - CREATOR
# ========================================

@app.route('/creator', methods=['GET', 'POST'])
def creator():
    if request.method == 'POST':
        duration = int(request.form.get('duration', 15))
        difficulty = request.form.get('difficulty', 'easy')
        num_problems = int(request.form.get('num_problems', 3))
        
        contest_id = str(uuid.uuid4())[:8].upper()
        
        factory = ContestFactory()
        try:
            problems = factory.generate_contest(num_problems, difficulty)
            
            contests[contest_id] = {
                'id': contest_id,
                'duration': duration * 60,
                'difficulty': difficulty,
                'num_problems': num_problems,
                'problems': problems,
                'remaining_time': duration * 60,
                'active': True,
                'created_at': time.time()
            }
            
            global active_contest_id
            active_contest_id = contest_id
            
            return render_template('contest_created.html', 
                                 contest_id=contest_id, 
                                 contest=contests[contest_id])
        except ValueError as e:
            return f"Erreur : {str(e)}", 400
    
    return render_template('creator.html')

@app.route('/creator/contests')
def creator_contests():
    return render_template('creator_contests.html', contests=contests)

# ========================================
# ROUTES - ADMIN DASHBOARD
# ========================================

@app.route('/admin/workers')
def admin_workers():
    return render_template('admin_workers.html')

@app.route('/admin/activity')
def admin_activity():
    return render_template('admin_activity.html')

@app.route('/admin/logs')
def admin_logs():
    return render_template('admin_logs.html')

# ========================================
# API ENDPOINTS (JSON)
# ========================================

@app.route('/api/contests')
def api_contests():
    return jsonify(list(contests.values()))

@app.route('/api/contest/<contest_id>')
def api_contest(contest_id):
    contest = contests.get(contest_id)
    if not contest:
        return jsonify({"error": "Contest non trouvé"}), 404
    return jsonify(contest)

@app.route('/api/contest/<contest_id>/leaderboard')
def api_leaderboard(contest_id):
    return jsonify(leaderboard_instance.get_leaderboard())

@app.route('/api/workers')
def api_workers():
    return jsonify(workers_status)

@app.route('/api/queue')
def api_queue():
    return jsonify({"size": queue_instance.size()})

@app.route('/api/logs')
def api_logs():
    return jsonify(submissions_log[-20:])

@app.route('/api/submit', methods=['POST'])
def api_submit():
    """API : Soumettre du code avec validation complète"""
    data = request.json
    
    username = data.get('username')
    problem_id = data.get('problem_id')
    language = data.get('language')
    code = data.get('code')
    contest_id = data.get('contest_id')
    
    # Validation 1: Données manquantes
    if not all([problem_id, language, code, username, contest_id]):
        return jsonify({"error": "Données manquantes"}), 400
    
    # Validation 2: Contest existe
    contest = contests.get(contest_id)
    if not contest:
        return jsonify({"error": "Contest non trouvé"}), 404
    
    # Validation 3: Contest actif
    if not contest.get('active', False):
        return jsonify({"error": "Le contest est terminé"}), 403
    
    # Validation 4: Temps restant
    if contest.get('remaining_time', 0) <= 0:
        return jsonify({"error": "Le temps du contest est écoulé"}), 403
    
    # Validation 5: Langage supporté
    supported_languages = ['python', 'cpp', 'java']
    if language not in supported_languages:
        return jsonify({
            "error": f"Langage '{language}' non supporté. Langages autorisés: {', '.join(supported_languages)}"
        }), 400
    
    # Validation 6: Code non vide
    if len(code.strip()) == 0:
        return jsonify({"error": "Le code est vide"}), 400
    
    # Validation 7: Code trop long
    if len(code) > 50000:
        return jsonify({"error": "Le code est trop long (max 50000 caractères)"}), 400
    
    # Validation 8: Problème déjà résolu
    if is_problem_solved(username, contest_id, problem_id):
        return jsonify({
            "error": "Vous avez déjà résolu ce problème",
            "already_solved": True
        }), 403
    
    # Validation 9: Problème existe dans le contest
    if problem_id not in contest.get('problems', []):
        return jsonify({"error": "Ce problème ne fait pas partie de ce contest"}), 404
    
    submission_id = str(uuid.uuid4())[:8]
    
    submission = {
        "id": submission_id,
        "username": username,
        "problem_id": problem_id,
        "language": language,
        "status": "pending",
        "timestamp": time.time(),
        "contest_id": contest_id,
        "code_length": len(code)
    }
    
    submissions_log.append(submission)
    
    # Simuler l'évaluation avec le vrai judge
    import threading
    from judge.judge_engine import JudgeEngine
    
    def evaluate_submission():
        try:
            engine = JudgeEngine()
            
            task = {
                "username": username,
                "problem_id": problem_id,
                "language": language,
                "code": code
            }
            
            result = engine.judge(task)
            verdict = result.get("verdict", "SYSTEM_ERROR")
            
            # Mettre à jour le leaderboard
            leaderboard_instance.update(username, verdict)
            
            # Si OK, marquer comme résolu
            if verdict == "OK":
                mark_problem_solved(username, contest_id, problem_id)
            
            # Mettre à jour le statut
            for sub in submissions_log:
                if sub['id'] == submission_id:
                    sub['status'] = verdict
                    sub['verdict'] = verdict
                    if 'error' in result:
                        sub['error'] = result['error']
                    break
                    
        except Exception as e:
            for sub in submissions_log:
                if sub['id'] == submission_id:
                    sub['status'] = 'SYSTEM_ERROR'
                    sub['verdict'] = 'SYSTEM_ERROR'
                    sub['error'] = str(e)
                    break
    
    threading.Thread(target=evaluate_submission, daemon=True).start()
    
    # Simuler un worker qui prend la tâche
    for worker in workers_status:
        if worker["status"] == "idle":
            worker["status"] = "running"
            worker["task"] = f"{problem_id} ({username})"
            
            def reset_worker():
                time.sleep(3)
                worker["status"] = "idle"
                worker["task"] = None
            
            threading.Thread(target=reset_worker, daemon=True).start()
            break
    
    return jsonify({
        "success": True,
        "submission_id": submission_id,
        "message": "Soumission reçue et en cours d'évaluation"
    })

@app.route('/api/submission/<submission_id>/status')
def api_submission_status(submission_id):
    """API : Statut d'une soumission"""
    for sub in submissions_log:
        if sub['id'] == submission_id:
            return jsonify(sub)
    
    return jsonify({"error": "Soumission non trouvée"}), 404

@app.route('/api/problem/solved', methods=['POST'])
def api_check_solved():
    """Vérifie si un problème est résolu"""
    data = request.json
    username = data.get('username')
    contest_id = data.get('contest_id')
    problem_id = data.get('problem_id')
    
    solved = is_problem_solved(username, contest_id, problem_id)
    return jsonify({"solved": solved})

# ========================================
# LANCEMENT DU SERVEUR
# ========================================

if __name__ == '__main__':
    print(f"🚀 Dashboard démarré sur http://{DASHBOARD_HOST}:{DASHBOARD_PORT}")
    print(f"📊 Pages disponibles :")
    print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/ (Accueil)")
    print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/contests (Liste contests)")
    print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/creator (Créer un contest)")
    print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/admin/workers (Workers)")
    
    app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT, debug=True)