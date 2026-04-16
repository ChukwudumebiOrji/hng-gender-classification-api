from flask import Flask, request, jsonify
from datetime import datetime, timezone
import requests

app = Flask(__name__)

genderize_url = "https://api.genderize.io"


def make_error_message(message, status_code):
    response = jsonify({
        "status": "error",
        "message": message
    })
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response, status_code


def make_success_message(data):
    response = jsonify({
        "status": "success",
        "data": data
    })
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response, 200


@app.route("/")
def home():
    response = jsonify({"status": "success", "message": "Hello world!"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response, 200


@app.route("/api/classify", methods=["GET"])
def classify():
    name = request.args.get("name")

    if name is None or name.strip() == "":
        return make_error("Name query parameter is required", 400)

    if not isinstance(name, str):
        return make_error("Name must be a string", 422)

    try:
        response = requests.get(genderize_url, params={"name": name}, timeout=5)

        if response.status_code != 200:
            return make_error("Failed to fetch data from Genderize API", 502)

        api_data = response.json()

        gender = api_data.get("gender")
        probability = api_data.get("probability")
        count = api_data.get("count")

        if gender is None or count == 0:
            return make_error("No prediction available for the provided name", 422)

        is_confident = probability >= 0.7 and count >= 100

        processed_at = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

        result = {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": count,
            "is_confident": is_confident,
            "processed_at": processed_at
        }

        return make_success_message(result)

    except requests.RequestException:
        return make_error_message("Failed to connect to Genderize API", 502)
    except Exception:
        return make_error_message("Internal server error", 500)


if __name__ == "__main__":
    app.run(debug=True)
