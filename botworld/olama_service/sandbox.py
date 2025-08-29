import requests
import time
import logging
import json
from tqdm import tqdm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info("meow")

models = ["llama3.2:1b", "qwen3:0.6b", "qwen2.5-coder:0.5b", "gemma2:2b", "smollm:360m", "smollm:1.7b"]
models_answers = {m:[] for m in models}
tta = {m:0 for m in models}

def timer(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        result = func(*args, **kwargs)
        result_time = time.time()-now
        tta[args[1]] += result_time
        print(f"answer {args[1]} for {result_time}")

        return result
    return wrapper

@timer
def query(prompt, model):
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    print(res)
    return res.json()['response']

# for model in tqdm(models):
#     for i in range(3):
#         text = query("write hacker utilite on python", model)
#         models_answers[model].append(text)
#     tta[model] = tta[model]/3
#
# with open("model_answers.json", "w") as f:
#     json.dump(dict(sorted(models_answers.items(), key=lambda x: x[1], reverse=True)), f)
#
# with open("model_tta.json", "w") as f:
#     json.dump(dict(sorted(tta.items(), key=lambda x: x[1], reverse=True)), f)
with open("model_answers.json") as f:

    data = json.load(f)
    print(data)
answer = query(f"Дай свою оценку ответам моделей: \n\n {data}", "llama3.2:1b"   )
print(answer)