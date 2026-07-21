import os
import smtplib
import requests
from email.mime.text import MIMEText

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate

from models import db, Profile, SkillGroup, Project, Experience, Education, Certification, Resource

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'portfolio.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 60 * 1024 * 1024  # 60MB upload cap

    os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
    db.init_app(app)
    migrate = Migrate(app, db)

    from admin import admin_bp
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        _seed_if_empty()

    register_routes(app)
    return app


def _seed_if_empty():
    """First-run convenience: if the DB is empty, seed it from seed_data.py
    so the site isn't blank before you've touched the admin panel."""
    if db.session.get(Profile, 1):
        return
    from seed_data import run_seed
    run_seed()


def register_routes(app):
    @app.route("/")
    def index():
        profile = db.session.get(Profile, 1)
        skills = SkillGroup.query.order_by(SkillGroup.sort_order.asc()).all()
        projects = Project.query.order_by(Project.sort_order.asc()).all()
        experience = Experience.query.order_by(Experience.sort_order.asc()).all()
        education = Education.query.order_by(Education.sort_order.asc()).all()
        certifications = Certification.query.order_by(Certification.sort_order.asc()).all()
        resources = Resource.query.order_by(Resource.sort_order.asc()).all()

        categories = sorted({r.category for r in resources if r.category})
        type_order = ["pdf", "ppt", "docx", "video", "note", "link"]
        present_types = {r.resource_type for r in resources}
        resource_types = [t for t in type_order if t in present_types]

        return render_template(
            "index.html",
            profile=profile.to_dict() if profile else {},
            skills=[s.to_dict() for s in skills],
            projects=[p.to_dict() for p in projects],
            experience=[e.to_dict() for e in experience],
            education=[e.to_dict() for e in education],
            certifications=[c.to_dict() for c in certifications],
            resources=[r.to_dict() for r in resources],
            resource_categories=categories,
            resource_types=resource_types,
        )

    @app.route("/resources/<int:resource_id>")
    def resource_detail(resource_id):
        resource = Resource.query.get_or_404(resource_id)
        profile = db.session.get(Profile, 1)
        return render_template(
            "resource_detail.html",
            r=resource.to_dict(),
            profile=profile.to_dict() if profile else {},
        )

    # @app.route("/contact", methods=["POST"])
    # def contact():
    #     """Handle the contact form. Sends an email if SMTP env vars are set,
    #     otherwise logs the message server-side so nothing is silently lost."""
    #     data = request.get_json(silent=True) or request.form
    #     name = (data.get("name") or "").strip()
    #     email = (data.get("email") or "").strip()
    #     message = (data.get("message") or "").strip()

    #     if not name or not email or not message:
    #         return jsonify(ok=False, error="All fields are required."), 400

    #     mail_user = os.environ.get("MAIL_USER")
    #     mail_pass = os.environ.get("MAIL_PASS")
    #     mail_to = os.environ.get("MAIL_TO", mail_user)

    #     if mail_user and mail_pass and mail_to:
    #         try:
    #             body = f"From: {name} <{email}>\n\n{message}"
    #             msg = MIMEText(body)
    #             msg["Subject"] = f"Portfolio contact from {name}"
    #             msg["From"] = mail_user
    #             msg["To"] = mail_to
    #             msg["Reply-To"] = email

    #             with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
    #                 server.ehlo()
    #                 server.starttls()
    #                 server.ehlo()
    #                 server.login(mail_user, mail_pass)
    #                 server.sendmail(mail_user, [mail_to], msg.as_string())
    #         except Exception as exc:  # pragma: no cover - best-effort delivery
    #             app.logger.error("Failed to send contact email: %s", exc)
    #             return jsonify(ok=False, error="Message received but email delivery failed."), 502
    #     else:
    #         app.logger.info("Contact form (no SMTP configured): %s <%s> — %s", name, email, message)

    #     return jsonify(ok=True)
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