
<div align="center">

# 🔐 Password Manager System  
**Secure, Local, and Simple Password Storage**

A local password manager built with Python Flask that securely hashes your credentials, backs them up, and gives you full control via a modern web dashboard.

<img src="assets/logo.png" alt="App Logo" width="200" />

</div>

---

<p align="center">
  <!-- Language & Framework -->
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Werkzeug-Security-308446?style=for-the-badge&logo=werkzeug&logoColor=white" />

  <!-- Database -->
  <img src="https://img.shields.io/badge/MySQL-Connector-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask--MySQLDB-ORM-orange?style=for-the-badge" />

  <!-- Security & Encryption -->
  <img src="https://img.shields.io/badge/SHA256-Password%20Hashing-green?style=for-the-badge&logo=gnupg&logoColor=white" />
  <img src="https://img.shields.io/badge/AES-Encryption-yellow?style=for-the-badge&logo=virustotal&logoColor=black" />
  <img src="https://img.shields.io/badge/Base64-Encoding-grey?style=for-the-badge" />

  <!-- Frontend -->
  <img src="https://img.shields.io/badge/HTML-5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS-3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-Client%20Logic-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap&logoColor=white" />

  <!-- Libraries -->
  <img src="https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Datetime-TimeOps-grey?style=for-the-badge&logo=clockify&logoColor=white" />
  <img src="https://img.shields.io/badge/OS-FileOps-333333?style=for-the-badge&logo=powerbi&logoColor=white" />
  <img src="https://img.shields.io/badge/Logging-Rotation%20Handler-blue?style=for-the-badge&logo=logstash&logoColor=white" />

  <!-- Environment -->
  <img src="https://img.shields.io/badge/Localhost-Development-lightgrey?style=for-the-badge&logo=apache&logoColor=black" />
  <img src="https://img.shields.io/badge/Markdown-Documentation-000000?style=for-the-badge&logo=markdown&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-Repo-181717?style=for-the-badge&logo=github&logoColor=white" />
</p>


---

## 📜 Overview

The **Password Manager System** is a secure, locally-hosted web app that lets users register, log in, and manage their credentials in one place. Passwords are **hashed**, not stored in plain text, and users can **add**, **edit**, **delete**, and **copy** them from a beautiful dashboard. All actions are logged, and a JSON **backup** is automatically created for added reliability.

---

## 🌟 Features

- 🔐 **User Registration & Login**  
- 🧠 **Unique User ID System**
- 🧾 **Hashed Password Storage (SHA256)**
- 💾 **Automatic Backup File (JSON)**
- 🛡️ **Secure Deletion with Re-Authentication**
- 📊 **Password Count, Audit Log, and Dashboard**
- ✂️ **Copy, Edit, and Delete Stored Passwords**

---

## 📂 Project Flow

```mermaid
graph TD
    A[Visit App] --> B{Is User Registered?}
    B -- Yes --> C[Login]
    B -- No --> D[Register]
    D --> E[Generate Unique User ID]
    C --> F[Fetch User ID from MySQL]
    F --> G[Display Dashboard]

    G --> H[View Passwords]
    G --> I[Add New Password]
    G --> J[Edit/Copy/Delete]

    I --> K[Hash + Store in DB]
    K --> L[Update Xlsx Backup & Logs]

    J --> M{User Verified?}
    M -- Yes --> N[Delete/Edit Action]
    N --> L
````

---

## 🧰 Tech Stack

| Layer            | Tech/Tool                                                                                                                                                                                                                                                 |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend          | ![Python](https://img.icons8.com/color/25/python.png) Python, ![Flask](https://img.icons8.com/ios/25/flask.png) Flask                                                                                                                                     |
| Frontend         | ![HTML5](https://img.icons8.com/color/25/html-5.png) HTML, ![CSS3](https://img.icons8.com/color/25/css3.png) CSS, ![JavaScript](https://img.icons8.com/color/25/javascript.png) JS, ![Bootstrap](https://img.icons8.com/color/25/bootstrap.png) Bootstrap |
| Database         | ![MySQL](https://img.icons8.com/ios-filled/25/mysql-logo.png) MySQL                                                                                                                                                                                       |
| Logging & Backup | Local `logs/`, `backup/passwords.json`                                                                                                                                                                                                                    |

---

## 📸 Dashboard Preview

<p align="center">
  <img src="assets/dashboard.png" alt="Dashboard Screenshot" width="100%" />
</p>

---

## 📁 File Structure

```
password-manager-system/
│
├── static/                 # CSS, JS files
├── templates/              # Flask HTML templates
├── password_backup.xlsx    # Auto-generated xlsx backups
├── password_manager.log    # Logs of user activity
├── app.py                  # Main Flask app
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🧪 How to Run Locally

### ✅ Prerequisites

* Python 3.8+
* MySQL Server
* pip (`pip install -r requirements.txt`)

### ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/password-manager-system.git
cd password-manager-system

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

# 🔧 Configure Database

1. ### Open MySQL
2. ### Create database:

   ```sql
   CREATE DATABASE password_manager;
   ```
3. #### 🔐 `users` Table

```sql
CREATE TABLE users (
  id CHAR(36) NOT NULL PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

| Field           | Type           | Key         | Description            |
| --------------- | -------------- | ----------- | ---------------------- |
| `id`            | `char(36)`     | Primary Key | UUID for each user     |
| `username`      | `varchar(255)` | Unique      | Unique username        |
| `password_hash` | `varchar(255)` |             | SHA256 hashed password |
| `created_at`    | `timestamp`    |             | Account creation time  |

---

4. #### 🔑 `passwords` Table

```sql
CREATE TABLE passwords (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  salt VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id CHAR(36),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

| Field           | Type           | Key         | Description                                 |
| --------------- | -------------- | ----------- | ------------------------------------------- |
| `id`            | `int`          | Primary Key | Auto-incremented ID for each password entry |
| `salt`          | `varchar(255)` |             | Salt used in AES encryption                 |
| `username`      | `varchar(255)` |             | Username of the app/site account            |
| `password_hash` | `text`         |             | Encrypted (hashed + AES) password           |
| `created_at`    | `timestamp`    |             | Entry creation time                         |
| `user_id`       | `char(36)`     | Foreign Key | Links to the `users` table via `users.id`   |

---

### 🔄 Relationships

```text
users.id (char[36])  ←──  passwords.user_id (char[36])
[1 User] → [Many Passwords]
```



### 🚀 Run the App

```bash
python app.py
```

Visit: `http://localhost:5000`

---

## 🔐 Security Notes

* All passwords are **SHA256 hashed**
* User authentication required for all operations
* **Deletion is double-verified**
* Regular **logs and JSON backups** maintained locally

---

## 🚀 Future Roadmap

* [ ] 🔑 Export encrypted vault
* [ ] 📲 Mobile-friendly UI
* [ ] 🔒 Add 2FA/MFA login option
* [ ] 📊 Insights: weak vs strong password detection

---

## 👨‍💻 Author

Made with 🖤 by [**Shivam Prasad**](https://github.com/shivamprasad1001)
🔗 Connect: [LinkedIn](https://www.linkedin.com/in/shivamprasad1001)

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

> ⭐ Star the repo if you like it. Pull requests and feedback welcome!
