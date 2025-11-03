# Notes App

### Запуск приложения с помощью Docker
1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/nikolaevas831/notes_app.git
   cd notes_app
   ```
2. **Создайте .env файл по примеру .env.example**
    ```bash
    cp .env.example .env
   ```
Отредактируйте .env при необходимости
3. **Запустите приложение**
    ```bash
    docker-compose up -d --build
   ```