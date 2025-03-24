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

    // Feedback sistemi
    let isRated = false;
    document.querySelectorAll('.star').forEach(star => {
        star.addEventListener('mouseover', (e) => {
            if(isRated) return;
            const value = parseInt(e.target.dataset.value);
            document.querySelectorAll('.star').forEach((s, index) => {
                s.classList.toggle('full', index < value);
            });
        });

        star.addEventListener('click', (e) => {
            if(isRated) return;
            isRated = true;
            document.querySelector('.stars-container').style.opacity = '0';
            document.querySelector('.rating-text').style.opacity = '0';
            document.querySelector('.thank-you-message').style.opacity = '1';
            setTimeout(() => document.querySelector('.feedback-container').remove(), 2000);
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

// Öneri oluştur butonu
document.getElementById('generateRecommendationBtn').addEventListener('click', () => {
    if(!selectedMood || !selectedType) {
        alert('Lütfen hem mod hem de öneri türü seçin!');
        return;
    }
    
    // API çağrısı için mock data (Gerçek uygulamada API'ye bağlanmalı)
    const mockData = {
        happy: {
            music: "Upbeat pop müzikler - Taylor Swift - Shake It Off",
            movie: "Komedi filmleri - The Grand Budapest Hotel",
            book: "Mutluluk Becerileri - Stefan Klein",
            activity: "Açık havada yürüyüş yapın"
        },
        // Diğer mood'lar için veriler eklenmeli...
    };

    const resultDiv = document.getElementById('recommendationResult');
    resultDiv.innerHTML = `
        <h4>${selectedMood.toUpperCase()} modu için ${selectedType.toUpperCase()} önerisi:</h4>
        <p>${mockData[selectedMood][selectedType]}</p>
    `;
    resultDiv.style.display = 'block';
});