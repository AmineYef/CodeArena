# from judge.judge_engine import JudgeEngine
# import uuid
# import shutil
# import os

# def worker_process(task):
#     sandbox = f"data/tmp/{uuid.uuid4()}"
#     os.makedirs(sandbox, exist_ok=True)

#     try:
#         result = JudgeEngine.judge(task, sandbox)
#     finally:
#         shutil.rmtree(sandbox, ignore_errors=True)

#     return result


from judge.judge_engine import JudgeEngine
import os
import judge.executor
def worker_process(task):
    engine = JudgeEngine()
    result = engine.judge(task)
    return result
