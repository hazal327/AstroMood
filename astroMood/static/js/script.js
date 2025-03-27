let calculatedSign = null;

document.addEventListener('DOMContentLoaded', () => {
    // Yıldız animasyonları
    function createStars() {
        const starsContainer = document.getElementById('stars');
        const starCount = 100;
        const characters = ['★', '✧', '✦', '✯', '✰'];
        
        starsContainer.innerHTML = '';
        for(let i = 0; i < starCount; i++) {
            const star = document.createElement('span');
            star.textContent = characters[Math.floor(Math.random() * characters.length)];
            star.style.left = `${Math.random() * 100}%`;
            star.style.top = `${Math.random() * -150}%`;
            star.style.fontSize = `${Math.random() * 20 + 10}px`;
            star.style.animationDelay = `${Math.random() * -20}s`;
            starsContainer.appendChild(star);
        }
    }
    createStars();
//feedback için
    let isRated = false;

document.querySelectorAll('.star').forEach(star => {
    star.addEventListener('mouseover', (e) => {
        if (isRated) return;
        const value = parseInt(e.target.dataset.value);
        document.querySelectorAll('.star').forEach((s, index) => {
            s.classList.toggle('full', index < value);
        });
    });

    star.addEventListener('click', async (e) => {
        if (isRated) return;

        isRated = true;
        const value = parseInt(e.target.dataset.value);

        // BACKEND’E GÖNDERİYORUZ
        await fetch('/submit_rating', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rating: value })
        });

        // Görsel efektler korunuyor
        document.querySelector('.stars-container').style.opacity = '0';
        document.querySelector('.rating-text').style.opacity = '0';
        document.querySelector('.thank-you-message').style.opacity = '1';
        
        // İstatistikleri al
const res = await fetch('/get_rating_stats');
const stats = await res.json();

// "Teşekkür ederiz!" sabit kalsın
const msgEl = document.querySelector('.thank-you-message');
msgEl.innerText = `Teşekkür ederiz!`;
msgEl.style.opacity = '1';
msgEl.style.maxHeight = '50px';

// Ortalama puanı alt satırda göster
const statsEl = document.getElementById("rating-stats");
statsEl.innerText = `Ortalama puan: ⭐️ ${stats.average} / 5 (${stats.total} oy)`;
statsEl.style.opacity = '1';

// Geri bildirim kutusunu kaldırma istersen burayı yoruma alabilirsin
setTimeout(() => document.querySelector('.feedback-container').remove(), 3000);

    });
});

    // Günleri doldur
    const daySelect = document.getElementById('day');
    for(let i = 1; i <= 31; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        daySelect.appendChild(option);
    }

    // Burç hesaplama
    document.getElementById('zodiacForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const day = parseInt(document.getElementById('day').value);
        const month = parseInt(document.getElementById('month').value);

        try {
            const response = await fetch('/api/calculate-zodiac', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ day, month })
            });
            
            const data = await response.json();
            if(data.error) throw new Error(data.error);

            calculatedSign = data.zodiac_en;
            showStep('date-section');
            document.getElementById('zodiacResult').innerHTML = `
                <div class="zodiac-result">
                    <h3>Burcunuz: ${data.zodiac_tr} (${data.zodiac_en.toUpperCase()})</h3>
                </div>
            `;
        } catch(error) {
            alert(error.message);
        }
    });

    // Yorum butonu event listener
    document.getElementById('showHoroscopeBtn').addEventListener('click', getHoroscope);
});

function getHoroscope() {
    const day = document.getElementById('horoscopeDay').value;
    showStep('result-section');
    
    fetch('/api/daily-horoscope', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ sign: calculatedSign, day })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('horoscopeResult');
        resultDiv.innerHTML = data.error ? 
            `<div class="error">${data.error}</div>` : 
            `<div class="horoscope-card">
                <h3>${data.sign} Burcu ${getDayText(day)} Yorumu</h3>
                <div class="date">${data.date}</div>
                <p class="prediction">${data.prediction}</p>
            </div>`;
    })
    .catch(error => console.error('Hata:', error));
}

function getDayText(day) {
    return { TODAY: 'Günlük', TOMORROW: 'Yarınki', YESTERDAY: 'Dünkü' }[day];
}

function showStep(stepId) {
    document.querySelectorAll('.active-step, .hidden-step').forEach(el => {
        el.classList.remove('active-step');
        el.classList.add('hidden-step');
    });
    const step = document.getElementById(stepId);
    step.classList.add('active-step');
    step.classList.remove('hidden-step');
}
// Feedback Sistemi
document.querySelectorAll('.star').forEach(star => {
    star.addEventListener('mouseover', (e) => {
        if(document.querySelector('.feedback-container').classList.contains('rated')) return;
        const value = parseInt(e.target.dataset.value);
        document.querySelectorAll('.star').forEach((s, index) => {
            s.classList.toggle('full', index < value);
        });
    });

    star.addEventListener('click', (e) => {
        if(document.querySelector('.feedback-container').classList.contains('rated')) return;
        document.querySelector('.feedback-container').classList.add('rated');
    });
});
// Seçimleri takip etmek için değişkenler
let selectedMood = null;
let selectedType = null;

// Mood seçim işleyicisi
document.querySelectorAll('.mood-buttons button, .type-buttons button').forEach(button => {
    button.addEventListener('click', (e) => {
        const isMoodButton = e.target.parentElement.classList.contains('mood-buttons');
        
        // Aktif sınıfı yönet
        document.querySelectorAll(isMoodButton ? '.mood-buttons button' : '.type-buttons button')
            .forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');

        // Değerleri güncelle
        if(isMoodButton) {
            selectedMood = e.target.dataset.mood;
        } else {
            selectedType = e.target.dataset.type;
        }
    });
});
document.getElementById('generateRecommendationBtn').addEventListener('click', async () => {
    if (!selectedMood || !selectedType) {
        alert('Lütfen hem mod hem de öneri türü seçin!');
        return;
    }

    const resultDiv = document.getElementById('recommendationResult');
    let recommendationText = "";

    if (selectedType === "activity") {
        try {
            const res = await fetch("/get_activity", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ 
                    mood: selectedMood, 
                    zodiac: calculatedSign 
                })
            });  // Artık kendi sunucuna istek atıyorsun
            const data = await res.json();
    
            if (data.error) {
                recommendationText = `Öneri bulunamadı: ${data.error}`;
            } else {
                recommendationText = `🎯 ${data.mood} ve ${data.zodiac} burcu için: ${data.activity}`;
            }
        } catch (error) {
            console.error("Aktivite önerisi hatası:", error);
            resultDiv.innerHTML = `<p>Aktivite önerisi alınırken bir hata oluştu.</p>`;
        }
    }

    else if (selectedType === "book") {
        // 📚 Google Books API - Kitap Önerisi
        if (selectedMood === "sad") {
            query = "üzgün |acı |kaybetmek | gözyaşı |dram | korku"; // sad mood için özel anahtar kelimeler
        } else if (selectedMood === "happy") {
            query = "mutluluk|pozitif |heyecan | güzellik | gülümseme ";
        } else if (selectedMood === "stressed") {
            query = "rahatlama|zihinsel huzur| kaygı | huzursuzluk";
        } else if (selectedMood === "energetic") {
            query = "  macera | deneyim | enerjik";
        }
    
        const res = await fetch(`https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(query)}&langRestrict=tr&maxResults=20`);
        const data = await res.json();
        const book = data.items[Math.floor(Math.random() * data.items.length)].volumeInfo;
    
        recommendationText = `${book.title} - ${book.authors?.[0] || "Bilinmeyen Yazar"}`;
    }

    else if (selectedType === "music") {
        // 🎵 iTunes Search API - Müzik Önerisi
        const moodKeyword = selectedMood === "sad" ? "sad" : selectedMood === "happy" ? "happy" : selectedMood === "stressed" ? "stressed" :selectedMood === "energetic" ? "energetic":  "music";
       
        const res = await fetch(`https://itunes.apple.com/search?term=${moodKeyword}&media=music&limit=25`);
        const data = await res.json();
        const track = data.results[Math.floor(Math.random() * data.results.length)];
        recommendationText = `${track.trackName} - ${track.artistName}`;
    }

    else if (selectedType === "movie") {
        try {
            const response = await fetch("/get_movie", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ 
                    mood: selectedMood, 
                    zodiac: calculatedSign 
                })
            });

            const data = await response.json();

            recommendationText = `${data.title} - ${data.release}`;

        } catch (error) {
            console.error("Film önerisi hatası:", error);
            resultDiv.innerHTML = `<p>Film önerisi alınırken bir hata oluştu.</p>`;
        }
        
    }

    // Sonucu yazdır
    resultDiv.innerHTML = `
        <h4>${selectedMood.toUpperCase()} modu için ${selectedType.toUpperCase()} önerisi:</h4>
        <p>${recommendationText}</p>
    `;

    document.addEventListener("DOMContentLoaded", () => {
        const toggleBtn = document.getElementById("toggleMotivation");
        const card = document.getElementById("motivationCard");
        const textEl = document.getElementById("motivationText");
    
        let quotes = [];
    
        // İlk yüklemede tüm alıntıları çek
        fetch("https://type.fit/api/quotes")
            .then(res => res.json())
            .then(data => {
                quotes = data;
            })
            .catch(() => {
                textEl.innerText = "Motivasyon alıntıları yüklenemedi 😕";
            });
    
        toggleBtn.addEventListener("click", () => {
            if (quotes.length > 0) {
                const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
                textEl.innerText = `"${randomQuote.text}" — ${randomQuote.author || "Bilinmeyen"}`;
            } else {
                textEl.innerText = "Motivasyon cümlesi bulunamadı 😅";
            }
    
            card.classList.toggle("hidden");
        });
    });
    

});
