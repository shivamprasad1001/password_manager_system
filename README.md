# 🔐 Password Manager System

A secure, locally-hosted password manager system built using **Python Flask**, with a responsive frontend using **HTML**, **CSS**, **JavaScript**, and **Bootstrap**. Passwords are stored securely in **MySQL** using hashed formats, and the system also maintains logs and backup files for recovery and auditing.

## 🚀 Features

- 🔑 Secure login and user registration system  
- 🧠 Passwords stored with hashing for enhanced security  
- 💾 Local backup of saved passwords  
- 📊 Dashboard showing total passwords, security score, and recent activity  
- ➕ Add new passwords  
- 👁️ View, copy, edit, and delete stored passwords  
- 🔍 Search through stored credentials  
- 🧪 Deletion verification with username & password  
- 🗂️ Logs user activity for traceability

---

## 🛠️ Tech Stack

| Tech / Tool         | Description                                  |
|---------------------|----------------------------------------------|
| ![Python](https://img.icons8.com/color/20/000000/python.png) Python | Backend programming language         |
| ![Flask](https://img.icons8.com/ios/20/000000/flask.png) Flask      | Web framework                        |
| ![HTML5](https://img.icons8.com/color/20/000000/html-5.png) HTML    | Markup language for UI               |
| ![CSS3](https://img.icons8.com/color/20/000000/css3.png) CSS        | Styling                              |
| ![JS](https://img.icons8.com/color/20/000000/javascript--v1.png) JS | Interactive frontend behavior        |
| ![MySQL](https://img.icons8.com/ios-filled/20/000000/mysql-logo.png) MySQL | Relational database management   |
| ![GitHub](https://img.icons8.com/ios-glyphs/20/000000/github.png) GitHub | Source control & versioning       |

---

## ⚙️ Project Workflow

```mermaid
graph TD
    A[User Visits Site] --> B{Is User Registered?}
    B -- Yes --> C[Login Page]
    B -- No --> D[Register New User]
    D --> E[System Generates Unique User ID]
    E --> C
    C --> F[Dashboard]

    F --> G[View Stored Passwords]
    F --> H[Add New Password]
    F --> I[Edit / Copy / Delete Password]

    I --> J{Delete Requested?}
    J --> K[Verify Username + Password]
    K --> L[Delete Password]

    H --> M[Hash & Save to MySQL]
    M --> N[Update Backup File]
    M --> O[Store Log]
````

---

## 📷 Screenshots

### 🔐 Dashboard View

![Dashboard Screenshot](assets/dashboard.png)

---

## 🧪 Installation & Run

### 🔧 Prerequisites

* Python 3.x
* MySQL
* Flask (`pip install flask`)
* Flask-MySQLdb (`pip install flask-mysqldb`)
* Other common modules: `os`, `hashlib`, `datetime`

### 🖥️ Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/password-manager-system.git
   cd password-manager-system
   ```

2. **Set Up the Database**

   * Create a MySQL database named `password_manager`
   * Import the `schema.sql` (if provided) or run:

     ```sql
     CREATE TABLE users (...);
     CREATE TABLE passwords (...);
     ```

3. **Configure `.env` or `config.py`**
   Add your MySQL DB credentials.

4. **Run the App**

   ```bash
   python app.py
   ```

5. Open `http://localhost:5000` in your browser.

---

## 🛡️ Security

* Passwords are hashed before being stored.
* Deletion requires re-authentication.
* Local backup ensures recovery in case of failure.
* Logs all sensitive operations for auditing.

---

---

## 👨‍💻 Author

**Shivam Prasad**
[GitHub](https://github.com/shivamprasad1001) • [LinkedIn](https://www.linkedin.com/in/shivamprasad1001/)

---

## 📜 License

This project is licensed under the MIT License.

