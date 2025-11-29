import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import json
from generate_pdf import generate_document

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data.db")

# Load instance config if exists
INSTANCE_CFG = os.path.join(BASE_DIR, "instance", "config.json")
if not os.path.exists(INSTANCE_CFG):
    # create default instance config
    with open(INSTANCE_CFG, 'w') as f:
        json.dump({"admin_user":"admin","admin_pass":"admin123"}, f)

with open(INSTANCE_CFG, 'r') as f:
    cfg = json.load(f)

app = Flask(__name__)
app.secret_key = 'change-me-for-production'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # public landing
    return render_template('index.html')

# ===== Public verify page =====
@app.route('/verify')
def verify():
    doc_id = request.args.get('id')
    if not doc_id:
        return render_template('verify.html', error='No id provided')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM documents WHERE doc_id=?', (doc_id,))
    data = cur.fetchone()
    conn.close()
    if not data:
        return render_template('verify.html', error='Invalid Document ID')
    # convert row to dict
    doc = dict(data)
    return render_template('verify_result.html', doc=doc)

# ===== Admin (very simple) =====
@app.route('/admin', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # check with instance config
        if username == cfg.get('admin_user') and password == cfg.get('admin_pass'):
            # set a simple session marker
            resp = redirect(url_for('admin_dashboard'))
            resp.set_cookie('admin_auth', '1')
            return resp
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.cookies.get('admin_auth') == '1':
            return func(*args, **kwargs)
        return redirect(url_for('admin_login'))
    return wrapper

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT doc_id, title, applicant, issue_date, status FROM documents ORDER BY issue_date DESC')
    rows = cur.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', docs=rows)

@app.route('/admin/create', methods=['GET','POST'])
@admin_required
def admin_create():
    if request.method == 'POST':
        title = request.form.get('title') or 'Untitled Document'
        applicant = request.form.get('applicant') or 'Unknown'
        status = request.form.get('status') or 'Approved'
        doc_id, pdf_path = generate_document(title, applicant, status)
        flash(f'Document created: {doc_id}', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_create.html')

@app.route('/static/pdf/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static', 'pdf'), filename)

if __name__ == '__main__':
    app.run(debug=True)
