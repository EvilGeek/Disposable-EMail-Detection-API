from flask import Flask, request, jsonify
import os
import urllib3
from utils import *
from database import Database

# Disable SSL warnings
urllib3.disable_warnings()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "DispoEMailAPI")  # Use environment variable for secret key

db = Database()

@app.route("/")
def home_api():
    """Health check endpoint."""
    return jsonify({"status": True})

@app.route("/api/disposable")
@app.route("/api/disposable/")
def disposable_api():
    try:
        email = request.args.get("email", None)
        domain = request.args.get("domain", None)

        # Validate email if provided
        if email and not is_valid_email(email):
            return jsonify({
                "status": False,
                "error": "Not a valid email provided."
            }), 400

        # If both email and domain are missing, return an error
        if not email and not domain:
            return jsonify({
                "status": False,
                "error": "At least provide email or domain param."
            }), 400

        # If email is provided, extract domain from it
        if not domain and email:
            domain = email.split("@")[1]

        # Email suggestion logic
        email_suggester = EmailSuggest()
        email_suggestion = email_suggester.suggest(domain)

        # MX Record Lookup
        mx_finder = MXRecordFinder()
        best_mx = mx_finder.get_best_mx(domain)

        best_mx_domain = best_mx["domain"] if best_mx else None

        # Check if the domain is public first
        is_public_domain = db.is_public_domain(domain)

        # Check if the domain or MX domain is disposable (only if not public)
        if is_public_domain:
            is_disposable = False  # If public, it's never disposable
        else:
            is_disposable = db.is_disposable_domain(domain)
            # Check the MX domain for disposability if it's not public
            if best_mx_domain:
                is_disposable = is_disposable or db.is_disposable_domain(best_mx_domain)

        # Prepare the response results
        results = {
            "status": True,
            "domain": domain,
            "is_disposable_domain": is_disposable,
            "is_public_domain": is_public_domain,
            "did_you_mean": None,
            "mx": bool(best_mx)  # True if MX records exist, False otherwise
        }

        # Suggest the corrected email if necessary
        if email and email_suggestion and not is_disposable:
            email_username = email.split("@")[0]
            results["did_you_mean"] = email_username + "@" + email_suggestion
        elif domain and email_suggestion and not is_disposable:
            results["did_you_mean"] = email_suggestion

        # Return the JSON response
        return jsonify(results)

    except Exception as e:
        # Log the error (optional, based on your logging setup)
        print(f"Error occurred: {str(e)}")
        return jsonify({"status": False, "error": "An error occurred, please try again later."}), 500

def setup():
    """Initial setup to load disposable and public domains into the database."""
    try:
        print("....STARTING SETUP....")
        DISPOSABLE_DOMAINS = disposable_domain_scrapper()
        print(f"Loaded {len(DISPOSABLE_DOMAINS)} disposable domains.")
        print("....SCRAPING DONE....")
        db.add_disposable_domain(DISPOSABLE_DOMAINS)
        print(f"Loaded {len(PUBLIC_DOMAINS)} public domains.")
        db.add_public_domain(PUBLIC_DOMAINS)
        print("....SETUP DONE....")
    except Exception as e:
        print(f"Setup failed: {str(e)}")

if __name__ == "__main__":
    setup()
    app.run(debug=True, host='0.0.0.0', port=5000)
