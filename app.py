
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session,
    send_from_directory
)

from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import os
import uuid


app = Flask(__name__)

app.secret_key = "waitless-print-secret-key"

# ---------------------------------
# UPLOAD SETTINGS
# ---------------------------------

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------
# HOME PAGE
# ---------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------
# STUDENT REGISTRATION
# ---------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not phone or not password:
            flash("Please fill all fields!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()

        try:
            conn.execute(
                """
                INSERT INTO students
                (name, email, phone, password)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, phone, hashed_password)
            )

            conn.commit()

            flash("Registration successful! Please login.")
            return redirect(url_for("login"))

        except Exception:
            conn.rollback()
            flash("Email already registered or registration failed!")

        finally:
            conn.close()

    return render_template("register.html")


# ---------------------------------
# STUDENT LOGIN
# ---------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db_connection()

        try:
            student = conn.execute(
                "SELECT * FROM students WHERE email = ?",
                (email,)
            ).fetchone()

        finally:
            conn.close()

        if student and check_password_hash(student["password"], password):

            session.clear()
            session["email"] = student["email"]

            flash("Login successful!")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password!")

    return render_template("login.html")


# ---------------------------------
# CHECK ALLOWED FILE
# ---------------------------------

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ---------------------------------
# STUDENT DASHBOARD
# ---------------------------------

@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        flash("Please login first!")
        return redirect(url_for("login"))

    conn = get_db_connection()

    try:
        documents = conn.execute(
            """
            SELECT *
            FROM documents
            WHERE student_email = ?
            ORDER BY upload_date DESC
            """,
            (session["email"],)
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "dashboard.html",
        documents=documents
    )


# ---------------------------------
# PDF UPLOAD
# ---------------------------------

@app.route("/upload", methods=["POST"])
def upload():

    if "email" not in session:
        flash("Please login first!")
        return redirect(url_for("login"))

    if "document" not in request.files:
        flash("Please select a PDF file!")
        return redirect(url_for("dashboard"))

    file = request.files["document"]

    if file.filename == "":
        flash("No file selected!")
        return redirect(url_for("dashboard"))

    if not allowed_file(file.filename):
        flash("Only PDF files are allowed!")
        return redirect(url_for("dashboard"))

    original_filename = secure_filename(file.filename)

    unique_filename = str(uuid.uuid4()) + "_" + original_filename

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    conn = get_db_connection()

    try:
        file.save(file_path)

        conn.execute(
            """
            INSERT INTO documents
            (student_email, filename)
            VALUES (?, ?)
            """,
            (session["email"], unique_filename)
        )

        conn.commit()

        flash("PDF uploaded successfully!")

    except Exception:
        conn.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        flash("Unable to upload PDF!")

    finally:
        conn.close()

    return redirect(url_for("dashboard"))


# ---------------------------------
# PDF DOWNLOAD
# ---------------------------------

@app.route("/download/<filename>")
def download(filename):

    if "email" not in session:
        flash("Please login first!")
        return redirect(url_for("login"))

    conn = get_db_connection()

    try:
        document = conn.execute(
            """
            SELECT *
            FROM documents
            WHERE filename = ?
            AND student_email = ?
            """,
            (filename, session["email"])
        ).fetchone()

    finally:
        conn.close()

    if document is None:
        flash("Document not found!")
        return redirect(url_for("dashboard"))

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


# ---------------------------------
# PDF DELETE
# ---------------------------------

@app.route("/delete/<filename>", methods=["POST"])
def delete_document(filename):

    if "email" not in session:
        flash("Please login first!")
        return redirect(url_for("login"))

    conn = get_db_connection()

    try:
        document = conn.execute(
            """
            SELECT *
            FROM documents
            WHERE filename = ?
            AND student_email = ?
            """,
            (filename, session["email"])
        ).fetchone()

        if document is None:
            flash("Document not found!")
            return redirect(url_for("dashboard"))

        # Do not delete a document linked to a print request
        linked_request = conn.execute(
            """
            SELECT id FROM print_requests
            WHERE document_id = ?
            LIMIT 1
            """,
            (document["id"],)
        ).fetchone()

        if linked_request:
            flash("This PDF has a print request and cannot be deleted!")
            return redirect(url_for("dashboard"))

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        conn.execute(
            "DELETE FROM documents WHERE id = ?",
            (document["id"],)
        )

        conn.commit()

        flash("Document deleted successfully!")

    except Exception:
        conn.rollback()
        flash("Unable to delete document!")

    finally:
        conn.close()

    return redirect(url_for("dashboard"))


# ---------------------------------
# CREATE PRINT REQUEST
# ---------------------------------

@app.route("/print_request", methods=["POST"])
def create_print_request():

    if "email" not in session:
        flash("Please login first!")
        return redirect(url_for("login"))

    try:
        document_id = int(request.form.get("document_id", ""))
        copies = int(request.form.get("copies", ""))

    except (ValueError, TypeError):
        flash("Invalid document or copies!")
        return redirect(url_for("dashboard"))

    print_type = request.form.get("print_type", "")
    paper_size = request.form.get("paper_size", "")

    if copies < 1 or copies > 100:
        flash("Copies must be between 1 and 100!")
        return redirect(url_for("dashboard"))

    if print_type not in ["Black & White", "Colour"]:
        flash("Invalid print type!")
        return redirect(url_for("dashboard"))

    if paper_size not in ["A4", "A3", "A5"]:
        flash("Invalid paper size!")
        return redirect(url_for("dashboard"))

    conn = get_db_connection()

    try:
        document = conn.execute(
            """
            SELECT id
            FROM documents
            WHERE id = ?
            AND student_email = ?
            """,
            (document_id, session["email"])
        ).fetchone()

        if document is None:
            flash("Please select a valid PDF!")
            return redirect(url_for("dashboard"))

        conn.execute(
            """
            INSERT INTO print_requests
            (student_email, document_id, copies, print_type, paper_size)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session["email"],
                document_id,
                copies,
                print_type,
                paper_size
            )
        )

        conn.commit()

        flash("Print request submitted successfully!")

    except Exception:
        conn.rollback()
        flash("Unable to submit print request!")

    finally:
        conn.close()

    return redirect(url_for("dashboard"))


# =================================
# ADMIN LOGIN
# =================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()

        try:
            admin = conn.execute(
                """
                SELECT *
                FROM admins
                WHERE username = ?
                """,
                (username,)
            ).fetchone()

        finally:
            conn.close()

        if admin and check_password_hash(admin["password"], password):

            session.clear()
            session["admin"] = admin["username"]

            flash("Admin login successful!")

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Admin Username or Password!")

    return render_template("admin_login.html")


# =================================
# ADMIN DASHBOARD
# =================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        flash("Please login as Admin first!")
        return redirect(url_for("admin_login"))

    conn = get_db_connection()

    try:
        requests_data = conn.execute(
            """
            SELECT
                print_requests.id,
                print_requests.student_email,
                students.name,
                documents.filename,
                print_requests.copies,
                print_requests.print_type,
                print_requests.paper_size,
                print_requests.status,
                print_requests.request_date

            FROM print_requests

            LEFT JOIN documents
            ON print_requests.document_id = documents.id

            LEFT JOIN students
            ON print_requests.student_email = students.email

            ORDER BY print_requests.request_date DESC
            """
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "admin_dashboard.html",
        requests_data=requests_data
    )


# =================================
# ADMIN UPDATE PRINT REQUEST STATUS
# =================================

@app.route(
    "/admin/update_status/<int:request_id>",
    methods=["POST"]
)
def update_print_status(request_id):

    if "admin" not in session:
        flash("Please login as Admin first!")
        return redirect(url_for("admin_login"))

    new_status = request.form.get("status", "")

    allowed_statuses = [
        "Pending",
        "Accepted",
        "Rejected",
        "Completed"
    ]

    if new_status not in allowed_statuses:
        flash("Invalid status!")
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()

    try:
        result = conn.execute(
            """
            UPDATE print_requests
            SET status = ?
            WHERE id = ?
            """,
            (new_status, request_id)
        )

        conn.commit()

        if result.rowcount == 0:
            flash("Print request not found!")
        else:
            flash("Print request status updated successfully!")

    except Exception:
        conn.rollback()
        flash("Unable to update status!")

    finally:
        conn.close()

    return redirect(url_for("admin_dashboard"))


# =================================
# ADMIN LOGOUT
# =================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    flash("Admin logged out successfully!")

    return redirect(url_for("admin_login"))


# =================================
# STUDENT LOGOUT
# =================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!")

    return redirect(url_for("home"))


# ---------------------------------
# FILE SIZE ERROR
# ---------------------------------

@app.errorhandler(413)
def file_too_large(error):

    flash("File is too large! Maximum size is 10 MB.")

    return redirect(url_for("dashboard"))


# ---------------------------------
# RUN APPLICATION
# ---------------------------------

if __name__ == "__main__":

    app.run(debug=True)
