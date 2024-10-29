from app import db, User, app
from werkzeug.security import generate_password_hash

# Create an application context to work with the database
with app.app_context():
    username = "admin"
    raw_password = "Sel1d1Qadm1n"  # Replace with your desired password

    # Generate hashed password
    hashed_password = generate_password_hash(raw_password)

    # Create the user object with the hashed password
    admin_user = User(username=username, password=hashed_password)

    # Add the user to the session and commit to save it
    db.session.add(admin_user)
    db.session.commit()

    print("Admin user created successfully!")

