import os
import django
import requests

# Django ayarlarını yüklüyoruz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ascent_web.settings')
django.setup()

from stories.models import Story # Senin model ismin farklıysa burayı düzelt

API_KEY = '136267ffdad4436b81f340b29b7e5515'
BASE_URL = 'https://api.themoviedb.org/3'

def save_to_db(data, category):
    for item in data:
        title = item.get('title') or item.get('name')
        description = item.get('overview')
        rating = item.get('vote_average')
        poster_path = item.get('poster_path')
        image_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

        # Veritabanına kaydet (Varsa güncelle, yoksa ekle)
        Story.objects.update_or_create(
            title=title,
            defaults={
                'description': description,
                'rating': rating,
                'category': category,
                'image_url': image_url
            }
        )
    print(f"{category} kategorisinden {len(data)} içerik eklendi!")

def fetch_content(media_type, category_label, count):
    # Sayfa başı 20 sonuç geldiği için döngüyle çekiyoruz
    results = []
    page = 1
    while len(results) < count:
        url = f"{BASE_URL}/discover/{media_type}?api_key={API_KEY}&page={page}&language=tr-TR&sort_by=vote_count.desc"
        
        # Anime ve Çizgi Film için ekstra filtreler (Genre ID'leri)
        if category_label == 'Anime' or category_label == 'Çizgi Film':
            url += "&with_genres=16" # Animation genre id
            
        response = requests.get(url).json()
        new_items = response.get('results', [])
        if not new_items: break
        
        results.extend(new_items)
        page += 1
        
    save_to_db(results[:count], category_label)

if __name__ == '__main__':
    print("Veri çekme işlemi başlıyor...")
    fetch_content('movie', 'Film', 50)
    fetch_content('tv', 'Dizi', 50)
    fetch_content('tv', 'Anime', 15)
    print("İşlem tamamlandı! Siteni yenileyip kontrol edebilirsin.")