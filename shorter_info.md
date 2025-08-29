No problem! Let's fix that. It's actually better to not have an `.env` 

---

### 🏃‍♂️ Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AhrimanXD/ecommerce-api-with-fastapi/
    cd ecommerce-api-with-fastapi
    ```

2.  **Start the containers:**
    This command will start PostgreSQL, Redis, and the FastAPI server. The API will be available shortly.
    ```bash
    docker-compose up -d
    ```

3.  **Initialize the Database (First-Time Setup):**
    The database starts empty. To create the tables and seed it with sample products and categories, run:
    ```bash
    # Run the schema creation and seeding script
    docker-compose exec db psql -U postgres -d app -f /docker-entrypoint-initdb.d/seed.sql
    ```
    *Note: The seed script defines the product units as `('KG', 'G', 'LITER', 'PIECE')` to match the application's enum.*

4.  **Access the Application:**
    - **API Server:** http://localhost:8000
    - **Interactive API Docs (Swagger UI):** http://localhost:8000/docs
    - **Alternative API Docs (ReDoc):** http://localhost:8000/redoc

5.  **(Optional) Run Tests:**
    Execute the test suite to verify everything is working correctly.
    ```bash
    docker-compose exec web pytest -v
    ```

---

### Important Note on Configuration

This project uses default development credentials for simplicity. The configuration is hardcoded in `app/core/config.py` for now. **For a production deployment, you should:**

1.  Create an `.env` file:
    ```bash
    # .env
    DATABASE_URL=postgresql://user:strongpassword@hostname/dbname
    SECRET_KEY=your-super-secret-key-here
    ```
2.  Modify the application to read these values from environment variables instead of the config file.
