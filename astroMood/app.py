from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

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
    else:
        return jsonify({
            "average": 0,
            "total": 0,
            "counts": {str(i): 0 for i in range(1, 6)}
        })


@app.route("/get_activity")
def get_activity():
    try:
        res = requests.get("https://www.boredapi.com/api/activity")
        data = res.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Aktivite getirilemedi", "details": str(e)})
    

@app.route("/get_movie")
def get_movie():
    try:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=popularity.desc&language=tr-TR"
        response = requests.get(url)
        data = response.json()
        movies = data.get("results", [])

        if not movies:
            return jsonify({"error": "Film bulunamadı"})

        from random import choice
        movie = choice(movies)

        return jsonify({
            "title": movie["title"],
            "overview": movie["overview"],
            "release": movie["release_date"]
        })

    except Exception as e:
        return jsonify({"error": "Film alınamadı", "details": str(e)})
    

if __name__ == '__main__':
    app.run(port=5001, debug=True)


