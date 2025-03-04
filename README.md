# Credit Service

## Project Description

Credit Service is a web service that facilitates financial operations, such as managing credits, payments, and financial plans. The API is built using **Django REST Framework (DRF)** and relies on **MySQL/MS SQL** for data storage.

## Technologies

- **Python 3.9+**
- **Django 4+ / Django REST Framework**
- **SQLAlchemy** for database interaction
- **MySQL** as the primary database

## Installation and Setup

You can run the service either manually or using Docker. Choose one of the following methods:

### Docker Setup

To run the service using Docker, copy the `example.env` file to `.env` and configure it accordingly:

```bash
cp example.env .env
```

Then, build and start the container with:

```bash
docker-compose up --build
```

#### Environment Variables
Ensure your `.env` file is properly configured before running the container. Below are the required environment variables:

```ini
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db  # The service name in docker-compose
DB_PORT=3306  # or 1433 for MS SQL
```

## Manual Setup if you prefer running the service without Docker.

### 1. Clone the Repository

```bash
git clone https://github.com/RozhkoDmytro/credit-service
cd credit-service
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux & Mac
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project's root directory and add:

```ini
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306  # or 1433 for MS SQL
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Server

```bash
python manage.py runserver
```

## Project Structure

```plaintext
finance_project/
│── manage.py
│── finance_project/
│   ├── settings.py
│   ├── urls.py
│── users/  # User management
│── credits/  # Credit management
│── payments/  # Payment processing
│── plans/  # Planning
│── dictionary/  # Reference data
│── reports/  # Report generation
```

## API Endpoints

### **Credits**

- `GET /api/user_credits/{user_id}/` – Retrieve the credit history of a user

### **Payments**

- `POST /api/plans_insert/` – Upload financial plans for a new month
- `GET /api/plans_performance/?date=YYYY-MM-DD` – Get financial plan performance for a given date
- `GET /api/year_performance/?year=YYYY` – Retrieve annual analytics

## Testing

Run tests using:

```bash
python manage.py test
```

## Contact

For any inquiries or suggestions, contact us via email: [d.rozhko.ua@gmail.com](mailto\:d.rozhko.ua@gmail.com)

