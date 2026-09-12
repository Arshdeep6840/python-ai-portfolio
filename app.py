import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Import the hardcoded data
from data import PROFILE, SKILLS, PROJECTS, EXPERIENCE, EDUCATION, CERTIFICATIONS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    register_routes(app)
    return app


def register_routes(app):
    @app.route("/")
    def index():
        return render_template(
            "index.html",
            profile=PROFILE,
            skills=SKILLS,
            projects=PROJECTS,
            experience=EXPERIENCE,
            education=EDUCATION,
            certifications=CERTIFICATIONS,
        )

    @app.route("/contact", methods=["POST"])
    def contact():
        """Handle contact form using Resend API."""
        data = request.get_json(silent=True) or request.form

        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()

        if not name or not email or not message:
            return jsonify(ok=False, error="All fields are required."), 400

        api_key = os.environ.get("RESEND_API_KEY")
        mail_to = os.environ.get("MAIL_TO")

        if not api_key or not mail_to:
            app.logger.error("Missing RESEND_API_KEY or MAIL_TO")
            return jsonify(ok=False, error="Email service is not configured."), 500

        payload = {
            "from": "Portfolio Contact <onboarding@resend.dev>",
            "to": [mail_to],
            "subject": f"Portfolio Contact from {name}",
            "reply_to": email,
            "text": f"""
        New message from your portfolio

        Name: {name}
        Email: {email}

        Message:
        {message}
        """
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "https://api.resend.com/emails",
                json=payload,
                headers=headers,
                timeout=15
            )

            if response.status_code not in (200, 201):
                app.logger.error("Resend Error: %s", response.text)
                return jsonify(
                    ok=False,
                    error="Email delivery failed."
                ), 502

        except Exception as exc:
            app.logger.exception(exc)
            return jsonify(
                ok=False,
                error="Unable to send email."
            ), 502

        return jsonify(ok=True)


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))