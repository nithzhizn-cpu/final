# SpySignal E2EE Backend — Railway v3

Простий бекенд для Railway, одна директорія:

- main.py
- models.py
- database.py
- schemas.py
- requirements.txt
- Procfile

## Локальний запуск

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Перевірка:
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs
