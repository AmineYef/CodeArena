from judge.judge_engine import JudgeEngine
import os
import judge.executor
def worker_process(task):
    engine = JudgeEngine()
    result = engine.judge(task)
    return result
