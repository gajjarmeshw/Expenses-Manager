# Expenses Manager App

The Expense Manager App is a web-based application built using Django, HTML, Bootstrap, and JavaScript. It allows users to track and manage their expenses effectively.

## Features

User Registration and Authentication: Users can create an account, log in, and log out securely.

Expense Tracking: Users can add, edit, and delete expenses, including details such as category, amount, date, and description.

Dashboard: Users can view a summary of their expenses, including total expenses, total expenses per day, and a pie chart representation of expenses by category.

## Installation

To run the Expense Manager App locally, follow these steps:
1. Clone the repository or download the source code.
2. Install Python (version 3.7 or higher) if you haven't already.
3. Create a virtual environment to keep the project dependencies isolated:

```bash
python3 -m venv expense_manager_venv
```

4. Activate the virtual environment:
For Windows:
```
expense_manager_venv\Scripts\activate
```

For Linux:
```
source expense_manager_venv/bin/activate
```

5. Navigate to the project directory:
```bash
cd expenseswebsite
```

6. Install the project dependencies:
```
pip install -r requirements.txt
```
7. Apply the database migrations:
```
python manage.py migrate
```
8. Start the development server:
```
python manage.py runserver
```
9. Open your web browser and visit http://localhost:8000 to access the Expense Manager App.

Happy expense tracking!

