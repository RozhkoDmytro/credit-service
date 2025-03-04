# Credit Service

## Description
Credit Service is a web service that facilitates financial operations, such as managing credits, payments, and financial plans. The API is built using Django REST Framework (DRF) and relies on MySQL/MS SQL for data storage.

## Technologies
- **Programming Language**: Python 3.9+
- **Framework**: Django 4+ / Django REST Framework
- **Database**: MySQL or MS SQL
- **ORM**: Django's built-in ORM

## Installation and Setup

You can run the service either manually or using Docker. Choose one of the following methods:

### Manual Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/RozhkoDmytro/credit-service.git
   cd credit-service
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows, use 'env\Scripts\activate'
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `example.env` to `.env`:
     ```sh
     cp example.env .env
     ```
   - Update `.env` with your database credentials and other configurations.

5. **Apply database migrations:**
   ```sh
   python manage.py migrate
   ```

6. **Load initial data:**
   - Place your CSV files in the `static/csv_files/` directory.
   - Run the data loading script:
     ```sh
     python manage.py import_csv
     ```

7. **Start the development server:**
   ```sh
   python manage.py runserver
   ```

### Docker Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/RozhkoDmytro/credit-service.git
   cd credit-service
   ```

2. **Build and start the Docker containers:**
   ```sh
   docker-compose up --build
   ```

3. **Apply database migrations inside the web container:**
   ```sh
   docker-compose exec web python manage.py migrate
   ```

4. **Load initial data:**
   ```sh
   docker-compose exec web python manage.py import_csv
   ```

The service should now be accessible at `http://localhost:8000/`.
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

- **Retrieve User Credits:** `GET /user_credits/{user_id}/`
- **Upload Plans:** `POST /plans_insert/` (Accepts an Excel file)

## API Endpoints (in plans)
- **Plan Performance Evaluation:** `GET /plans_performance/?date=YYYY-MM-DD`
- **Annual Summary Report:** `GET /year_performance/?year=YYYY`

## Testing

1. **Ensure test dependencies are installed:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Run tests:**
   ```sh
   python manage.py test
   ```

## Postman Configuration

A Postman collection is available in the repository as `Credit-service.postman_collection.json`. To use it:

1. **Import the collection:**
   - Open Postman.
   - Click on **Import**.
   - Select the `Credit-service.postman_collection.json` file from the repository.

2. **Set up environment variables:**
   - Configure the necessary environment variables in Postman to match your local setup.

3. **Execute requests:**
   - Use the imported collection to test the API endpoints.

## Test Data

Sample test data is located in the `static/test_xlsx/` directory. Ensure that the Excel files are formatted correctly before uploading them through the `/plans_insert/` endpoint.

## License

This project is licensed under the Unlicense License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or suggestions, contact us via email: [d.rozhko.ua@gmail.com](mailto\:d.rozhko.ua@gmail.com)
