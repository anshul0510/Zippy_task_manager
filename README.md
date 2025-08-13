# 📝 Task Manager API

A RESTful API built using **Flask** for managing tasks.  
Supports **user authentication**, **CRUD operations**, **pagination**, and **task filtering**.

---

## 📌 Features
- User registration & login with **JWT authentication**.
- Create, read, update, and delete tasks.
- Pagination for task listing.
- Filter tasks by completion status.
- Timestamp for task creation and updates.
- Unit tests for authentication and tasks.

---

## 📂 Project Structure
ZIPPY TASK MANAGER/
│── app.py 
    │── routes/
    │ ├── auth_routes.py # Auth endpoints
    │ ├── task_routes.py # Task endpoints
    │── models.py # Database models
│── tests/
│ ├── test_auth.py # Auth tests
│ ├── test_tasks.py # Task tests
│── requirements.txt # Dependencies
│── README.md # Documentation
│── run.py # Entry point for Flask app

## ⚙️ Installation

### 1️⃣ Clone the repository
git clone https://github.com/anshul0510/Zippy_task_manager.git
cd project-name

### 2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

### 3️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Create .env file
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URI=sqlite:///tasks.db

### 5️⃣ Initialize the database
flask db init
flask db migrate
flask db upgrade

### 6️⃣ Run the server
flask run
Server runs at: http://127.0.0.1:5000/


🔐 Authentication
This API uses JWT for authentication.
Include the token in the Authorization header:Authorization: Bearer <your_token>

📡 API Endpoints
Auth:
Method	Endpoint	Description	Auth Required
POST	/auth/register	Register user	❌
POST	/auth/login	Login user	❌

Tasks
Method	Endpoint	Description	Auth Required
GET	/tasks	List tasks (paginated)	✅
GET	/tasks/<id>	Get task by ID	✅
POST	/tasks	Create new task	✅
PUT	/tasks/<id>	Update existing task	✅
DELETE	/tasks/<id>	Delete task	✅


🧪 Running Tests
pytest -v

🛠️ Built With
Flask – Web framework
Flask-JWT-Extended – Authentication
Flask-SQLAlchemy – ORM
Flask-Migrate – Migrations
Pytest – Testing framework

