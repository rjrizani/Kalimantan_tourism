from flask import Flask, render_template

app = Flask(__name__)

# Sample tourism destinations data
destinations = [
    {
        'name': 'Tanjung Puting National Park',
        'location': 'Central Kalimantan',
        'description': 'Famous for its orangutan conservation and river cruises through pristine rainforest.',
        'image': 'tanjung_puting.jpg'
    },
    {
        'name': 'Derawan Islands',
        'location': 'East Kalimantan',
        'description': 'Beautiful archipelago known for its marine biodiversity, beaches, and diving spots.',
        'image': 'derawan.jpg'
    },
    {
        'name': 'Mahakam River',
        'location': 'East Kalimantan',
        'description': 'Historic river offering cultural tours and glimpses of traditional Dayak villages.',
        'image': 'mahakam.jpg'
    }
]

@app.route('/')
def index():
    return render_template('index.html', destinations=destinations)

if __name__ == '__main__':
    app.run(debug=True)
