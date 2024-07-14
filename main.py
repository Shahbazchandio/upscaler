from app import create_app, db
from app.models.user import User

app = create_app()

@app.cli.command("create-admin")
def create_admin():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    
    user = User(username=username)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    print(f"Admin user '{username}' created successfully.")

if __name__ == '__main__':
    app.run()