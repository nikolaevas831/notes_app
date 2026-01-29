# Notes App

### Launching an application using Docker
1. **Clone repository**
   ```bash
   git clone https://github.com/nikolaevas831/notes_app.git
   cd notes_app
   ```
2. **Create .env file using .env.example**
    ```bash
    cp .env.example .env
   ```
3. **Run app**
    ```bash
    docker-compose up -d --build
   ```
4. **Access API**
    ```bash
    http://localhost:8000/docs
    ```
