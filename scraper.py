import cloudscraper
from bs4 import BeautifulSoup
import json
import time

def start_scraping():
    # إنشاء متصفح وهمي متطور لتجاوز الحماية
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome','platform': 'windows','mobile': False}
    )
    
    url = "https://mangalek.com" 
    
    try:
        print("🚀 محاولة سحب البيانات من الموقع...")
        # إضافة headers إضافية للتمويه
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        res = scraper.get(url, headers=headers, timeout=30)
        
        if res.status_code != 200:
            print(f"❌ فشل الاتصال. كود الحالة: {res.status_code}")
            return

        soup = BeautifulSoup(res.text, "html.parser")
        manga_data = []

        # البحث عن العناصر (تأكدنا من المسارات الصحيحة للموقع)
        items = soup.select('.page-item-detail, .manga-item')
        
        for index, item in enumerate(items[:20]): # سحب أول 20 مانجا
            title_el = item.select_one('h3 a')
            img_el = item.select_one('img')
            
            if title_el and img_el:
                title = title_el.get_text(strip=True)
                m_url = title_el['href']
                img = img_el.get('data-src') or img_el.get('src') or ""
                if img.startswith('//'): img = "https:" + img
                
                manga_data.append({
                    "id": index + 1000,
                    "title": title,
                    "cover": img,
                    "url": m_url,
                    "chapter": "فصل جديد",
                    "rating": "4.9",
                    "age": "+13",
                    "translator": {"name": "Mohammed Elfagih", "insta": "Gremory807"}
                })

        # حفظ الملف حتى لو القائمة فارغة لتجنب خطأ السيرفر
        if not manga_data:
            print("⚠️ لم يتم العثور على مانجا، جاري وضع بيانات تجريبية")
            manga_data = [{"id": 1, "title": "جاري التحديث...", "cover": "", "url": "#"}]

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(manga_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ تم إنشاء ملف data.json بنجاح وبداخله {len(manga_data)} مانجا")

    except Exception as e:
        print(f"❌ خطأ تقني: {e}")
        # إنشاء ملف فارغ لمنع تعطل السيرفر
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

if __name__ == "__main__":
    start_scraping()
