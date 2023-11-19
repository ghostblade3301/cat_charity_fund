# Учебный проект по fastapi - QRkot

## Установка
1. Склонируйте репозиторий:
```
git@github.com:ghostblade3301/cat_charity_fund.git
```
2. Перейдите в директорию с проектом:

```
cd cat_charity_fund
```

3. Cоздайте и активируйте виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```
4. Обновите пакетный менеджер pip:
```
python3 -m pip install --upgrade pip
```
5. Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
6. В корне проекта создайте файл .env и добавляем переменные окружения
```
APP_TITLE=QRKot
APP_DESCRIPTION=Сервис сбора пожертвований для котиков.
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=NEW_SECRET
```
7. Применяем миграции
```
alembic upgrade head 
```
## Запуск
Выполняем команду запуска
```
uvicorn app.main:app --reload
```
Документация будет доступна по адресу: http://127.0.0.1:8000/docs