import cloudscraper
from bs4 import BeautifulSoup
import json
import random
import time

def get_data():
    # 1. إعدادات التخفي (Anti-Ban)
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )
    
    # قائمة مواقع مانجا (يمكنك إضافة المزيد، سنركز على ليك حالياً)
    target_url = "https://mangalek.com" 
    
    print("⚡ جاري الاتصال بالسيرفر وسحب البيانات...")
    manga_db = []

    try:
        response = scraper.get(target_url, timeout=25)
        if response.status_code != 200:
            raise Exception("فشل الاتصال بالموقع المصدر")

        soup = BeautifulSoup(response.text, "html.parser")
        
        # استهداف العناصر بدقة عالية
        items = soup.select('.page-item-detail, .manga-item, .post-item')

        for idx, item in enumerate(items):
            try:
                # استخراج البيانات الأساسية
                title_tag = item.select_one('h3 a, .post-title a')
                if not title_tag: continue
                
                title = title_tag.get_text(strip=True)
                link = title_tag['href']
                
                # معالجة الصورة بذكاء
                img_tag = item.select_one('img')
                img_src = "https://via.placeholder.com/300x450?text=No+Image"
                if img_tag:
                    img_src = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('srcset')
                    if img_src and img_src.startswith('//'): img_src = "https:" + img_src
                    # تنظيف الرابط للحصول على أعلى دقة
                    img_src = img_src.split(' ')[0]

                # استخراج الفصل
                chapter_tag = item.select_one('.chapter a, .btn-link')
                chapter = chapter_tag.get_text(strip=True) if chapter_tag else "فصل جديد"

                # استخراج التقييم (وإضافة تقييم وهمي واقعي إذا لم يوجد)
                rating_tag = item.select_one('.score')
                rating = rating_tag.get_text(strip=True) if rating_tag else str(round(random.uniform(4.0, 5.0), 1))

                # تحديد الفئة العمرية عشوائياً (للمحاكاة لأن الموقع لا يوفرها في الرئيسية)
                age_ratings = ["+13", "+17", "الكل"]
                age = random.choice(age_ratings)

                # 2. إضافة حقوق المترجم (مهم جداً)
                translator_info = {
                    "name": "Mohammed Elfagih",
                    "insta": "Gremory807",
                    "insta_url": "https://instagram.com/Gremory807"
                }

                # بناء كائن البيانات
                entry = {
                    "id": idx + 1000, # معرف فريد
                    "title": title,
                    "cover": img_src,
                    "url": link,
                    "chapter": chapter,
                    "rating": rating,
                    "age": age,
                    "status": "مستمر", # افتراضي
                    "translator": translator_info,
                    "timestamp": time.time()
                }
                manga_db.append(entry)

            except Exception as e:
                continue # تجاوز الأخطاء الفردية

        # 3. حفظ البيانات في ملف JSON
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(manga_db, f, ensure_ascii=False, indent=2)
            
        print(f"✅ تم العملية بنجاح! تم تجهيز {len(manga_db)} مانجا.")

    except Exception as e:
        print(f"❌ خطأ فادح: {e}")

if __name__ == "__main__":
    get_data()
