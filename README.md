# Arshdeep Singh — Portfolio

A Flask + Tailwind portfolio with a terminal / neural-network visual theme,
backed by a SQLite database and a password-protected `/admin` panel — edit
every section of the site (profile, skills, projects, experience, education,
certifications, resources/documents) without touching code.

> **Just reviewed:** this codebase was audited end-to-end — every route,
> form, and database field was tested with an automated test suite
> (`tests/test_app.py`, 33 tests, all passing). Six real bugs were found and
> fixed; see [Bug fixes](#bug-fixes--changelog) below for exactly what
> changed and why.

## Structure

```
app.py                    Flask app factory, public routes, contact form
models.py                 SQLAlchemy models for every content type
admin.py                  Admin blueprint: login, dashboard, generic CRUD
admin_utils.py            Auth, CSRF, file upload helpers, entity field configs
seed_data.py              First-run seed (only runs if the DB is empty)
templates/index.html      Public single-page layout
templates/resource_detail.html   Public page for a single resource/document
templates/admin/          Login, dashboard, generic list/form, profile editor
static/css/style.css      Glow effects, reveals, admin panel styling
static/js/particles.js    Animated neural-network canvas background
static/js/main.js         Typewriter, scroll-reveal, mobile nav, resource filter, contact form
static/assets/            Your downloadable résumé PDF
static/uploads/resources/ Files you upload through /admin (certs, docs, videos)
instance/portfolio.db     SQLite database (created automatically on first run)
tests/test_app.py         Automated test suite (pytest) — see Testing below
requirements.txt          Flask, Flask-SQLAlchemy, gunicorn, python-dotenv
requirements-dev.txt      Adds pytest, for running the test suite
Procfile / render.yaml    Render deployment config
vercel.json                Vercel config — see the Vercel warning below
run_sql.py / lite.sql     Dev-only helper to run an ad-hoc query against instance/portfolio.db
```

## Editing content — via /admin, not code

Go to `/admin`, log in with your admin password, and you'll find a section
for each content type: Profile, Skill Groups, Projects, Experience,
Education, Certifications, Resources. Add, edit, or delete records from
there — the public site reflects changes immediately, no redeploy needed.

**Resources** is the documents/notes hub: each entry can be a PDF, PPT,
DOCX, video, typed note, or plain link. Upload a file and/or a preview
thumbnail, or paste a YouTube/Drive URL for videos. File size is filled in
automatically when you upload; duration is a manual field since extracting
it would need extra dependencies.

**Certifications** now also has a **Company / issuing organization** field
in the admin form (this was missing before — see changelog).

The very first time the app runs against an empty database, it seeds itself
from `seed_data.py` with your current résumé content, so the site isn't
blank before you've touched `/admin`. After that, `seed_data.py` is never
run again automatically — manage everything through the admin panel.

## Admin password

Set it via an environment variable — **do this before deploying**, the
default is intentionally weak:

```
ADMIN_PASSWORD=choose-a-real-password
```

Locally: put it in `.env` (already in `.gitignore`, never commit it) or
`export ADMIN_PASSWORD=whatever` before running `python3 app.py`. As of
this review, `app.py` actually loads `.env` via `python-dotenv` — it didn't
before (see changelog), so if you were relying on `.env` locally, that now
works correctly.

On Render/Vercel: add it under the service's Environment Variables.

Also set `SECRET_KEY` (any random string — used to sign the session
cookie and CSRF tokens) the same way:

```
SECRET_KEY=some-long-random-string
```

**Security note:** the `.env` file included in this project folder has a
real password and secret key in it. It's correctly listed in `.gitignore`
so it won't get committed, but since it now travels with the project
folder itself, treat it as sensitive — rotate `ADMIN_PASSWORD` and
`SECRET_KEY` to new values before you consider this production-ready.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
export ADMIN_PASSWORD=whatever-you-want   # or rely on .env, see above
python3 app.py
```

Visit `http://localhost:5000` for the site, `http://localhost:5000/admin`
for the panel.

## Testing

An automated test suite lives in `tests/test_app.py` (pytest) and covers:

- every public route (`/`, `/resources/<id>`, `/contact`)
- admin login, logout, and CSRF protection on every form
- full create → list → edit → delete cycle for **every** content type
  (skills, projects, experience, education, certifications, resources)
- the specific bugs listed below, so they can't silently come back

Run it with:

```bash
pip install -r requirements-dev.txt
pytest -v
```

It uses a throwaway `instance/test_portfolio.db`, never your real database,
and deletes every record and uploaded file it creates. All 33 tests pass
against the current code.

## ⚠️ Persistence — read this before deploying

You chose local-disk storage for the database and uploads, which is the
simplest option but comes with a real limitation: **most hosting
platforms' free tiers wipe the local filesystem on every redeploy or
restart** (this now affects your database too, not just uploaded files,
since all your content lives in `instance/portfolio.db`).

- **Render (recommended for this setup):** the filesystem persists while
  the service is *running*, but is wiped on redeploys and on the free
  tier's periodic restarts. For real persistence, add a
  [Render Disk](https://render.com/docs/disks) (small paid add-on) mounted
  at `/opt/render/project/src/instance` — then your database and uploads
  survive redeploys.
- **Vercel: not recommended for this version.** Vercel's Python functions
  run on a read-only filesystem (only `/tmp` is writable, and it doesn't
  persist between requests) — admin edits and file uploads would silently
  disappear. `vercel.json` is left in place in case you later split this
  into a static frontend + separate API, but don't deploy the admin panel
  there as-is.
- **Simple habit either way:** periodically download `instance/portfolio.db`
  and the contents of `static/uploads/` as a backup, especially before a
  redeploy, until you've set up persistent storage.
- **Later upgrade path:** point `DATABASE_URL` at a hosted Postgres
  instance (Render offers a free Postgres tier) instead of SQLite, and
  swap file uploads to Cloudinary or S3 — both keep content safe across
  redeploys with no code changes to the models beyond the connection
  string, though file uploads would need `admin_utils.save_upload` pointed
  at the new storage.

## Contact form email (optional)

The `/contact` route works out of the box — without configuration it just
logs submissions server-side so nothing is lost silently. To actually send
you an email, set these environment variables (Gmail example — use an
[app password](https://myaccount.google.com/apppasswords), not your real
password):

```
MAIL_USER=youraddress@gmail.com
MAIL_PASS=your-16-char-app-password
MAIL_TO=youraddress@gmail.com     # optional, defaults to MAIL_USER
```

## Deploy on Render

1. Push this folder to a GitHub repo.
2. On [render.com](https://render.com) → New → Web Service → connect the repo.
3. Render detects `render.yaml` automatically, or set manually:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Add environment variables: `ADMIN_PASSWORD`, `SECRET_KEY`, and
   optionally `MAIL_USER` / `MAIL_PASS` / `MAIL_TO`.
5. (Strongly recommended) Attach a Render Disk for persistence — see above.
6. Deploy — you'll get a `https://your-app.onrender.com` URL.

## Bug fixes & changelog

This codebase was fully audited: every route was hit with a test client,
every admin form was submitted end-to-end, and the database schema was
checked against what the templates and forms actually read/write. Six real
bugs were found (three of them user-facing) and fixed, plus a couple of
small hardening/cleanup changes.

| # | Bug | Impact | Fix |
|---|---|---|---|
| 1 | **Uploaded files served broken links** — `save_upload()` returned a path like `uploads/<file>`, but `admin.py` physically saves into `static/uploads/resources/<file>`. | Every certificate image and every resource file/preview you uploaded through `/admin` produced a 404 on the live site. Two orphaned files already existed on disk from a previous real upload attempt. | `UPLOAD_SUBDIR` now matches the real folder (`uploads/resources`), so the stored DB path always matches where the file actually lives. Covered by `TestFileUploads::test_upload_saved_path_matches_disk_location`. |
| 2 | **Certification company never displayed** — `Certification.to_dict()` returned the key `"Company"` (capital C) but `templates/index.html` reads `cert.company` (lowercase). | The issuing company/organization for both seeded certifications was silently blank on the homepage, even though it was correctly saved in the database. | `to_dict()` now returns `"company"`. Covered by `TestPublicRoutes::test_certification_company_renders`. |
| 3 | **No way to set a certification's company via the admin panel** — the `certifications` field list in `admin_utils.ENTITY_CONFIGS` never included a `company` field. | Admins could only set/change the issuing company by hand-editing the database or `seed_data.py` — the admin form had no input for it at all. | Added a "Company / issuing organization" text field to the certifications admin form. Covered by `TestCertificationCompanyField`. |
| 4 | **`.env` was silently ignored** — `python-dotenv` was listed in `requirements.txt` but `app.py` never called `load_dotenv()`. | Locally, `ADMIN_PASSWORD` / `SECRET_KEY` / `MAIL_*` values in `.env` had no effect; the app silently fell back to the default `changeme` password without any warning. | `app.py` now calls `load_dotenv()` on startup. Covered by `TestEnvironment::test_dotenv_values_are_loaded`. |
| 5 | **Admin password printed to server logs** — `check_admin_password()` had a leftover `print(expected)` debug line. | The real admin password was written to stdout/server logs on every single login attempt (successful or not) — a real exposure risk on any hosting platform that aggregates logs. | Removed the debug `print()`. |
| 6 | **Negative sort order silently discarded** — `populate_from_form()` used `raw.isdigit()` to validate number fields, and `str.isdigit()` returns `False` for negative numbers (e.g. `"-5"`). | Entering `-5` as a sort order (a reasonable way to pin an item to the front of a list) silently saved as `0` instead, with no error shown. | Number parsing now uses `int(raw)` in a `try/except`, so negative numbers are accepted and only genuinely invalid input falls back to `0`. Covered by `TestNumberFieldParsing`. |

**Smaller hardening/cleanup changes made at the same time:**
- Login (`/admin/login`) now validates the CSRF token on POST, same as every other form in the app (it previously rendered a token but never checked it).
- Fixed a typo in the seed data ("Unitfied Mentor" → "Unified Mentor").
- `run_sql.py` / `lite.sql`: fixed `lite.sql` (it opened with `use portfolio`, which is MySQL/T-SQL syntax and invalid in SQLite — this dev utility would fail immediately) and pointed `run_sql.py` at the actual database path (`instance/portfolio.db`) the app uses, instead of a relative `portfolio.db` in the current directory.
- Replaced the deprecated `Model.query.get(1)` calls with `db.session.get(Model, 1)` in `app.py` / `admin.py` — same behavior, but removes SQLAlchemy 2.0 deprecation warnings and avoids a future breaking change.

None of these required any database migration — the existing
`instance/portfolio.db` schema already had the `company` column (it was
just inaccessible from the UI); the fixes are all in application code.

## Notes

- Tailwind is loaded via CDN for zero build-step simplicity.
- Animations respect `prefers-reduced-motion`.
- The admin panel has no rate-limiting on login attempts beyond your
  password's strength — pick a real password, not `changeme`.
- Certification images and document previews/files uploaded through
  `/admin` are only as safe as your backup habits until persistent
  storage is set up (see the Persistence section above).
- Two unreferenced files from an earlier broken upload
  (`static/uploads/resources/d9ca39898c1f_Generative_AI_Modern_Excellence.pptx`
  and `...16e7ea06c7d1_how-to-build-a-gen-ai-solution-1.jpg`) are still on
  disk with no database record pointing at them — now that uploads work
  correctly, you can safely delete them or re-attach them to a Resource via
  `/admin` if you still want them.
#   a r s h d e e p - p o r t f o l i o  
 #   p y t h o n - a i - p o r t f o l i o  
 