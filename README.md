# 🔐 Password Manager  
A simple and secure **Password Manager** built with **Flask** and **HTML/CSS/JavaScript**. It allows users to store, retrieve, and manage passwords for different websites/apps securely.  
<p align="center">
  <img src="https://github.com/shivamprasad1001/password_manager_system/blob/main/static/demo/login.png?raw=true" width="30%" />
  <img src="https://github.com/shivamprasad1001/password_manager_system/blob/main/static/demo/index.png?raw=true" width="30%" />
  <img src="https://github.com/shivamprasad1001/password_manager_system/blob/main/static/demo/register.png?raw=true" width="30%" />
</p>
---

## 🚀 Features  
✅ **Offline Mode** – Works without an internet connection.  
✅ **Store & Retrieve Passwords** – Securely save credentials for different accounts.  
✅ **Admin Authentication** – Protect sensitive actions (edit/delete) with authentication.  
✅ **Copy to Clipboard** – Easily copy usernames & passwords with a single click.  
✅ **Responsive Design** – Works on both desktop & mobile.  

---

## 🛠️ Technologies Used  
- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite (Can be extended to MySQL/PostgreSQL)  

---

## 🎮 Installation & Setup  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/shivamprasad1001/password_manager_system
cd password_manager_system
```
2️⃣ Create a Virtual Environment
```sh
python -m venv venv

```
```sh
venv\Scripts\activate

```
3️⃣ Install Dependencies
```sh
pip install -r requirements.txt

```
4️⃣ Configure MySQL (If using MySQL instead of SQLite)
⚠️ Warning: Before running the app, update the MySQL username & password in app.py (Line 14).
Modify this section:
```sh

app.config['MYSQL_USER'] = "your_mysql_username",  # CHANGE THIS
app.config['MYSQL_PASSWORD'] = "your_mysql_password",  # CHANGE THIS

```
5️⃣ Run the Flask App

```sh
python app.py

```
6️⃣ Open in Browser

```sh
http://127.0.0.1:5000
```
# 🔐 Usage
1️⃣ Add New Password – Enter website/app name, username, and password.   
2️⃣ Copy Passwords – Click 📋 "Copy" to quickly copy credentials.   
3️⃣ Edit or Delete – Requires admin authentication for modifications.   

# ⚡ Security Considerations
🔹 Use environment variables instead of storing raw passwords.   
🔹 Implement encryption (e.g., bcrypt) before saving passwords.    
🔹 Enable HTTPS if deploying online.    

# 📜 License
This project is licensed under the MIT License. Feel free to use and modify it!

# 🤝 Contributing
Got ideas or improvements? Contributions are welcome!

📌 Fork this repo → Make changes → Submit a PR

