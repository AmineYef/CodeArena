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
from collections import defaultdict

app = Flask(__name__)

@app.template_filter('markdown')
def markdown_filter(text):
    """Convertit le markdown en HTML"""
    return markdown.markdown(text, extensions=['extra', 'codehilite', 'fenced_code'])

contests = {}
active_contest_id = None
leaderboard_instance = Leaderboard()
queue_instance = TaskQueue()

solved_problems = {}  


attempts_tracking = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))


user_scores = defaultdict(lambda: defaultdict(int))


workers_status = [
    {"id": 1, "status": "idle", "task": None},
    {"id": 2, "status": "idle", "task": None},
    {"id": 3, "status": "idle", "task": None},
    {"id": 4, "status": "idle", "task": None},
]

submissions_log = []



def detect_language(code):
    """Détecte le langage de programmation à partir du code"""
    if not code:
        return None
    
    lines = [line.strip() for line in code.split('\n')]
    
 
    python_keywords = [
        'def ', 'import ', 'from ', 'print(', 'if __name__ == "__main__"',
        'elif ', 'else:', 'try:', 'except ', 'with ', 'as ', 'lambda ',
        'class ', '__init__', 'self.', 'return '
    ]
    

    cpp_keywords = [
        '#include', 'using namespace', 'cout <<', 'cin >>', 'std::',
        'int main()', 'void ', 'public:', 'private:', 'class ',
        'return 0;', '<< endl', '#define '
    ]
    

    java_keywords = [
        'public class', 'public static void main', 'System.out.println',
        'import java.', 'String[] args', 'public void ', 'private void ',
        'class ', 'extends ', 'implements ', 'new ', 'throws '
    ]
    
    python_score = sum(1 for line in lines for keyword in python_keywords if keyword in line)
    cpp_score = sum(1 for line in lines for keyword in cpp_keywords if keyword in line)
    java_score = sum(1 for line in lines for keyword in java_keywords if keyword in line)
    
    scores = {
        'python': python_score,
        'cpp': cpp_score,
        'java': java_score
    }
    
    max_score = max(scores.values())
    if max_score > 0:
        for lang, score in scores.items():
            if score == max_score:
                return lang
    
    return None

def increment_attempt(username, contest_id, problem_id):
    """Incrémente le compteur de tentatives pour un problème"""
    attempts_tracking[username][contest_id][problem_id] += 1

def get_attempt_count(username, contest_id, problem_id):
    """Récupère le nombre de tentatives pour un problème"""
    return attempts_tracking[username][contest_id][problem_id]

def is_problem_solved(username, contest_id, problem_id):
    """Vérifie si un problème est résolu par un utilisateur"""
    if username not in solved_problems:
        return False
    if contest_id not in solved_problems[username]:
        return False
    return solved_problems[username][contest_id].get(problem_id, False)

def mark_problem_solved(username, contest_id, problem_id):
    """Marque un problème comme résolu"""
    if username not in solved_problems:
        solved_problems[username] = {}
    if contest_id not in solved_problems[username]:
        solved_problems[username][contest_id] = {}
    solved_problems[username][contest_id][problem_id] = True

def update_user_score(username, contest_id, verdict):
    """Met à jour le score d'un utilisateur selon le verdict"""
    if contest_id not in user_scores[username]:
        user_scores[username][contest_id] = 0
    
    if verdict == "OK":
        user_scores[username][contest_id] += 100
    elif verdict == "WRONG_ANSWER":
        user_scores[username][contest_id] -= 10
    elif verdict == "TIMEOUT":
        user_scores[username][contest_id] -= 20
    elif verdict in ["RUNTIME_ERROR", "COMPILATION_ERROR", "SYSTEM_ERROR"]:
        user_scores[username][contest_id] -= 10
    

    user_scores[username][contest_id] = max(0, user_scores[username][contest_id])
    

    leaderboard_instance.update(username, verdict)
    
    return user_scores[username][contest_id]

def get_user_stats(username, contest_id):
    """Récupère les statistiques d'un utilisateur pour un contest"""
    contest = contests.get(contest_id)
    if not contest:
        return {"solved": 0, "total": 0, "total_attempts": 0, "score": 0}
    
    solved_count = 0
    total_attempts = 0
    if username in solved_problems and contest_id in solved_problems[username]:
        solved_count = sum(1 for pid in contest['problems'] 
                          if solved_problems[username][contest_id].get(pid, False))
    
    if username in attempts_tracking and contest_id in attempts_tracking[username]:
        for problem_id in contest['problems']:
            total_attempts += attempts_tracking[username][contest_id].get(problem_id, 0)
    
    score = user_scores[username].get(contest_id, 0)
    
    return {
        "solved": solved_count,
        "total": len(contest['problems']),
        "total_attempts": total_attempts,
        "score": score
    }

def calculate_user_position(username, contest_id):
    """Calcule la position de l'utilisateur dans le classement"""
    user_scores_list = []
    for user in user_scores:
        if contest_id in user_scores[user]:
            score = user_scores[user][contest_id]
            solved = 0
            if user in solved_problems and contest_id in solved_problems[user]:
                contest_probs = contests.get(contest_id, {}).get('problems', [])
                solved = sum(1 for pid in contest_probs 
                           if solved_problems[user][contest_id].get(pid, False))
            user_scores_list.append({
                'user': user,
                'score': score,
                'solved': solved
            })
    
    user_scores_list.sort(key=lambda x: (-x['score'], -x['solved']))
    
    for i, user_data in enumerate(user_scores_list):
        if user_data['user'] == username:
            return i + 1
    
    return None


@app.route('/')
def index():
    return render_template('index.html')


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
    

    problems_numbered = []
    for idx, problem_id in enumerate(contest['problems'], 1):
        solved = is_problem_solved(username, contest_id, problem_id)
        attempts = get_attempt_count(username, contest_id, problem_id)
        problems_numbered.append({
            'number': idx,
            'id': problem_id,
            'solved': solved,
            'attempts': attempts if attempts > 0 else None
        })
    
    stats = get_user_stats(username, contest_id)
    
    position = calculate_user_position(username, contest_id)
    
    return render_template('contest_dashboard.html', 
                         contest=contest, 
                         contest_id=contest_id,
                         username=username,
                         problems_numbered=problems_numbered,
                         user_stats=stats,
                         user_position=position)

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
    

    already_solved = is_problem_solved(username, contest_id, problem_id)

    attempts = get_attempt_count(username, contest_id, problem_id)
    
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
    
    stats = get_user_stats(username, contest_id)
    
    return render_template('problem.html',
                         contest_id=contest_id,
                         problem_number=problem_number,
                         problem_id=problem_id,
                         statement=statement,
                         meta=meta,
                         username=username,
                         already_solved=already_solved,
                         attempts=attempts,
                         current_score=stats['score'])

@app.route('/contest/<contest_id>/leaderboard')
def leaderboard_view(contest_id):
    contest = contests.get(contest_id)
    if not contest:
        return "Contest non trouvé", 404
    
    return render_template('leaderboard.html', 
                         contest=contest,
                         contest_id=contest_id)



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


@app.route('/admin/workers')
def admin_workers():
    return render_template('admin_workers.html')

@app.route('/admin/activity')
def admin_activity():
    return render_template('admin_activity.html')

@app.route('/admin/logs')
def admin_logs():
    return render_template('admin_logs.html')



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

    leaderboard_data = []
    
    
    all_users = set()
    for user in solved_problems:
        if contest_id in solved_problems[user]:
            all_users.add(user)
    for user in attempts_tracking:
        if contest_id in attempts_tracking[user]:
            all_users.add(user)
    
    for username in all_users:
        stats = get_user_stats(username, contest_id)
        position = calculate_user_position(username, contest_id)
        
        leaderboard_data.append({
            'user': username,
            'solved': stats['solved'],
            'total_attempts': stats['total_attempts'],
            'score': stats['score'],
            'position': position,
            'success_rate': round((stats['solved'] * 100 / stats['total_attempts']), 1) if stats['total_attempts'] > 0 else 0
        })
    
   
    leaderboard_data.sort(key=lambda x: (-x['score'], -x['solved'], x['total_attempts']))
    
    return jsonify(leaderboard_data)

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
    
  
    if not all([problem_id, language, code, username, contest_id]):
        return jsonify({"error": "Données manquantes"}), 400
    
  
    contest = contests.get(contest_id)
    if not contest:
        return jsonify({"error": "Contest non trouvé"}), 404
    
  
    if not contest.get('active', False):
        return jsonify({"error": "Le contest est terminé"}), 403
    
 
    if contest.get('remaining_time', 0) <= 0:
        return jsonify({"error": "Le temps du contest est écoulé"}), 403
    
 
    supported_languages = ['python', 'cpp', 'java']
    if language not in supported_languages:
        return jsonify({
            "error": f"Langage '{language}' non supporté. Langages autorisés: {', '.join(supported_languages)}"
        }), 400
    

    if len(code.strip()) == 0:
        return jsonify({"error": "Le code est vide"}), 400
    

    if len(code) > 50000:
        return jsonify({"error": "Le code est trop long (max 50000 caractères)"}), 400
    

    detected_language = detect_language(code)
    if detected_language and detected_language != language:
        return jsonify({
            "error": f"Langage incorrect. Le code semble être écrit en {detected_language.upper()}, mais vous avez sélectionné {language.upper()}.",
            "detected_language": detected_language,
            "selected_language": language,
            "code": "LANGUAGE_MISMATCH"
        }), 400
    

    if is_problem_solved(username, contest_id, problem_id):
        return jsonify({
            "warning": "Vous avez déjà résolu ce problème. Vous ne pouvez plus soumettre de solution.",
            "already_solved": True,
            "blocked": True
        }), 403  
    

    if problem_id not in contest.get('problems', []):
        return jsonify({"error": "Ce problème ne fait pas partie de ce contest"}), 404
    

    increment_attempt(username, contest_id, problem_id)
    attempts = get_attempt_count(username, contest_id, problem_id)
    
    submission_id = str(uuid.uuid4())[:8]
    
    submission = {
        "id": submission_id,
        "username": username,
        "problem_id": problem_id,
        "language": language,
        "status": "pending",
        "timestamp": time.time(),
        "contest_id": contest_id,
        "code_length": len(code),
        "detected_language": detected_language,
        "attempt_number": attempts
    }
    
    submissions_log.append(submission)
    

    import threading
    
    def evaluate_submission():
        try:
            from judge.judge_engine import JudgeEngine
            engine = JudgeEngine()
            
            task = {
                "username": username,
                "problem_id": problem_id,
                "language": language,
                "code": code
            }
            
            result = engine.judge(task)
            verdict = result.get("verdict", "SYSTEM_ERROR")
            

            update_user_score(username, contest_id, verdict)
            

            if verdict == "OK":
                mark_problem_solved(username, contest_id, problem_id)
            

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

            update_user_score(username, contest_id, "SYSTEM_ERROR")
    
    threading.Thread(target=evaluate_submission, daemon=True).start()
    

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
        "message": "Soumission reçue et en cours d'évaluation",
        "detected_language": detected_language,
        "already_solved": False,
        "attempt_number": attempts
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
    attempts = get_attempt_count(username, contest_id, problem_id)
    return jsonify({"solved": solved, "attempts": attempts})

@app.route('/api/detect-language', methods=['POST'])
def api_detect_language():
    """API pour détecter le langage du code"""
    data = request.json
    code = data.get('code', '')
    
    detected = detect_language(code)
    
    return jsonify({
        "detected_language": detected,
        "message": f"Langage détecté: {detected.upper()}" if detected else "Impossible de détecter le langage"
    })

@app.route('/api/user/stats/<contest_id>/<username>')
def api_user_stats(contest_id, username):
    """API pour récupérer les statistiques d'un utilisateur"""
    stats = get_user_stats(username, contest_id)
    position = calculate_user_position(username, contest_id)
    
    return jsonify({
        **stats,
        "position": position
    })

@app.route('/api/contest/<contest_id>/position/<username>')
def api_user_position(contest_id, username):
    """API pour récupérer la position d'un utilisateur"""
    position = calculate_user_position(username, contest_id)
    return jsonify({"position": position})



if __name__ == '__main__':
    print(f"🚀 Dashboard démarré sur http://{DASHBOARD_HOST}:{DASHBOARD_PORT}")
    print(f"📊 Pages disponibles :")
    print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/ (Accueil)")
    print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/contests (Liste contests)")
    print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/creator (Créer un contest)")
    print(f"   - http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/admin/workers (Workers)")
    
    app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT, debug=True)