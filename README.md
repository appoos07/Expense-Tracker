# Daily Expenses Sharing Application

## Setup Instructions

1. Install dependencies:
   sudo apt update
   sudo apt install python3-pip
   python3 -m venv myenv
   source myenv/bin/activate
   pip install django
   pip install django djangorestframework  

4. Run migrations:
    python manage.py makemigrations
    python manage.py migrate

2. Start the development server:
    python manage.py runserver

## API Endpoints

- `POST /api/users/`: Create a new user.
- `GET /api/users/{id}/`: Retrieve user details.
- `POST /api/expenses/`: Add a new expense.
- `GET /api/expenses/{id}/`: Retrieve individual user expenses.
- `GET /api/expenses/`: Retrieve overall expenses.
- `GET /api/expenses/download/`: Download the balance sheet.

## Additional Notes

- Ensure percentages in the percentage split method add up to 100%.
- Include error handling and input validation.
