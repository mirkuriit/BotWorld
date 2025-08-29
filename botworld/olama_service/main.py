import requests
import time
import logging
import json
from tqdm import tqdm

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename="meow.log")

model = OllamaLLM(model="mistral")

context = None
current_game_status = None

with open("design_doc.txt") as f:
    context = f.read()

with open("game_status.txt") as f:
    current_game_status = f.read()

with open("design_doc.txt") as f:
    context = f.read()

with open("game_status.txt") as f:
    current_game_status = f.read()
print(current_game_status)
prompt_template = """
Ты игровой AI. Используй следующий контекст об игре:
{context}

Текущее состояние игры:
{game_status}

Инструкция: {question}

Пожалуйста, сначала объясни свои рассуждения, почему ты выбираешь определенное направление, а затем дай ответ строго в формате: `move [направление]`.

Структура ответа:
РАССУЖДЕНИЕ: [твое объяснение здесь]
КОМАНДА: move [направление]

Ты можешь двигаться в 4 направлениях:
- up (вверх) - уменьшает номер строки
- down (вниз) - увеличивает номер строки  
- left (влево) - уменьшает номер столбца
- right (вправо) - увеличивает номер столбца

Пример правильного ответа:
РАССУЖДЕНИЕ: Я выбираю движение вправо, потому что там находится еда (f), которая увеличит мое здоровье на 10 единиц. Также это движение отдаляет меня от других игроков (e), снижая риск сражения.
КОМАНДА: move right

Твой ответ:
"""


prompt = ChatPromptTemplate.from_template(prompt_template)

chain = prompt | model

response = chain.invoke({
    "context": context,
    "game_status": current_game_status,
    "question": "Какой ход будет лучшим в текущей ситуации?"
})

print(response)






