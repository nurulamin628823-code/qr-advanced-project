# QR Document Verification System (Advanced) - ZIP Ready Project

This project implements an advanced RAJUK-style document verification system in **Python (Flask)**.
It includes:
- Admin dashboard (simple username/password)
- Create Document form (fills database, generates QR, embeds in PDF)
- Document list/history
- Verification public page (scan QR -> verify)
- SQLite database

## Quick start (local)
1. Extract the ZIP.
2. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows
   ```
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Initialize database:
   ```
   python create_db.py
   ```
5. Run the app:
   ```
   python app.py
   ```
6. Open the Admin area:
   - http://localhost:5000/admin
   - Default credentials (change in instance/config.json):
     username: admin
     password: admin123

7. Generate a document from Admin → Dashboard → Create Document.
   The PDF will be saved in static/pdf/ and include a QR that links to:
   `/verify?id=<doc_id>`

## Notes
- This is a simple demo project. Do **not** use default credentials in production.
- For production: use ENV variables, serve behind a proper webserver, use HTTPS.
