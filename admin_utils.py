import os
import secrets
from functools import wraps

from flask import session, request, abort
from werkzeug.utils import secure_filename

from models import Project, SkillGroup, Experience, Education, Certification, Resource

ALLOWED_EXTENSIONS = {
    "pdf", "ppt", "pptx", "doc", "docx", "txt", "md",
    "mp4", "webm", "mov",
    "png", "jpg", "jpeg", "gif", "svg",
}

UPLOAD_SUBDIR = "uploads/resources"


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def check_admin_password(password):
    expected = os.environ.get("ADMIN_PASSWORD", "changeme")
    return secrets.compare_digest(password or "", expected)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            from flask import redirect, url_for
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


# ---------------------------------------------------------------------------
# CSRF (lightweight, session-token based — adequate for a single-admin panel)
# ---------------------------------------------------------------------------

def get_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


def validate_csrf():
    token = request.form.get("csrf_token", "")
    if not token or not secrets.compare_digest(token, session.get("csrf_token", "")):
        abort(400, description="Invalid or missing CSRF token. Go back and try again.")


# ---------------------------------------------------------------------------
# File uploads
# ---------------------------------------------------------------------------

def human_readable_size(num_bytes):
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file_storage, upload_folder):
    """Saves an uploaded file with a collision-proof name.
    Returns the path relative to /static (for use with url_for('static', filename=...))."""
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_file(file_storage.filename):
        abort(400, description="That file type isn't allowed.")
    safe_name = secure_filename(file_storage.filename)
    unique_name = f"{secrets.token_hex(6)}_{safe_name}"
    os.makedirs(upload_folder, exist_ok=True)
    file_storage.save(os.path.join(upload_folder, unique_name))
    return f"{UPLOAD_SUBDIR}/{unique_name}"


def delete_upload(static_folder, relative_path):
    if not relative_path:
        return
    full_path = os.path.join(static_folder, relative_path)
    if os.path.isfile(full_path):
        try:
            os.remove(full_path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Generic entity configs — drives the reusable admin list/form templates
# ---------------------------------------------------------------------------

ENTITY_CONFIGS = {
    "skills": {
        "model": SkillGroup,
        "label": "Skill Groups",
        "list_columns": ["category", "sort_order"],
        "fields": [
            {"name": "category", "label": "Category", "type": "text", "required": True},
            {"name": "import_line", "label": "Import line (e.g. from ml import ...)", "type": "text"},
            {"name": "tags", "label": "Tags (comma-separated)", "type": "textarea"},
            {"name": "sort_order", "label": "Sort order", "type": "number"},
        ],
    },
    "projects": {
        "model": Project,
        "label": "Projects",
        "list_columns": ["name", "period", "sort_order"],
        "fields": [
            {"name": "name", "label": "Name", "type": "text", "required": True},
            {"name": "file", "label": "File label (e.g. project.py)", "type": "text"},
            {"name": "period", "label": "Period", "type": "text"},
            {"name": "description", "label": "Description", "type": "textarea"},
            {"name": "tech", "label": "Tech stack (comma-separated)", "type": "textarea"},
            {"name": "github", "label": "GitHub URL", "type": "text"},
            {"name": "live", "label": "Live URL", "type": "text"},
            {"name": "highlight", "label": "Highlight (full-width card)", "type": "checkbox"},
            {"name": "sort_order", "label": "Sort order", "type": "number"},
        ],
    },
    "experience": {
        "model": Experience,
        "label": "Experience",
        "list_columns": ["role", "org", "sort_order"],
        "fields": [
            {"name": "role", "label": "Role", "type": "text", "required": True},
            {"name": "org", "label": "Organization", "type": "text"},
            {"name": "period", "label": "Period", "type": "text"},
            {"name": "commit", "label": "Commit hash label (cosmetic)", "type": "text"},
            {"name": "points", "label": "Bullet points (one per line)", "type": "textarea"},
            {"name": "sort_order", "label": "Sort order", "type": "number"},
        ],
    },
    "education": {
        "model": Education,
        "label": "Education",
        "list_columns": ["degree", "school", "sort_order"],
        "fields": [
            {"name": "degree", "label": "Degree", "type": "text", "required": True},
            {"name": "school", "label": "School", "type": "text"},
            {"name": "period", "label": "Period", "type": "text"},
            {"name": "detail", "label": "Detail (e.g. CGPA: 8.7)", "type": "text"},
            {"name": "link", "label": "School / course link (optional)", "type": "text"},
            {"name": "sort_order", "label": "Sort order", "type": "number"},
        ],
    },
    "certifications": {
        "model": Certification,
        "label": "Certifications",
        "list_columns": ["name", "sort_order"],
        "fields": [
            {"name": "name", "label": "Title", "type": "text", "required": True},
            {"name": "company", "label": "Issuing company / organization", "type": "text"},
            {"name": "image", "label": "Certificate image", "type": "file"},
            {"name": "sort_order", "label": "Sort order", "type": "number"},
        ],
    },
    "resources": {
        "model": Resource,
        "label": "Resources / Documents",
        "list_columns": ["title", "resource_type", "size_label", "sort_order"],
        "fields": [
            {"name": "title", "label": "Title", "type": "text", "required": True},
            {"name": "description", "label": "Short description", "type": "textarea"},
            {"name": "category", "label": "Category / tech tag (optional)", "type": "text"},
            {"name": "resource_type", "label": "Type", "type": "select",
             "choices": ["pdf", "ppt", "docx", "video", "note", "link"]},
            {"name": "content", "label": "Note content (for type=note)", "type": "textarea"},
            {"name": "external_url", "label": "External URL (YouTube / Drive / link)", "type": "text"},
            {"name": "file_path", "label": "Upload file (pdf / ppt / docx / video)", "type": "file"},
            {"name": "preview_image", "label": "Preview thumbnail image", "type": "file"},
            {"name": "duration_label", "label": "Duration (for videos, e.g. \"4 min 12 sec\")", "type": "text"},
            {"name": "sort_order", "label": "Sort order", "type": "number"},
        ],
    },
}


def populate_from_form(instance, config, form, files, upload_folder, static_folder):
    for field in config["fields"]:
        ftype = field["type"]
        name = field["name"]

        if ftype == "checkbox":
            setattr(instance, name, name in form)
        elif ftype == "number":
            raw = form.get(name, "").strip()
            try:
                setattr(instance, name, int(raw))
            except (TypeError, ValueError):
                setattr(instance, name, 0)
        elif ftype == "file":
            file_storage = files.get(name)
            if file_storage and file_storage.filename:
                old_value = getattr(instance, name, None)
                if old_value:
                    delete_upload(static_folder, old_value)
                new_path = save_upload(file_storage, upload_folder)
                setattr(instance, name, new_path)
                # auto-fill human-readable size for the main resource file
                if name == "file_path" and hasattr(instance, "size_label"):
                    try:
                        full_path = os.path.join(static_folder, new_path)
                        instance.size_label = human_readable_size(os.path.getsize(full_path))
                    except OSError:
                        pass
            # if no new file chosen, leave the existing value untouched
        else:
            setattr(instance, name, form.get(name, "").strip())
