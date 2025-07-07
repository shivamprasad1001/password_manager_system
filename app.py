from flask import Flask, jsonify, render_template, request, redirect, url_for, session, send_file, flash
from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.Cipher import AES
import base64
from flask_mysqldb import MySQL
import os
import pandas as pd
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import hashlib

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('password_manager.log', maxBytes=1000000, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'James'
app.config['MYSQL_DB'] = 'password_manager'

mysql = MySQL(app)

# AES Secret Key (Must be 16, 24, or 32 bytes)
SECRET_KEY = b'16ByteSecretKey!'

# AES Encryption & Decryption
def encrypt_password(password):
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(password.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')
def decrypt_password(encrypted_password):
    try:
        encrypted_password = base64.b64decode(encrypted_password)
        nonce = encrypted_password[:16]
        ciphertext = encrypted_password[16:]
        cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext).decode('utf-8')
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return "Decryption Error"

# Log action to database
def log_action(user_id, action, description=""):
    try:
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        cur = mysql.connection.cursor()
        cur.execute(
            """INSERT INTO logs 
            (user_id, action, description, ip_address, user_agent) 
            VALUES (%s, %s, %s, %s, %s)""",
            (user_id, action, description, ip_address, user_agent)
        )
        mysql.connection.commit()
        logger.info(f"Action logged: {action} by user {user_id}")
    except Exception as e:
        logger.error(f"Failed to log action: {str(e)}")
    finally:
        if 'cur' in locals():
            cur.close()

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "☀️ Good morning"
    elif hour < 18:
        return "🌤️ Good afternoon"
    return "🌙 Good evening"

def username_color(username):
    colors = ["#00bcd4", "#f44336", "#4caf50", "#ff9800", "#9c27b0"]
    hash_val = int(hashlib.md5(username.encode()).hexdigest(), 16)
    return colors[hash_val % len(colors)]



@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        cur = mysql.connection.cursor()
        print(session)
        # Get password stats
        cur.execute("SELECT COUNT(*) FROM passwords WHERE user_id = %s", (user_id,))
        total_passwords = cur.fetchone()[0]
        
        # Get  passwords
        cur.execute("""
            SELECT * FROM passwords WHERE user_id = %s
            ORDER BY created_at DESC 
        """, (user_id,))
        recent_passwords = cur.fetchall()
        
        
        # Get recent logs
        cur.execute("""
            SELECT action, description, ip_address, created_at 
            FROM logs 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
        """, (session.get('user_id'),))
        logs = cur.fetchall()
        
        # Decrypt passwords for display
        decrypted_passwords = []
        for p in recent_passwords:
            decrypted_passwords.append({
                'id': p[0],
                'salt': p[1],
                'username': p[2],
                'password': decrypt_password(p[3]),
                'date': p[4].strftime('%b %d, %Y') if p[4] else ''
            })
        username = session['user']
        greeting = get_greeting()
        color = username_color(username)
        role = "Admin" if username == "shivam" else "Pro"  # Customize as needed
        return render_template('index.html',
                            username=username,
                            total_passwords=total_passwords,
                            passwords=decrypted_passwords,
                            greeting=greeting, 
                            color=color, 
                            role=role,
                            last_login=datetime.now().strftime('%b %d, %Y at %I:%M %p'))
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        flash('An error occurred while loading the dashboard', 'danger')
        return redirect(url_for('login'))
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    import uuid
    
    

    if request.method == 'POST':
        username = request.form['username']
        password = encrypt_password(request.form['password'])
        user_id = str(uuid.uuid4())

        
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (id, username, password_hash) VALUES (%s, %s, %s)",
                (user_id, username, password)
            )
            mysql.connection.commit()
            logger.info(f"New user registered: {username}")
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logger.warning(f"Registration failed for {username}: {str(e)}")
            flash('Username already exists!', 'danger')
        finally:
            if 'cur' in locals():
                cur.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user and (decrypt_password(user[2]) == password or user[2] == password):
                session['user_id'] = user[0]
                session['user'] = user[1]
                print(session)
                log_action(user[0], 'LOGIN_SUCCESS', 'User logged in successfully')
                logger.info(f"User {username} logged in successfully")
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            
            log_action(None, 'LOGIN_FAILED', f'Failed login attempt for username: {username}')
            logger.warning(f"Failed login attempt for username: {username}")
            flash('Invalid credentials', 'danger')
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash('An error occurred during login', 'danger')
        finally:
            if 'cur' in locals():
                cur.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        log_action(session.get('user_id'), 'LOGOUT', 'User logged out')
        logger.info(f"User {session['user']} logged out")
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/add_password', methods=['POST'])
def add_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    salt = request.form.get('salt')
    username = request.form['username']
    save_password = request.form['password']
    password_hash = encrypt_password(request.form['password'])
    user_id = session['user_id']
    new_data = [(user_id, salt, username, save_password)]
    
    try:
        save_to_excel(new_data)
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO passwords (salt, username, password_hash, user_id)
            VALUES (%s, %s, %s, %s)
        """, (salt, username, password_hash, user_id))
        mysql.connection.commit()
        log_action(session.get('user_id'), 'ADD_PASSWORD', f'Added password for {username}')
        logger.info(f"Password added for {username} by {session['user']}")
        flash('Password added successfully!', 'success')
    except Exception as e:
        log_action(session.get('user_id'), 'ADD_PASSWORD_FAILED', str(e))
        logger.error(f"Failed to add password: {str(e)}")
        flash('Failed to add password', 'danger')
    finally:
        if 'cur' in locals():
            cur.close()
    
    return redirect(url_for('dashboard'))

@app.route('/delete-password', methods=['POST'])
@app.route('/delete-password', methods=['POST'])
def delete_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    password_id = request.form.get('password_id')
    admin_username = request.form.get('admin_username')
    admin_password = request.form.get('admin_password')
    user_id = session['user_id']

    if not all([password_id, admin_username, admin_password]):
        flash("All fields are required.", "warning")
        return redirect(url_for('dashboard'))

    try:
        cur = mysql.connection.cursor()

        # Check if admin username exists
        cur.execute("SELECT username FROM users")
        usernames = [row[0] for row in cur.fetchall()]

        print(usernames)
        if admin_username not in usernames:
            log_action(user_id, 'DELETE_PASSWORD_FAILED', 'Invalid admin credentials')
            flash("Invalid admin credentials. username or password not match", "danger")
            return redirect(url_for('dashboard'))

        # Fetch admin credentials
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (admin_username,))
        admin = cur.fetchone()

        from werkzeug.security import check_password_hash

        if not admin or not decrypt_password(admin[1] != admin_password) or str(admin[0]) != str(user_id):
            log_action(user_id, 'DELETE_PASSWORD_FAILED', 'Invalid admin credentials')
            flash("Invalid admin credentials.", "danger")
            return redirect(url_for('dashboard'))

        # Check if password belongs to this user
        cur.execute("SELECT id FROM passwords WHERE id = %s AND user_id = %s", (password_id, user_id))
        password_info = cur.fetchone()

        if not password_info:
            flash("Unauthorized or invalid password.", "danger")
            return redirect(url_for('dashboard'))

        # Delete password
        cur.execute("DELETE FROM passwords WHERE id = %s", (password_id,))
        mysql.connection.commit()

        log_action(user_id, 'DELETE_PASSWORD', f"Deleted password ID {password_id}")
        flash("Password deleted successfully.", "success")

    except Exception as e:
        log_action(user_id, 'DELETE_PASSWORD_ERROR', str(e))
        logger.error(f"Password deletion error: {str(e)}")
        flash("An error occurred while deleting the password.", "danger")

    finally:
        if 'cur' in locals():
            cur.close()

    return redirect(url_for('dashboard'))


# Edit Password - Show Form
@app.route('/edit-password/<int:id>', methods=['GET'])
def edit_password(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, salt, username, password_hash 
            FROM passwords 
            WHERE id = %s
        """, (id,))
        password = cur.fetchone()
        
        if not password:
            flash('Password entry not found', 'danger')
            return redirect(url_for('dashboard'))
        
        # Decrypt the password for editing
        decrypted_password = decrypt_password(password[3])
        
        entry = {
            'id': password[0],
            'salt': password[1],
            'username': password[2],
            'password': decrypted_password
        }
        
        return render_template('edit.html', entry=entry)
        
    except Exception as e:
        logger.error(f"Error accessing password for editing: {str(e)}")
        flash('An error occurred while accessing the password', 'danger')
        return redirect(url_for('dashboard'))
    finally:
        if 'cur' in locals():
            cur.close()

# Update Password - Process Form
@app.route('/update-password/<int:id>', methods=['POST'])
def update_password(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        salt = request.form.get('salt')
        username = request.form['username']
        password = encrypt_password(request.form['password'])
        
        cur = mysql.connection.cursor()
        
            
        # Update the password
        cur.execute("""
            UPDATE passwords 
            SET salt = %s, username = %s, password_hash = %s 
            WHERE id = %s
        """, (salt, username, password, id))
        mysql.connection.commit()
        
        log_action(session.get('user_id'), 'UPDATE_PASSWORD', f'Updated password ID {id}')
        logger.info(f"Password ID {id} updated by {session['user']}")
        flash('Password updated successfully!', 'success')
        
    except Exception as e:
        mysql.connection.rollback()
        log_action(session.get('user_id'), 'UPDATE_PASSWORD_FAILED', str(e))
        logger.error(f"Failed to update password: {str(e)}")
        flash('An error occurred while updating the password', 'danger')
    finally:
        if 'cur' in locals():
            cur.close()
    
    return redirect(url_for('dashboard'))



# save password - Process Form
def save_to_excel(new_data):
    try:
        file_path = "password_backup.xlsx"
        new_df = pd.DataFrame(new_data, columns=['User_id', 'Website/App', 'username', 'Decrypted Password'])

        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path, engine="openpyxl")
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            updated_df = new_df

        updated_df.to_excel(file_path, index=False, engine="openpyxl")
        logger.info("Password backup updated successfully")
    except Exception as e:
        logger.error(f"Failed to update password backup: {str(e)}")

if __name__ == '__main__':
    # Create logs table if it doesn't exist
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    action VARCHAR(50) NOT NULL,
                    description TEXT,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            mysql.connection.commit()
            cur.close()
            logger.info("Database tables initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {str(e)}")
    
    app.run(debug=True, host='0.0.0.0')