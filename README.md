# Shortify URL Shortener

![shortify_logo](media/shortify_logo.jpeg)

## Overview

**Shortify** is a URL shortener service written in Python using **FastAPI** as the web framework and **PostgreSQL** as the database. This application allows users to shorten long URLs into short, easy-to-share links. Additionally, it provides features for updating URLs, redirecting to the original URLs using shortcodes, and tracking statistics about redirects.

## Features

- **Shorten URLs** to a custom or randomly generated shortcode
- **Update** the URL associated with an existing shortcode
- **Redirect** to the original URL using the shortcode
- **Track statistics** like creation date, last redirect date, and redirect count

## Technologies Used

- **FastAPI**: Fast and modern web framework for building APIs with Python.
- **PostgreSQL**: Relational database for storing URL data.
- **SQLAlchemy**: ORM for interacting with the PostgreSQL database.
- **Docker**: For containerization of the app and running it in isolated environments.

## Folder Structure

The project follows **Domain-Driven Design (DDD)** principles to structure the code in a modular and maintainable way:

```
shortify/
│
├── app/
│   ├── api/                 # Routes and API endpoints
│   ├── core/                # Core configurations and utilities
│   ├── data/                # Database models and repository layer
│   ├── domain/              # Business logic layer
│   ├── main.py              # FastAPI application setup
│   └── tests/               # Test cases and testing utilities
├── Dockerfile               # Dockerfile for containerization
├── docker-compose.yml       # Docker Compose configuration
└── requirements.txt         # Project dependencies
```

## Endpoints

### POST /shorten

#### Request Body

```json
{
  "url": "https://www.example.com/",
  "shortcode": "abn123"
}
```

- **url**: The original URL to shorten.
- **shortcode** (optional): A custom shortcode provided by the user. If not provided, a random 6-character shortcode will be generated.

#### Response Body

```json
{
  "shortcode": "abn123",
  "update_id": "<update_id>"
}
```

- **shortcode**: The generated or provided shortcode for the URL.
- **update_id**: A unique identifier to update the URL for the given shortcode.

#### HTTP Status Codes

- **201**: Successfully created the shortcode.
- **400**: URL not present.
- **409**: Shortcode already in use.
- **412**: Invalid shortcode or URL.

---

### POST /update/{update_id}

#### Request Body

```json
{
  "url": "https://www.example.com/"
}
```

- **url**: The new URL to associate with the shortcode.

#### Response Body

```json
{
  "shortcode": "abn123"
}
```

#### HTTP Status Codes

- **201**: Successfully updated the URL.
- **400**: URL not present.
- **401**: Provided update ID does not exist.
- **412**: Invalid URL.

---

### GET /{shortcode}

#### HTTP Status Code

- **302**: Redirects to the original URL.
- **404**: Shortcode not found.

---

### GET /{shortcode}/stats

#### Response Body

```json
{
  "created": "2017-05-10T20:45:00.000Z",
  "lastRedirect": "2018-05-16T10:16:24.666Z",
  "redirectCount": 6
}
```

- **created**: The creation date of the shortcode in ISO8601 format.
- **lastRedirect**: The last time the shortcode was accessed in ISO8601 format.
- **redirectCount**: The number of times the shortcode has been used.

#### HTTP Status Codes

- **200**: Successfully retrieved statistics.
- **404**: Shortcode not found.

---

## Running the Application

To run the application, follow these steps:

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the PostgreSQL database**:

   ```bash
   docker-compose up -d
   ```

3. **Run the FastAPI app**:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the app** at [http://localhost:8000](http://localhost:8000).

---

## Running Tests

To run the tests inside Docker Compose, use the following command:

```bash
docker-compose run --rm shortify pytest
```

This will run `pytest` inside the existing `shortify` service container.

---

## Why Domain-Driven Development (DDD)?

Domain-Driven Development (DDD) is used to ensure that the application's architecture is clean, modular, and scalable. By organizing the code into distinct layers (e.g., domain, data, api), it becomes easier to maintain and extend the application over time. 

### Repository Pattern

The repository pattern is applied to abstract the data access layer, promoting separation of concerns and making the codebase easier to test and maintain. This ensures that business logic is not tightly coupled with database queries, allowing for scalability and flexibility.
