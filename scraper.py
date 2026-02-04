import cloudscraper
from bs4 import BeautifulSoup
import json
import os

def start_scraping():
    # استخدام متصفح وهمي لتجاوز الحماية
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','mobile': False})
    url = "https://mangalek.com" 
    
    try:
        print("🔍 محاولة سحب البيانات...")
        res = scraper.get(url, timeout=30)
        soup = BeautifulSoup(res.text, "html.parser")
        manga_data = []

        # البحث عن المانجا
        items = soup.select('.page-item-detail, .manga-item')
        
        for index, item in enumerate(items[:20]):
            title_el = item.select_one('h3 a')
            img_el = item.select_one('img')
            if title_el and img_el:
                img = img_el.get('data-src') or img_el.get('src') or ""
                if img.startswith('//'): img = "https:" + img
                manga_data.append({
                    "id": index + 1,
                    "title": title_el.get_text(strip=True),
                    "cover": img,
                    "url": title_el['href'],
                    "chapter": "فصل جديد",
                    "translator": {"name": "Mohammed Elfagih", "insta": "Gremory807"}
                })

        # التأكد من إنشاء الملف دائماً لمنع خطأ السيرفر
        if not manga_data:
            print("⚠️ لم نجد بيانات، سنضع بيانات مؤقتة")
            manga_data = [{"id": 0, "title": "جاري التحديث...", "cover": "", "url": "#"}]

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(manga_data, f, ensure_ascii=False, indent=2)
        print(f"✅ تم إنشاء data.json بنجاح!")

    except Exception as e:
        print(f"❌ خطأ: {e}")
        # إنشاء ملف فارغ إجبارياً لمنع السيرفر من الانهيار
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

if __name__ == "__main__":
    start_scraping()
