from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_URL = "https://horoscope-app-api.vercel.app/api/v1"

def get_zodiac_sign(month, day):
    # Düzeltilmiş ve kontrol edilmiş burç tarihleri
    zodiac_dates = [
        (1, 20, "capricorn", "Oğlak"),
        (2, 19, "aquarius", "Kova"),      # 19 Şubat'a kadar Kova
        (3, 21, "pisces", "Balık"),       # 20 Şubat - 20 Mart
        (4, 20, "aries", "Koç"),          # 21 Mart - 19 Nisan
        (5, 21, "taurus", "Boğa"),        # 20 Nisan - 20 Mayıs
        (6, 21, "gemini", "İkizler"),     # 21 Mayıs - 20 Haziran
        (7, 23, "cancer", "Yengeç"),      # 21 Haziran - 22 Temmuz
        (8, 23, "leo", "Aslan"),          # 23 Temmuz - 22 Ağustos
        (9, 23, "virgo", "Başak"),        # 23 Ağustos - 22 Eylül
        (10, 23, "libra", "Terazi"),      # 23 Eylül - 22 Ekim
        (11, 22, "scorpio", "Akrep"),     # 23 Ekim - 21 Kasım
        (12, 22, "sagittarius", "Yay"),   # 22 Kasım - 21 Aralık
        (12, 31, "capricorn", "Oğlak")    # 22 Aralık - 19 Ocak
]
    
    for end_month, end_day, sign_en, sign_tr in zodiac_dates:
        if (month == end_month and day <= end_day):
            return sign_en, sign_tr
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

if __name__ == '__main__':
    app.run(port=5001, debug=True)