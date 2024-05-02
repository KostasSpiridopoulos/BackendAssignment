# FastAPI Application

This FastAPI application provides APIs to manage articles, authors, tags, and comments. The application includes sample data and offers functionality for users to interact with data through the provided APIs.

## Table of Contents
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Using the APIs](#using-the-apis)
- [Adding New Data](#adding-new-data)
- [License](#license)

## Setup

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/KostasSpiridopoulos/BackendAssignment.git
cd BackendAssignment
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

To initialize the database and add sample data, run:

```bash
python sample_data.py
```

This will populate the database with sample users, authors, tags, and articles.

## Running the Application

To start the FastAPI application, use the following command:

```bash
uvicorn main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

## Using the APIs

The application provides APIs to manage articles, authors, tags, and comments. Once the application is running, you can interact with the APIs through the automatically generated Swagger UI available at:

```
http://127.0.0.1:8000/docs
```

Here you can:
- Create and manage articles, authors, and tags.
- Add comments to articles.
- Query articles based on different criteria.

## Adding New Data

- **Via API**: Use the provided APIs to add authors, tags, articles, and comments.
- **Via Sample Data**: Modify the `sample_data.py` file to include more sample data and run the script again to add the data to the database.

## License

This project is licensed under the [MIT License](LICENSE).
```

This `README.md` file provides detailed information on how to set up the FastAPI application, initialize the database, and interact with the APIs. It also includes a section on how to add new data, both through the APIs and the `sample_data.py` script.
