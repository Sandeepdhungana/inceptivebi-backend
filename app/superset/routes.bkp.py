from flask import Blueprint, request, jsonify
import requests
import os
from yarl import URL

preset_bp = Blueprint('preset', __name__)



@preset_bp.route('/get-dashboard-details', methods=['GET'])
def get_dashboard():
    try:

        user_accessible_dashboard = []
        all_dashboard = get_all_dashboards()
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/json",
            "Referer": f"https://{os.getenv("WORKSPACE_SLUG")}.us1a.app.preset.io/"
        }
        jwt_token = authenticate_with_preset()
        for dashboard in all_dashboards:
            embedded_url = f"https://{os.getenv("WORKSPACE_SLUG")}.us1a.app.preset.io/api/v1/dashboard/{dashboard.get("id",-1)}/embedded"
            
            response = requests.get(embedded_url, headers=headers)
            if response.status_code == 200:
                user_accessible_dashboard.append({
                    "title":dashboard.title,
                    "uuid":dashboard.uuid
                })
        
        return jsonify(user_accessible_dashboard), 200


    except requests.exceptions.HTTPError as error:
        return jsonify({"error": str(error)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500        

@preset_bp.route("/guest-token", methods=["GET"])
def guest_token_generator():
    """
    Route used by frontend to retrieve a Guest Token.
    """
    try:
        jwt_token = authenticate_with_preset()
        guest_token = jsonify(fetch_guest_token(jwt_token))
        return guest_token, 200
    except requests.exceptions.HTTPError as error:
        return jsonify({"error": str(error)}), 500


def get_all_dashboards(page_size=100):
    all_dashboards = []
    page = 0

    jwt_token = authenticate_with_preset()
    while True:
        url = f"https://{os.getenv('WORKSPACE_SLUG')}.us1a.app.preset.io/api/v1/dashboard?q=(page_size:{page_size},page:{page})"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()

        dashboards = data.get('result', [])
        all_dashboards.extend(dashboards)
        
        if len(dashboards) < page_size:
            break
        
        page += 1

    return all_dashboards

    
       

def authenticate_with_preset():
    """
    Authenticate with the Preset API to generate a JWT token.
    """
    url =  URL("https://api.app.preset.io/") / "v1/auth/"
    payload = {"name": os.getenv('API_TOKEN'), "secret": os.getenv('API_SECRET')}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=7,
        )
        response.raise_for_status()
        return response.json()["payload"]["access_token"]
    except requests.exceptions.HTTPError as http_error:
        error_msg = http_error.response.text
        print("Unable to generate a token", error_msg)
        raise requests.exceptions.HTTPError(
            "Unable to generate a JWT token. "
            "Please make sure your API key is enabled.",
        )


def fetch_guest_token(jwt):
    """
    Fetch and return a Guest Token for the embedded dashboard.
    """
    url = (
        URL("https://api.app.preset.io/")
        / "v1/teams"
        / os.getenv('PRESET_TEAM')
        / "workspaces"
        / os.getenv('WORKSPACE_SLUG')
        / "guest-token/"
    )
    payload = {
        "user": {"username": "sandeepdhunganaoff@gmail.com", "first_name": "Sandeep", "last_name": "Dhungana"},
        "resources": [
            {"type": "dashboard", "id": "03a182c8-5e85-4dd9-a727-eedaa98a51f7"},
            {"type": "dashboard", "id": "02784bdb-6ed7-4d46-befe-9545b3ec3c55"},
            {"type": "dashboard", "id": "02784bdb-6ed7-4d46-befe-9545b3ec3c55"},
            ],
        "rls": [
            # Apply an RLS to a specific dataset
            # { "dataset": dataset_id, "clause": "column = 'filter'" },
            # Apply an RLS to all datasets
            # { "clause": "column = 'filter'" },
        ],
    }

    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=7,
        )
        response.raise_for_status()
        return response.json()["payload"]["token"]
    except requests.exceptions.HTTPError as http_error:
        error_msg = http_error.response.text
        print("Unable to fetch guest token ", error_msg)
        raise requests.exceptions.HTTPError(
            "Unable to generate a Guest token. "
            "Please make sure the API key has admin access and the payload is correct.",
        )