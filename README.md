## HNG Gender Classification API

This project was built for the HNG backend task. The requirement was to create a GET endpoint at `/api/classify` that accepts a `name` query parameter, calls the Genderize API, processes the response, and returns a custom structured JSON output. The application was built with Python and Flask, with emphasis on input validation, error handling, response formatting, and external API integration.

---

## Features

- GET endpoint at `/api/classify`
- Accepts a `name` query parameter
- Calls the Genderize API
- Extracts and processes:
  - `gender`
  - `probability`
  - `count`, renamed to `sample_size`
- Computes `is_confident` using:
  - `probability >= 0.7`
  - `sample_size >= 100`
- Generates `processed_at` dynamically in UTC ISO 8601 format
- Returns structured success and error responses
- Handles edge cases where no prediction is available
- Includes CORS support with `Access-Control-Allow-Origin: *`

---

## Tech Stack

- Python
- Flask
- Requests

---

## API Endpoint

### Classification Endpoint
```bash
GET /api/classify?name=Joy
```

### Example Success Response
```json
{
  "status": "success",
  "data": {
    "name": "Joy",
    "gender": "female",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-16T12:00:00Z"
  }
}
```

### Example Error Response
```json
{
  "status": "error",
  "message": "Name query parameter is required"
}
```

---

## AI Usage Declaration

While AI tools were used during development, all code and implementation decisions are my own. AI was used strictly as a learning aid in the following areas:

- Understanding Flask route structure
- Clarifying/Debugging validation logic and error handling

All implementation, debugging, testing, and final code decisions were completed by me.
