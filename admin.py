import os

from flask import (
    Blueprint, render_template, request, redirect, url_for, session, abort, current_app
)

from models import db, Profile
from admin_utils import (
    check_admin_password, login_required, get_csrf_token, validate_csrf,
    ENTITY_CONFIGS, populate_from_form, delete_upload,save_upload
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        validate_csrf()
        if check_admin_password(request.form.get("password", "")):
            session.clear()
            session["is_admin"] = True
            next_url = request.args.get("next") or url_for("admin.dashboard")
            return redirect(next_url)
        error = "Incorrect password."
    return render_template("admin/login.html", error=error, csrf_token=get_csrf_token())


@admin_bp.route("/logout", methods=["POST"])
def logout():
    validate_csrf()
    session.clear()
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    counts = {key: cfg["model"].query.count() for key, cfg in ENTITY_CONFIGS.items()}
    return render_template("admin/dashboard.html", counts=counts, entities=ENTITY_CONFIGS, csrf_token=get_csrf_token())


# ---------------------------------------------------------------------------
# Profile (singleton) editor
# ---------------------------------------------------------------------------

@admin_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    prof = db.session.get(Profile, 1)
    if not prof:
        prof = Profile(id=1)
        db.session.add(prof)
        db.session.commit()

    saved = False
    if request.method == "POST":
        validate_csrf()
        for field in [
            "name", "roles", "location", "email", "contact_number", "github", "linkedin",
            "resume_file", "summary",
            "stat1_label", "stat1_value", "stat2_label", "stat2_value",
            "stat3_label", "stat3_value", "stat4_label", "stat4_value",
        ]:
            setattr(prof, field, request.form.get(field, "").strip())

        # Handle resume upload
        file_storage = request.files.get("upload_resume")
        if file_storage and file_storage.filename:
            upload_folder = os.path.join(current_app.static_folder, "uploads", "resources")
            if prof.resume_file_path:
                delete_upload(current_app.static_folder, prof.resume_file_path)
            new_path = save_upload(file_storage, upload_folder)
            prof.resume_file_path = new_path
        # if no new file chosen, leave prof.resume_file_path untouched

        db.session.commit()
        saved = True

    return render_template("admin/profile.html", profile=prof, csrf_token=get_csrf_token(), saved=saved)# ---------------------------------------------------------------------------
# Generic CRUD for the rest of the content types
# ---------------------------------------------------------------------------

@admin_bp.route("/<entity>/")
@login_required
def list_entity(entity):
    config = ENTITY_CONFIGS.get(entity) or abort(404)
    records = config["model"].query.order_by(config["model"].sort_order.asc()).all()
    return render_template(
        "admin/list.html",
        entity=entity, config=config,
        records=[r.to_dict() for r in records],
        csrf_token=get_csrf_token(),
    )


@admin_bp.route("/<entity>/new", methods=["GET", "POST"])
@login_required
def new_entity(entity):
    config = ENTITY_CONFIGS.get(entity) or abort(404)

    if request.method == "POST":
        validate_csrf()
        instance = config["model"]()
        upload_folder = os.path.join(current_app.static_folder, "uploads", "resources")
        populate_from_form(instance, config, request.form, request.files, upload_folder, current_app.static_folder)
        db.session.add(instance)
        db.session.commit()
        return redirect(url_for("admin.list_entity", entity=entity))

    return render_template(
        "admin/form.html",
        entity=entity, config=config, record={}, is_new=True,
        csrf_token=get_csrf_token(),
    )


@admin_bp.route("/<entity>/<int:record_id>/edit", methods=["GET", "POST"])
@login_required
def edit_entity(entity, record_id):
    config = ENTITY_CONFIGS.get(entity) or abort(404)
    instance = config["model"].query.get_or_404(record_id)

    if request.method == "POST":
        validate_csrf()
        upload_folder = os.path.join(current_app.static_folder, "uploads", "resources")
        populate_from_form(instance, config, request.form, request.files, upload_folder, current_app.static_folder)
        db.session.commit()
        return redirect(url_for("admin.list_entity", entity=entity))

    return render_template(
        "admin/form.html",
        entity=entity, config=config, record=instance.to_dict(), is_new=False,
        csrf_token=get_csrf_token(),
    )


@admin_bp.route("/<entity>/<int:record_id>/delete", methods=["POST"])
@login_required
def delete_entity(entity, record_id):
    config = ENTITY_CONFIGS.get(entity) or abort(404)
    validate_csrf()
    instance = config["model"].query.get_or_404(record_id)

    file_path = getattr(instance, "file_path", None)
    if file_path:
        delete_upload(current_app.static_folder, file_path)

    db.session.delete(instance)
    db.session.commit()
    return redirect(url_for("admin.list_entity", entity=entity))
