from flask import Flask, render_template

app = Flask(__name__)

# Sample tourism destinations data
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

@app.route('/')
def index():
    return render_template('index.html', destinations=destinations)

if __name__ == '__main__':
    app.run(debug=True)
