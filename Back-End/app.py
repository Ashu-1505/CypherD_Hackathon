# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os
import random
from decimal import Decimal, getcontext

app = Flask(__name__)
CORS(app, supports_credentials=True)
from dotenv import load_dotenv
load_dotenv() # This will load variables from .env into os.environ
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
print(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
getcontext().prec = 50

@app.route("/create_wallet", methods=["POST"])
def create_wallet():
    try:
        body = request.get_json()
        address = (body.get("address"))
        if not address:
            return jsonify({"error": "address required"}), 400

        # Random mock ETH balance between 1 and 10
        balance_eth = 8.5
        print(address)
        # Insert row
        response = supabase.table("wallets").insert({
            "address": address,
            "balance_eth": balance_eth
        }).execute()

        # Check for Supabase errors
        if getattr(response, "error", None):
            return jsonify({"error": "Supabase insert failed", "details": str(response.error)}), 500

        # Success response
        return jsonify({"address": address, "balance_eth": str(balance_eth)}), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "internal server error", "details": str(e)}), 500

@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):
    try:
        addr = address.strip().lower()
        print(addr, address)
        response = supabase.table("wallets").select("balance_eth").eq("address", addr).single().execute()

        if getattr(response, "error", None):
            return jsonify({"error": "Supabase select failed", "details": str(response.error)}), 500

        if not getattr(response, "data", None):
            return jsonify({"error": "Wallet not found"}), 404

        balance = response.data.get("balance_eth")
        return jsonify({"address": addr, "balance_eth": str(balance)}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "internal server error", "details": str(e)}), 500

from datetime import datetime

@app.route("/send_eth", methods=["POST","OPTIONS"])
def send_eth():
    if request.method == "OPTIONS":
        # Preflight request handled automatically by flask-cors
        return '', 200
    try:
        body = request.get_json()
        sender = (body.get("sender"))
        recipient = (body.get("recipient"))
        amount = body.get("amount")

        if not sender or not recipient or amount is None:
            return jsonify({"error": "sender, recipient, and amount required"}), 400
        
        return jsonify({"message": f"Sent {amount} ETH from {sender} to {recipient}"}), 200
        amount = Decimal(str(amount))

        # Fetch sender balance
        sender_res = supabase.table("wallets").select("balance_eth").eq("address", sender).single().execute()
        if not sender_res.data:
            return jsonify({"error": "Sender wallet not found"}), 404
        sender_balance = Decimal(sender_res.data["balance_eth"])

        if sender_balance < amount:
            return jsonify({"error": "Insufficient balance"}), 400

        # Deduct from sender
        supabase.table("wallets").update({"balance_eth": str(sender_balance - amount)}).eq("address", sender).execute()

        # Add to recipient (create if not exists)
        recipient_res = supabase.table("wallets").select("balance_eth").eq("address", recipient).single().execute()
        if recipient_res.data:
            recipient_balance = Decimal(recipient_res.data["balance_eth"])
            supabase.table("wallets").update({"balance_eth": str(recipient_balance + amount)}).eq("address", recipient).execute()
        else:
            # create recipient wallet with initial balance = amount
            supabase.table("wallets").insert({"address": recipient, "balance_eth": str(amount)}).execute()

        # Store transaction
        supabase.table("transactions").insert({
            "sender": sender,
            "recipient": recipient,
            "amount": str(amount),
            "timestamp": datetime.utcnow().isoformat()
        }).execute()

        return jsonify({"message": "Transfer successful"}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "internal server error", "details": str(e)}), 500

@app.route("/transactions/<address>", methods=["GET"])
def get_transactions(address):
    try:
        addr = address.strip().lower()

        response = supabase.table("transactions") \
            .select("*") \
            .or_(f"sender.eq.{addr},recipient.eq.{addr}") \
            .order("timestamp", desc=True) \
            .execute()

        if getattr(response, "error", None):
            return jsonify({"error": "Supabase select failed", "details": str(response.error)}), 500

        data = getattr(response, "data", [])
        return jsonify({"transactions": data}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=4000)
