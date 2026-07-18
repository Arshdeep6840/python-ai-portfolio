"""
Test suite for the Arshdeep portfolio Flask app.

Run with:
    pip install -r requirements-dev.txt
    pytest -v

Uses a throwaway SQLite DB (instance/test_portfolio.db) so it never touches
your real data, and cleans up every record + uploaded file it creates.
"""
import io
import os
import re
import sys

import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

TEST_DB_PATH = os.path.join(BASE_DIR, "instance", "test_portfolio.db")


@pytest.fixture(scope="module")
def client():
    os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
    os.environ["ADMIN_PASSWORD"] = "test-password-123"
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ.pop("MAIL_USER", None)  # force the "log, don't email" path for /contact

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    import app as appmod
    appmod.app.config.update(TESTING=True)

    with appmod.app.test_client() as c:
        yield c

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def _csrf_from(html):
    m = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert m, "no csrf_token found on page"
    return m.group(1)


@pytest.fixture(scope="module")
def admin_client(client):
    """Same client, but already logged in as admin."""
    csrf = _csrf_from(client.get("/admin/login").get_data(as_text=True))
    r = client.post("/admin/login", data={"password": "test-password-123", "csrf_token": csrf})
    assert r.status_code == 302
    return client


def csrf(client, path="/admin/profile"):
    return _csrf_from(client.get(path).get_data(as_text=True))


# ---------------------------------------------------------------------------
# Public site
# ---------------------------------------------------------------------------

class TestPublicRoutes:
    def test_homepage_loads(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert b"<html" in r.data

    def test_certification_company_renders(self, client):
        """Regression test: Certification.to_dict() used to return the key
        'Company' while the template read `cert.company`, so the issuer name
        silently never appeared on the page. Confirms the fix."""
        html = client.get("/").get_data(as_text=True)
        assert "Unified Mentor" in html
        assert "Cetpa Infotech" in html

    def test_resource_detail_found(self, client):
        r = client.get("/resources/1")
        assert r.status_code == 200

    def test_resource_detail_not_found(self, client):
        r = client.get("/resources/999999")
        assert r.status_code == 404


class TestContactForm:
    def test_missing_fields_rejected(self, client):
        r = client.post("/contact", json={"name": "", "email": "", "message": ""})
        assert r.status_code == 400
        assert r.get_json()["ok"] is False

    def test_valid_submission_accepted(self, client):
        r = client.post("/contact", json={
            "name": "Test User", "email": "test@example.com", "message": "Hello!",
        })
        assert r.status_code == 200
        assert r.get_json()["ok"] is True

    def test_accepts_form_encoded_too(self, client):
        r = client.post("/contact", data={
            "name": "Test User", "email": "test@example.com", "message": "Hello via form-encoding",
        })
        assert r.status_code == 200


# ---------------------------------------------------------------------------
# Admin auth + CSRF
# ---------------------------------------------------------------------------

class TestAdminAuth:
    def test_dashboard_requires_login(self, client):
        r = client.get("/admin/")
        assert r.status_code == 302
        assert "/admin/login" in r.headers["Location"]

    def test_wrong_password_rejected(self, client):
        token = csrf(client, "/admin/login")
        r = client.post("/admin/login", data={"password": "wrong", "csrf_token": token})
        assert r.status_code == 200
        assert "Incorrect" in r.get_data(as_text=True)

    def test_login_requires_csrf_token(self, client):
        r = client.post("/admin/login", data={"password": "test-password-123"})
        assert r.status_code == 400

    def test_correct_password_logs_in(self, admin_client):
        r = admin_client.get("/admin/")
        assert r.status_code == 200

    def test_forms_reject_missing_csrf(self, admin_client):
        r = admin_client.post("/admin/profile", data={"name": "Should Not Save"})
        assert r.status_code == 400

    def test_logout_then_dashboard_blocked_again(self, client):
        # use a short-lived second session so we don't disturb admin_client's login
        token = csrf(client, "/admin/login")
        client.post("/admin/login", data={"password": "test-password-123", "csrf_token": token})
        token = csrf(client)
        r = client.post("/admin/logout", data={"csrf_token": token})
        assert r.status_code == 302
        r = client.get("/admin/")
        assert r.status_code == 302
        # log back in for subsequent tests in this module
        token = csrf(client, "/admin/login")
        client.post("/admin/login", data={"password": "test-password-123", "csrf_token": token})


# ---------------------------------------------------------------------------
# Profile editor
# ---------------------------------------------------------------------------

class TestProfileEditor:
    def test_profile_save_roundtrips(self, admin_client):
        token = csrf(admin_client)
        r = admin_client.post("/admin/profile", data={
            "csrf_token": token, "name": "Arshdeep QA", "roles": "AI Dev, Backend Dev",
            "location": "Mohali", "email": "qa@example.com", "contact_number": "",
            "github": "", "linkedin": "", "resume_file": "", "summary": "QA summary",
            "stat1_label": "", "stat1_value": "", "stat2_label": "", "stat2_value": "",
            "stat3_label": "", "stat3_value": "", "stat4_label": "", "stat4_value": "",
        })
        assert r.status_code == 200
        assert "Arshdeep QA" in r.get_data(as_text=True)
        assert "QA summary" in admin_client.get("/").get_data(as_text=True)


# ---------------------------------------------------------------------------
# Generic CRUD — every entity type
# ---------------------------------------------------------------------------

ENTITY_PAYLOADS = {
    "skills": {"category": "Testing", "import_line": "import pytest", "tags": "pytest, unittest", "sort_order": "1"},
    "projects": {"name": "QA Project", "file": "qa.py", "period": "2026", "description": "desc",
                 "tech": "Python, Flask", "github": "https://github.com/x", "live": "", "sort_order": "1"},
    "experience": {"role": "QA Intern", "org": "TestCo", "period": "2026", "commit": "abc123",
                   "points": "Did a thing\nDid another thing", "sort_order": "1"},
    "education": {"degree": "MCA", "school": "QA University", "period": "2024-2026",
                   "detail": "CGPA 9.0", "link": "", "sort_order": "1"},
    "certifications": {"name": "QA Cert", "company": "QA Issuer Inc.", "sort_order": "1"},
    "resources": {"title": "QA Resource", "description": "desc", "category": "python",
                  "resource_type": "note", "content": "Some note content", "external_url": "", "sort_order": "1"},
}


@pytest.mark.parametrize("entity,payload", ENTITY_PAYLOADS.items())
class TestGenericCRUD:
    def test_new_form_loads(self, admin_client, entity, payload):
        r = admin_client.get(f"/admin/{entity}/new")
        assert r.status_code == 200

    def test_full_crud_cycle(self, admin_client, entity, payload):
        # CREATE
        token = csrf(admin_client)
        data = dict(payload, csrf_token=token)
        r = admin_client.post(f"/admin/{entity}/new", data=data, content_type="multipart/form-data")
        assert r.status_code == 302

        # LIST shows it
        r = admin_client.get(f"/admin/{entity}/")
        assert r.status_code == 200

        from admin_utils import ENTITY_CONFIGS
        with admin_client.application.app_context():
            model = ENTITY_CONFIGS[entity]["model"]
            rec = model.query.order_by(model.id.desc()).first()
            assert rec is not None
            rec_id = rec.id

        # EDIT form pre-fills
        r = admin_client.get(f"/admin/{entity}/{rec_id}/edit")
        assert r.status_code == 200

        # UPDATE
        token = csrf(admin_client)
        data = dict(payload, csrf_token=token)
        r = admin_client.post(f"/admin/{entity}/{rec_id}/edit", data=data, content_type="multipart/form-data")
        assert r.status_code == 302

        # DELETE
        token = csrf(admin_client)
        r = admin_client.post(f"/admin/{entity}/{rec_id}/delete", data={"csrf_token": token})
        assert r.status_code == 302

        with admin_client.application.app_context():
            assert model.query.get(rec_id) is None


class TestCertificationCompanyField:
    """Regression tests for the missing 'company' admin field bug."""

    def test_form_exposes_company_input(self, admin_client):
        html = admin_client.get("/admin/certifications/new").get_data(as_text=True)
        assert 'name="company"' in html

    def test_company_value_persists_and_prefills(self, admin_client):
        token = csrf(admin_client)
        r = admin_client.post("/admin/certifications/new", data={
            "csrf_token": token, "name": "Persist Test", "company": "Persist Co.", "sort_order": "0",
        }, content_type="multipart/form-data")
        assert r.status_code == 302

        from models import Certification
        with admin_client.application.app_context():
            rec = Certification.query.filter_by(name="Persist Test").first()
            assert rec.company == "Persist Co."
            rec_id = rec.id

        html = admin_client.get(f"/admin/certifications/{rec_id}/edit").get_data(as_text=True)
        assert 'value="Persist Co."' in html

        token = csrf(admin_client)
        admin_client.post(f"/admin/certifications/{rec_id}/delete", data={"csrf_token": token})


class TestNumberFieldParsing:
    """Regression test: negative sort_order used to be silently zeroed
    because str.isdigit() returns False for '-5'."""

    def test_negative_sort_order_preserved(self, admin_client):
        token = csrf(admin_client)
        admin_client.post("/admin/skills/new", data={
            "csrf_token": token, "category": "NegativeSortTest", "import_line": "", "tags": "",
            "sort_order": "-5",
        }, content_type="multipart/form-data")

        from models import SkillGroup
        with admin_client.application.app_context():
            rec = SkillGroup.query.filter_by(category="NegativeSortTest").first()
            assert rec is not None
            assert rec.sort_order == -5
            rec_id = rec.id

        token = csrf(admin_client)
        admin_client.post(f"/admin/skills/{rec_id}/delete", data={"csrf_token": token})

    def test_garbage_sort_order_defaults_to_zero(self, admin_client):
        token = csrf(admin_client)
        admin_client.post("/admin/skills/new", data={
            "csrf_token": token, "category": "GarbageSortTest", "import_line": "", "tags": "",
            "sort_order": "not-a-number",
        }, content_type="multipart/form-data")

        from models import SkillGroup
        with admin_client.application.app_context():
            rec = SkillGroup.query.filter_by(category="GarbageSortTest").first()
            assert rec is not None
            assert rec.sort_order == 0
            rec_id = rec.id

        token = csrf(admin_client)
        admin_client.post(f"/admin/skills/{rec_id}/delete", data={"csrf_token": token})


# ---------------------------------------------------------------------------
# File uploads
# ---------------------------------------------------------------------------

class TestFileUploads:
    def test_disallowed_extension_rejected(self, admin_client):
        token = csrf(admin_client)
        bad_file = (io.BytesIO(b"malicious"), "virus.exe")
        r = admin_client.post("/admin/resources/new", data={
            "csrf_token": token, "title": "BadFile", "description": "", "category": "",
            "resource_type": "note", "content": "", "external_url": "", "duration_label": "",
            "sort_order": "0", "file_path": bad_file,
        }, content_type="multipart/form-data")
        assert r.status_code == 400

    def test_upload_saved_path_matches_disk_location(self, admin_client):
        """Regression test: save_upload() used to return 'uploads/<file>' while
        admin.py physically saved into 'uploads/resources/<file>' — every
        uploaded file/image link on the live site was broken. Confirms the fix."""
        token = csrf(admin_client)
        good_file = (io.BytesIO(b"%PDF-1.4 fake pdf content"), "qa_resume.pdf")
        r = admin_client.post("/admin/resources/new", data={
            "csrf_token": token, "title": "QA PDF Resource", "description": "", "category": "",
            "resource_type": "pdf", "content": "", "external_url": "", "duration_label": "",
            "sort_order": "0", "file_path": good_file,
        }, content_type="multipart/form-data")
        assert r.status_code == 302

        from models import Resource
        with admin_client.application.app_context():
            rec = Resource.query.filter_by(title="QA PDF Resource").first()
            assert rec.file_path.startswith("uploads/resources/")
            assert rec.size_label  # auto-filled, proves the path resolved correctly
            rec_id = rec.id

        static_folder = admin_client.application.static_folder
        full_path = os.path.join(static_folder, rec.file_path)
        assert os.path.isfile(full_path)

        # the public detail page must actually serve the file (no 404)
        html = admin_client.get(f"/resources/{rec_id}").get_data(as_text=True)
        m = re.search(r'src="(/static/uploads/resources/[^"]+)"', html)
        assert m, "uploaded PDF iframe src not found on detail page"
        assert admin_client.get(m.group(1)).status_code == 200

        # DELETE must remove the physical file too
        token = csrf(admin_client)
        admin_client.post(f"/admin/resources/{rec_id}/delete", data={"csrf_token": token})
        assert not os.path.isfile(full_path)


# ---------------------------------------------------------------------------
# Config / environment
# ---------------------------------------------------------------------------

class TestEnvironment:
    def test_dotenv_values_are_loaded(self):
        """Regression test: python-dotenv is listed in requirements.txt but
        app.py never called load_dotenv(), so a real .env file's
        ADMIN_PASSWORD/SECRET_KEY were silently ignored. Confirms the fix
        by checking app.py actually calls load_dotenv()."""
        app_source = open(os.path.join(BASE_DIR, "app.py")).read()
        assert "load_dotenv" in app_source
