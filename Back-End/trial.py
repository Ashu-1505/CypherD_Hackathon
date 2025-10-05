from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv() # This will load variables from .env into os.environ
app = Flask(__name__)
import os
# --- Supabase Configuration ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# --- Example route to create a row ---
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        # Expecting JSON input like: {"name": "John", "email": "john@example.com"}
        data = request.get_json()

        # Insert into table (example: "users")
        response = supabase.table("wallets").insert(data).execute()

        # Return inserted data or any message
        return jsonify({
            "status": "success",
            "data": response.data
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True)
