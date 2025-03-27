from flask import Flask, render_template, request, jsonify
import requests
import random
import json
from pathlib import Path
from statistics import mean
from datetime import datetime

app = Flask(__name__)

if app.config.get('TESTING'):
    FEEDBACK_FILE = Path(__file__).parent / "test_feedback.json"
else:
    FEEDBACK_FILE = Path("feedback_ratings.json")
if FEEDBACK_FILE.exists():
    with open(FEEDBACK_FILE, "r") as f:
        ratings = json.load(f)
else:
    ratings = []
API_URL = "https://horoscope-app-api.vercel.app/api/v1"

def get_zodiac_sign(month, day):
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "aquarius", "Kova"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "pisces", "Balık"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "aries", "Koç"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "taurus", "Boğa"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "gemini", "İkizler"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "cancer", "Yengeç"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "leo", "Aslan"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "virgo", "Başak"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "libra", "Terazi"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "scorpio", "Akrep"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "sagittarius", "Yay"
    else:
        return "capricorn", "Oğlak"

@app.route('/')
def ana_sayfa():
    return render_template('index.html')

@app.route('/api/calculate-zodiac', methods=['POST'])
def api_calculate_zodiac():
    try:
        data = request.get_json()
        day = int(data['day'])
        month = int(data['month'])
        
        sign_en, sign_tr = get_zodiac_sign(month, day)
        
        return jsonify({
            "zodiac_en": sign_en,
            "zodiac_tr": sign_tr,
            "sign": sign_en
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/daily-horoscope', methods=['POST'])
def get_daily_horoscope():
    try:
        data = request.get_json()
        sign = data['sign'].lower()
        day = data.get('day', 'TODAY').upper()
        
        response = requests.get(
            f"{API_URL}/get-horoscope/daily",
            params={"sign": sign, "day": day}
        )
        response.raise_for_status()
        
        api_data = response.json()
        
        return jsonify({
            "prediction": api_data.get("data", {}).get("horoscope_data", "Yorum bulunamadı"),
            "sign": sign.capitalize(),
            "date": api_data.get("data", {}).get("date", datetime.now().strftime("%Y-%m-%d"))
        })
    
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": f"API Hatası: {err.response.text}"}), err.response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/submit_rating", methods=["POST"])
def submit_rating():
    data = request.get_json()
    rating = data.get("rating")
    if rating in [1, 2, 3, 4, 5]:
        ratings.append(rating)
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(ratings, f)
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@app.route("/get_rating_stats")
def get_rating_stats():
    from statistics import mean
    if ratings:
        return jsonify({
            "average": round(mean(ratings), 2),
            "total": len(ratings),
            "counts": {str(i): ratings.count(i) for i in range(1, 6)}
        })
@app.route("/rating_stats")
def rating_stats():
    return render_template(
        "stats.html",
        average=round(mean(ratings), 2) if ratings else 0,
        total=len(ratings),
        counts={str(i): ratings.count(i) for i in range(1,6)}
    )
        
mood_activity_map = {
    "happy": [
        "Have a picnic in the park",
        "Organize a dance party",
        "Take a spontaneous road trip",
        "Host a game night with friends",
        "Go to an amusement park"
    ],
    "sad": [
        "Practice meditation",
        "Write in a journal",
        "Take a relaxing bath",
        "Listen to calming music",
        "Do some gentle yoga"
    ],
    "stressed": [
        "Try a breathing exercise",
        "Go for a nature walk",
        "Practice mindfulness meditation",
        "Do a puzzle or coloring activity",
        "Take a relaxing art class"
    ],
    "energetic": [
        "Go rock climbing",
        "Try a high-intensity workout",
        "Join a sports league",
        "Go hiking",
        "Take a dance fitness class"
    ]
}

zodiac_activity_map = {
    "aries": [
        "Start a challenging physical project",
        "Try a competitive sport",
        "Attend a leadership workshop",
        "Go on an adventure expedition"
    ],
    "taurus": [
        "Visit a gourmet restaurant",
        "Do gardening",
        "Take a cooking class",
        "Enjoy a relaxing spa day"
    ],
    "gemini": [
        "Attend a public speaking workshop",
        "Join a debate club",
        "Take an improv comedy class",
        "Go to a networking event"
    ],
    "cancer": [
        "Have a family gathering",
        "Create a scrapbook",
        "Practice home cooking",
        "Do a creative writing session"
    ],
    "leo": [
        "Perform on stage",
        "Attend a theater workshop",
        "Host a party",
        "Take a photography class"
    ],
    "virgo": [
        "Organize a community cleanup",
        "Take a detailed skill workshop",
        "Do intensive study or learning",
        "Practice precision crafts"
    ],
    "libra": [
        "Attend an art exhibition",
        "Take a group dance class",
        "Practice meditation in a group",
        "Volunteer for a social cause"
    ],
    "scorpio": [
        "Do intense research",
        "Practice martial arts",
        "Take a psychology workshop",
        "Engage in deep meditation"
    ],
    "sagittarius": [
        "Plan an international trip",
        "Take a philosophy course",
        "Go on a hiking adventure",
        "Attend a cultural festival"
    ],
    "capricorn": [
        "Develop a business plan",
        "Take a professional development course",
        "Practice mountain climbing",
        "Organize a networking event"
    ],
    "aquarius": [
        "Join a tech workshop",
        "Attend a science lecture",
        "Participate in a community innovation project",
        "Try virtual reality experiences"
    ],
    "pisces": [
        "Take an art therapy class",
        "Practice ocean-related activities",
        "Attend a music workshop",
        "Do spiritual meditation"
    ]
}

@app.route("/get_activity", methods=["POST"])
def get_personalized_activity():
    try:
        data = request.get_json()
        mood = data.get("mood", "").lower()
        zodiac = data.get("zodiac", "").lower()

        # Validate inputs
        if mood not in mood_activity_map or zodiac not in zodiac_activity_map:
            return jsonify({"error": "Invalid mood or zodiac sign"}), 400

        # Get activities for mood and zodiac
        mood_activities = mood_activity_map.get(mood, [])
        zodiac_activities = zodiac_activity_map.get(zodiac, [])

        # Combine and randomize activities
        all_activities = mood_activities + zodiac_activities
        
        if not all_activities:
            return jsonify({"error": "No activities found"}), 404

        # Choose a random activity
        activity = random.choice(all_activities)

        return jsonify({
            "activity": activity,
            "mood": mood.capitalize(),
            "zodiac": zodiac.capitalize()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
TMDB_API_KEY = "ac398ec83301c3b8274302c22fbffef3"    
# Map moods and zodiac signs to movie genres
mood_genre_map = {
    "happy": 10751,  # Comedy
    "sad": 18,  # Drama
    "energetic": 28,  # Action
    "stressed": 35,  # Comedy
}
zodiac_genre_map = {
   "aries": 28,  # Action
    "taurus": 10749,  # Romance
    "gemini": 35,  # Comedy
    "cancer": 18,  # Drama
    "leo": 12,  # Adventure
    "virgo": 9648,  # Mystery
    "libra": 10751,  # Family
    "scorpio": 27,  # Horror
    "sagittarius": 878,  # Sci-Fi
    "capricorn": 80,  # Crime
    "aquarius": 99,  # Documentary
    "pisces": 14,  # Fantasy
} 

@app.route("/get_movie", methods=["POST"])
def get_movie():
    try:
        data = request.get_json()
        mood = data.get("mood", "").lower()
        zodiac = data.get("zodiac", "").lower()

        genre_ids = set()

        if mood in mood_genre_map:
            genre_ids.add(mood_genre_map[mood])
        if zodiac in zodiac_genre_map:
            genre_ids.add(zodiac_genre_map[zodiac])

        if not genre_ids:
            return jsonify({"error": "Mood or Zodiac sign not recognized."}), 400

        genre_ids_str = ",".join(map(str, genre_ids))

        url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_ids_str}&sort_by=popularity.desc&language=en-US&with_original_language=en"

        response = requests.get(url)
        movies = response.json().get("results", [])

        if not movies:
            return jsonify({"error": "No movies found for this mood and zodiac sign."})

        movie = random.choice(movies)

        return jsonify({
            "title": movie["title"],
            "overview": movie["overview"],
            "release": movie["release_date"]
        })

    except Exception as e:
        return jsonify({"error": "Movie could not be retrieved", "details": str(e)})
if __name__ == "__main__":
    app.run(debug=True, port=5001)


