from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def split_csv(value):
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def split_lines(value):
    return [v.strip() for v in (value or "").splitlines() if v.strip()]


class Profile(db.Model):
    """Singleton row (id=1) holding the hero/about content."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default="")
    roles = db.Column(db.Text, default="")  # comma-separated
    location = db.Column(db.String(160), default="")
    email = db.Column(db.String(160), default="")
    contact_number = db.Column(db.String(40), default="")
    github = db.Column(db.String(255), default="")
    linkedin = db.Column(db.String(255), default="")
    resume_file = db.Column(db.String(255), default="")
    summary = db.Column(db.Text, default="")

    stat1_label = db.Column(db.String(80), default="")
    stat1_value = db.Column(db.String(20), default="")
    stat2_label = db.Column(db.String(80), default="")
    stat2_value = db.Column(db.String(20), default="")
    stat3_label = db.Column(db.String(80), default="")
    stat3_value = db.Column(db.String(20), default="")
    stat4_label = db.Column(db.String(80), default="")
    stat4_value = db.Column(db.String(20), default="")

    def to_dict(self):
        return {
            "name": self.name,
            "roles": split_csv(self.roles),
            "location": self.location,
            "email": self.email,
            "contact_number": self.contact_number,
            "github": self.github,
            "linkedin": self.linkedin,
            "resume_file": self.resume_file,
            "summary": self.summary,
            "stats": [
                {"label": self.stat1_label, "value": self.stat1_value},
                {"label": self.stat2_label, "value": self.stat2_value},
                {"label": self.stat3_label, "value": self.stat3_value},
                {"label": self.stat4_label, "value": self.stat4_value},
            ],
        }


class SkillGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120), default="")
    import_line = db.Column(db.String(255), default="")
    tags = db.Column(db.Text, default="")  # comma-separated
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "import_line": self.import_line,
            "tags": split_csv(self.tags),
            "sort_order": self.sort_order,
        }


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), default="")
    file = db.Column(db.String(160), default="")
    period = db.Column(db.String(80), default="")
    description = db.Column(db.Text, default="")
    tech = db.Column(db.Text, default="")  # comma-separated
    github = db.Column(db.String(255), default="")
    live = db.Column(db.String(255), default="")
    highlight = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "file": self.file,
            "period": self.period,
            "description": self.description,
            "tech": split_csv(self.tech),
            "github": self.github,
            "live": self.live,
            "highlight": self.highlight,
            "sort_order": self.sort_order,
        }


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(160), default="")
    org = db.Column(db.String(160), default="")
    period = db.Column(db.String(80), default="")
    commit = db.Column(db.String(40), default="")
    points = db.Column(db.Text, default="")  # newline-separated
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "org": self.org,
            "period": self.period,
            "commit": self.commit,
            "points": split_lines(self.points),
            "sort_order": self.sort_order,
        }


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(200), default="")
    school = db.Column(db.String(200), default="")
    period = db.Column(db.String(80), default="")
    detail = db.Column(db.String(160), default="")
    link = db.Column(db.String(255), default="")
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "degree": self.degree,
            "school": self.school,
            "period": self.period,
            "detail": self.detail,
            "link": self.link,
            "sort_order": self.sort_order,
        }


class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), default="")  # title
    company = db.Column(db.String(255), default="")  # issuing company/organization
    image = db.Column(db.String(255), default="")  # relative to static/
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "image": self.image,
            "sort_order": self.sort_order,
        }


RESOURCE_TYPES = ["pdf", "ppt", "docx", "video", "note", "link"]


class Resource(db.Model):
    """A document/resource: a PDF, slide deck, Word doc, video, typed note,
    or plain link. Shown in the public Resources section and linked from
    project/profile pages."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default="")
    description = db.Column(db.Text, default="")
    category = db.Column(db.String(120), default="")
    resource_type = db.Column(db.String(20), default="note")
    content = db.Column(db.Text, default="")  # for typed notes
    file_path = db.Column(db.String(255), default="")  # relative to static/
    preview_image = db.Column(db.String(255), default="")  # relative to static/
    external_url = db.Column(db.String(500), default="")  # YouTube/Drive/link
    size_label = db.Column(db.String(40), default="")  # auto-filled on upload
    duration_label = db.Column(db.String(40), default="")  # for videos
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "resource_type": self.resource_type,
            "content": self.content,
            "file_path": self.file_path,
            "preview_image": self.preview_image,
            "external_url": self.external_url,
            "size_label": self.size_label,
            "duration_label": self.duration_label,
            "sort_order": self.sort_order,
            "created_at": self.created_at,
        }
