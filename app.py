from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Destination, Article
import requests
from datetime import datetime
import logging
from functools import wraps
from forms import LoginForm, RegistrationForm, DestinationForm
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    destinations = Destination.query.all()
    articles = Article.query.order_by(Article.updated_at.desc()).all()
    return render_template('admin/dashboard.html', destinations=destinations, articles=articles)

@app.route('/admin/destination/new', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_destination_new():
    form = DestinationForm()
    if form.validate_on_submit():
        destination = Destination(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data,
            image=form.image.data
        )
        db.session.add(destination)
        db.session.commit()
        flash('Destination added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/destination_form.html', form=form)

@app.route('/admin/destination/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_destination_edit(id):
    destination = Destination.query.get_or_404(id)
    form = DestinationForm(obj=destination)
    if form.validate_on_submit():
        destination.name = form.name.data
        destination.location = form.location.data
        destination.description = form.description.data
        destination.image = form.image.data
        db.session.commit()
        flash('Destination updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/destination_form.html', form=form, destination=destination)

@app.route('/admin/destination/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_destination_delete(id):
    destination = Destination.query.get_or_404(id)
    db.session.delete(destination)
    db.session.commit()
    flash('Destination deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Public routes
@app.route('/')
def index():
    destinations = Destination.query.all()
    return render_template('index.html', destinations=destinations)

@app.route('/destination/<name>')
def destination_detail(name):
    destination = Destination.query.filter_by(name=name).first_or_404()
    return render_template('destination_detail.html', destination=destination)

@app.route('/developer')
def developer():
    return render_template('developer.html')

# Article routes
@app.route('/articles')
def articles():
    articles = Article.query.order_by(Article.updated_at.desc()).all()
    return render_template('articles.html', articles=articles)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article_detail.html', article=article)

@app.route('/admin/sync-articles')
@login_required
@admin_required
def sync_articles():
    try:
        # Fetch articles from API with timeout and error handling
        api_url = app.config['ARTICLES_API_URL']
        headers = {'Authorization': f'Bearer {app.config["API_KEY"]}'}
        response = requests.get(api_url + '/articles', headers=headers, timeout=10)
        response.raise_for_status()
        
        articles_data = response.json()
        
        # Update local database
        for article_data in articles_data:
            existing_article = Article.query.filter_by(api_id=str(article_data['id'])).first()
            
            if existing_article:
                # Update existing article
                existing_article.title = article_data['title']
                existing_article.content = article_data['content']
                existing_article.updated_at = datetime.utcnow()
            else:
                # Create new article
                new_article = Article(
                    api_id=str(article_data['id']),
                    title=article_data['title'],
                    content=article_data['content']
                )
                db.session.add(new_article)
        
        db.session.commit()
        flash('Articles synchronized successfully!', 'success')
        
    except requests.RequestException as e:
        logging.error(f"API sync error: {str(e)}")
        flash('Error synchronizing articles. Please try again later.', 'danger')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

def init_db():
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')  # Change this password in production
            db.session.add(admin)
            db.session.commit()
        # Seed destinations if empty
        if Destination.query.count() == 0:
            destinations = [
                {
                    'name': 'Tanjung Puting National Park',
                    'location': 'Central Kalimantan',
                    'description': 'Famous for its orangutan conservation and river cruises through pristine rainforest.',
                    'image': 'Tanjung Puting National Park.jpeg'
                },
                {
                    'name': 'Derawan Islands',
                    'location': 'East Kalimantan',
                    'description': 'Beautiful archipelago known for its marine biodiversity, beaches, and diving spots.',
                    'image': 'Derawan Islands.jpeg'
                },
                {
                    'name': 'Mahakam River',
                    'location': 'East Kalimantan',
                    'description': 'Historic river offering cultural tours and glimpses of traditional Dayak villages.',
                    'image': 'Mahakam River.jpeg'
                }
            ]
            for dest_data in destinations:
                destination = Destination(**dest_data)
                db.session.add(destination)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
