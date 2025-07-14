Проект работает в телеграме под ником @YourHomeFinanceBot

# Описание проекта
Телеграм-бот, который записывает, показывает и удаляет расходы пользователя.   
Ввод расходов осуществляется в форме диалога реализованный с помощью механизма конечных автоматов (Finite State Machine).  
Пользователь выбирает категорию, вводит текст расхода и затем сумму.  
Расходы могут быть показаны по различному времени: за сегодня, за этот месяц, за прошлый месяц, за всё время и по категориям.  
Удаляется расход по его номеру (id).


# Запуск проекта через Dockerfile:

Клонировать репозиторий и перейти в него в терминале:
```bash
git clone https://github.com/NGC6543/FinanceBot.git
```

Создать файл .env и указать API токен бота:
```bash
API_TOKEN=*ТОКЕН БОТА*
POSTGRES_DB="finance"
DB_HOST=db
POSTGRES_USER=<ваш логин (обычно postgres)>
POSTGRES_PASSWORD=<ваш пароль>
DB_PORT=5432
```

Перейти в директорию infra:
```bash
cd infra/
```

Запустить образы из файла Docker-compose:
```bash
docker compose -f docker-compose.yml up -d --build
```


# Запуск проекта локально:
Клонировать репозиторий и перейти в него в терминале:
```bash 
git clone https://github.com/NGC6543/FinanceBot.git
```

Установить виртуальное окружение и установить зависимости
```bash
python -m venv venv
pip install -r requirements.txt
```

Установить PostgreSQL и запустить его
```bash
https://www.postgresql.org/download/
```

Создать файл .env и указать API токен бота:
```bash
API_TOKEN=*ТОКЕН БОТА*
POSTGRES_DB="finance"
DB_HOST=localhost
POSTGRES_USER=<ваш логин (обычно postgres)>
POSTGRES_PASSWORD=<ваш пароль>
DB_PORT=5432
```

Запустить бота:
```bash
python main_finance.py
```

# Стек технологий
- Python 3.11.0
- aiogram
- PostgreSQL
- Docker

