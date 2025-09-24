# Team Project: Jewelry Store Web Application

This is a **team project** developed as part of coursework.  
I worked as a **backend developer** using Python and FastAPI, and also took on some responsibilities of a **project manager**, coordinating tasks and reviewing code.  
Since this was a learning project, I also occasionally modified **JavaScript and HTML code** to meet project requirements.

The project is a **website for selling jewelry**, including product listings, detail pages, and order forms.

## 🛠️ Technologies Used

- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript (minor fixes)
- **Templates**: Jinja2
- **Database**: SQLAlchemy, SQLModel
- **Validation**: Pydantic
- **File Uploads**: python-multipart
- **HTTP requests**: httpx
- **Testing**: pytest

## 📁 Project Structure

Jewelry_Store/
│
├── app/ # Main application logic

│ ├── auth.py # User authentication and authorization

│ ├── database.py # Database connection

│ ├── models.py # SQLAlchemy models

│ ├── routes.py # Web routes

│ ├── schemas.py # Validation schemas

│ └── templates/ # Jinja2 HTML templates

│ ├── admin.html

│ ├── cart.html

│ ├── catalog.html

│ ├── checkout.html

│ ├── details.html

│ ├── email_already_registered.html

│ ├── error.html

│ ├── index.html

│ ├── orders.html

│ ├── order-success.html

│ └── registration.html
│
├── static/ # Static files (CSS, JS, images)

│ ├── styles/

│ ├── scripts/

│ └── images/
│
├── tests/ # Unit and integration tests

│ ├── conftest.py

│ ├── test_auth.py

│ ├── test_database.py

│ ├── test_models.py

│ ├── test_routes.py

│ └── test_schemas.py
│
├── init.py # App initialization

├── app.db # SQLite database file

├── requirements.txt # Dependencies

└── run.py # Entry point to start the server


## 📦 Installation & Running

1. Create a virtual environment and install dependencies:
pip install -r requirements.txt

Run the server:
uvicorn main:app --reload
Open your browser at http://127.0.0.1:8000

⚡ Notes
This project was educational, so some frontend code was adjusted by backend developers to meet course requirements.
Role included backend development, project management, and minor frontend corrections.
The site simulates a jewelry e-commerce platform.
Project documentation and task tracking were maintained using Confluence.
