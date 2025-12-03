from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# Ajouter le chemin parent pour importer les modules server
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.settings import DASHBOARD_HOST, DASHBOARD_PORT
from server.contest_manager import ContestManager
from server.contest_factory import ContestFactory
from server.leaderboard import Leaderboard
from server.queue_manager import TaskQueue
import json
import uuid

app = Flask(__name__)

# ========================================
# VARIABLES GLOBALES (simuler état serveur)
# ========================================
# En production, ces objets seraient partagés avec le serveur TCP
# Pour la démo, on crée des instances séparées

contests = {}  # {contest_id: {info}}
active_contest_id = None
leaderboard_instance = Leaderboard()
queue_instance = TaskQueue()

# Simuler des workers
workers_status = [
    {"id": 1, "status": "idle", "task": None},
    {"id": 2, "status": "idle", "task": None},
    {"id": 3, "status": "idle", "task": None},
    {"id": 4, "status": "idle", "task": None},
]

submissions_log = []

# ========================================
# ROUTES - PAGE D'ACCUEIL
# ========================================

@app.route('/')
def index():
    """Page d'accueil avec navigation"""
    return render_template('index.html')


# ========================================
# ROUTES - CONTESTS (PARTICIPANTS)
# ========================================

@app.route('/contests')
def contests_list():
    """Liste des contests disponibles"""
    return render_template('contests.html', contests=contests)


@app.route('/contest/<contest_id>/join', methods=['GET', 'POST'])
def join_contest(contest_id):
    """Rejoindre un contest"""
    if request.method == 'POST':
        username = request.form.get('username', 'Anonymous')
        return redirect(url_for('contest_dashboard', contest_id=contest_id, username=username))
    
    contest = contests.get(contest_id)
    if not contest:
        return "Contest non trouvé", 404
    
    return render_template('join_contest.html', contest=contest, contest_id=contest_id)


@app.route('/contest/<contest_id>/dashboard')
def contest_dashboard(contest_id):
    """Dashboard du contest pour un participant"""
    username = request.args.get('username', 'Anonymous')
    contest = contests.get(contest_id)
    
    if not contest:
        return "Contest non trouvé", 404
    
    return render_template('contest_dashboard.html', 
                         contest=contest, 
                         contest_id=contest_id,
                         username=username)


@app.route('/contest/<contest_id>/problem/<problem_id>')
def problem_view(contest_id, problem_id):
    """Afficher un problème avec éditeur de code"""
    username = request.args.get('username', 'Anonymous')
    contest = contests.get(contest_id)
    
    if not contest or problem_id not in contest['problems']:
        return "Problème non trouvé", 404
    
    # Charger l'énoncé du problème
    problem_path = os.path.join('problems', problem_id)
    statement_path = os.path.join(problem_path, 'statement.md')
    
    statement = ""
    if os.path.exists(statement_path):
        with open(statement_path, 'r', encoding='utf-8') as f:
            statement = f.read()
    
    # Charger les métadonnées
    meta_path = os.path.join(problem_path, 'meta.json')
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            meta = json.load(f)
    
    return render_template('problem.html',
                         contest_id=contest_id,
                         problem_id=problem_id,
                         statement=statement,
                         meta=meta,
                         username=username)


@app.route('/contest/<contest_id>/leaderboard')
def leaderboard_view(contest_id):
    """Afficher le leaderboard du contest"""
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
    """Interface créateur de contest"""
    if request.method == 'POST':
        duration = int(request.form.get('duration', 15))
        difficulty = request.form.get('difficulty', 'easy')
        num_problems = int(request.form.get('num_problems', 3))
        
        # Créer le contest
        contest_id = str(uuid.uuid4())[:8].upper()
        
        factory = ContestFactory()
        try:
            problems = factory.generate_contest(num_problems, difficulty)
            
            contests[contest_id] = {
                'id': contest_id,
                'duration': duration * 60,  # convertir en secondes
                'difficulty': difficulty,
                'num_problems': num_problems,
                'problems': problems,
                'remaining_time': duration * 60,
                'active': True
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
    """Liste des contests créés"""
    return render_template('creator_contests.html', contests=contests)


# ========================================
# ROUTES - ADMIN DASHBOARD
# ========================================

@app.route('/admin/workers')
def admin_workers():
    """Vue des workers multiprocessing"""
    return render_template('admin_workers.html')


@app.route('/admin/activity')
def admin_activity():
    """Vue de l'activité du serveur"""
    return render_template('admin_activity.html')


@app.route('/admin/logs')
def admin_logs():
    """Logs du système"""
    return render_template('admin_logs.html')


# ========================================
# API ENDPOINTS (JSON)
# ========================================

@app.route('/api/contests')
def api_contests():
    """API : Liste des contests"""
    return jsonify(list(contests.values()))


@app.route('/api/contest/<contest_id>')
def api_contest(contest_id):
    """API : Détails d'un contest"""
    contest = contests.get(contest_id)
    if not contest:
        return jsonify({"error": "Contest non trouvé"}), 404
    return jsonify(contest)


@app.route('/api/contest/<contest_id>/leaderboard')
def api_leaderboard(contest_id):
    """API : Leaderboard d'un contest"""
    return jsonify(leaderboard_instance.get_leaderboard())


@app.route('/api/workers')
def api_workers():
    """API : État des workers"""
    return jsonify(workers_status)


@app.route('/api/queue')
def api_queue():
    """API : Taille de la queue"""
    return jsonify({"size": queue_instance.size()})


@app.route('/api/logs')
def api_logs():
    """API : Derniers logs"""
    return jsonify(submissions_log[-20:])  # 20 derniers logs


@app.route('/api/submit', methods=['POST'])
def api_submit():
    """API : Soumettre du code"""
    data = request.json
    
    username = data.get('username', 'Anonymous')
    problem_id = data.get('problem_id')
    language = data.get('language')
    code = data.get('code')
    
    if not all([problem_id, language, code]):
        return jsonify({"error": "Données manquantes"}), 400
    
    # Ajouter à la queue (simulation)
    submission_id = str(uuid.uuid4())[:8]
    
    submission = {
        "id": submission_id,
        "username": username,
        "problem_id": problem_id,
        "language": language,
        "status": "pending",
        "timestamp": "now"
    }
    
    submissions_log.append(submission)
    
    # Simuler un worker qui prend la tâche
    for worker in workers_status:
        if worker["status"] == "idle":
            worker["status"] = "running"
            worker["task"] = f"{problem_id} ({username})"
            break
    
    return jsonify({
        "success": True,
        "submission_id": submission_id,
        "message": "Soumission reçue"
    })


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