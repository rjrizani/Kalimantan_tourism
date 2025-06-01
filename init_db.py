from app import app, db, User, init_db

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            print("Creating admin user...")
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
        
        print("Database initialization completed!")