from flask import Flask, request, jsonify
from flask_cors import CORS
from movie_recommend import recommend
import pickle

# Load objects
with open('vectorizer.pkl', 'rb') as f:
    cv = pickle.load(f)
    
with open('new_df.pkl', 'rb') as f:
    new_df = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)

@app.route('/')
def home():
    return "Flask server is running!"

@app.errorhandler(404)
def not_found(e):
    return "Page not found!", 404

@app.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error!", 500

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = new_df['title'].tolist()  # convert the 'title' column to a list
    return jsonify(movies)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    movie_name = data['movie_name']
    recommendations = recommend(movie_name)
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
