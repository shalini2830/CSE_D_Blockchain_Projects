# Decentralized Land Registry - Fast Duplicate Check Only

This version performs **only exact duplicate checks** using SHA-256 hashes of uploaded deeds.
This ensures submissions are **fast**, even with large files.

- Optional file upload (image/PDF).
- Exact duplicate detection with red warning in the UI.
- Blockchain structure remains the same.

Run:
1. pip install -r requirements.txt
2. python app.py
3. Open http://127.0.0.1:5000
