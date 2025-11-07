# Blockchain Attendance System (SQLite) — Improved UI & Messages

## 👥 Team Members
- Name: SHAMSU NISHA N 
- RRN: 220071601235
- NAME: SHARMILA D
- RRN: 220071601236
- NAME: THARANI V S
- RRN:220071601265

---

## 📝 Problem Statement
Traditional attendance systems in educational institutions are prone to manipulation, errors, and require manual work. There is no tamper-proof way to ensure that attendance is recorded accurately and securely.

---

## 💡 Solution
This project implements a **Blockchain-based Attendance System** that ensures:  
- **Security & Integrity:** Attendance data is recorded as blockchain transactions, making it immutable.  
- **Duplicate Prevention:** Students cannot mark attendance more than once per day.  
- **User-Friendly Interface:** A clean web interface with flash messages for feedback.  
- **Persistence:** Attendance data is stored locally in SQLite for easy retrieval and management.

---

## ⚙️ Implementation Details
- **Backend:** Python Flask framework to handle requests and logic.  
- **Database:** SQLite to store student details and attendance records.  
- **Blockchain:** Minimal blockchain to store attendance transactions securely. Each block contains student info, timestamp, and hash of the previous block.  
- **Frontend:** Bootstrap-based UI for a clean and responsive dashboard, registration form, attendance marking, and blockchain viewing.  
- **Flash Messages:** Display success messages for attendance marked and warnings for duplicate attendance attempts.  
- **Duplicate Check:** The system checks the current date and prevents multiple attendance entries for the same student on the same day.  

---

## 🚀 How to Run
1. **Install Dependencies**  
```bash
pip install -r requirements.txt


How to run:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open http://127.0.0.1:5000
