## Запуск
py -3 -m venv .venv
# 3. Активируйте окружение
.\.venv\Scripts\Activate.ps1
#Linux/Macos
source .venv/bin/activate
# Если предыдущая команда выдает ошибку красным цветом, используйте эту:
# .\.venv\Scripts\activate.bat
# 4. Установите необходимые библиотеки
pip install -r requirements.txt

cp .env.example .env
# 5. Запустите сервер
python -m uvicorn main:app --reload