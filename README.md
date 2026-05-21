# Контрольная работа №3 — FastAPI серверные технологии

## Установка и запуск

Запуск
py -3 -m venv .venv

Активируйте окружение:
.venv\Scripts\Activate.ps1
Linux/Macos
source .venv/bin/activate

Установите необходимые библиотеки:
pip install -r requirements.txt

Запустите сервер:
python -m uvicorn main:app --reload

Скопируйте .env.example в .env

cp .env.example .env

Запустите сервер

python -m uvicorn main:app --reload

In‑memory пользователи (fake_users_db):

admin / admin123 (роль admin)

user / user123 (роль user)

guest / guest123 (роль guest)