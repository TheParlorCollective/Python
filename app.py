
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tattoo_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    portfolio_links = db.Column(db.String(300), nullable=True)
    preferred_styles = db.Column(db.String(100), nullable=True)
    ratings = db.Column(db.Float, nullable=True)
    parlor_id = db.Column(db.Integer, db.ForeignKey('parlor.id'), nullable=True)

class Parlor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    artists = db.relationship('Artist', backref='parlor', lazy=True)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorites = db.Column(db.Text, nullable=True)  # Store favorite artist IDs as comma-separated values

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    client = db.relationship('Client', backref='appointments', lazy=True)
    artist = db.relationship('Artist', backref='appointments', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

# Routes
@app.route('/')
def index():
    artists = Artist.query.all()
    parlors = Parlor.query.all()
    clients = Client.query.all()
    return render_template('index.html', artists=artists, parlors=parlors, clients=clients)

@app.route('/add_artist', methods=['GET', 'POST'])
def add_artist():
    if request.method == 'POST':
        name = request.form['name']
        bio = request.form['bio']
        portfolio_links = request.form['portfolio_links']
        preferred_styles = request.form['preferred_styles']
        ratings = request.form['ratings']
        artist = Artist(name=name, bio=bio, portfolio_links=portfolio_links, preferred_styles=preferred_styles, ratings=ratings)
        db.session.add(artist)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_artist.html')

@app.route('/add_parlor', methods=['GET', 'POST'])
def add_parlor():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        parlor = Parlor(name=name, address=address)
        db.session.add(parlor)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_parlor.html')

# Initialize Database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    