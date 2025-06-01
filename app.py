from flask import Flask, render_template, send_from_directory, request
from config import Config
from models import db, Destination

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def seed_destinations():
    """Seed initial destination data if the table is empty"""
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

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

def init_db():
    with app.app_context():
        db.create_all()
        seed_destinations()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
