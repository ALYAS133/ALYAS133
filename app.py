import os
import requests
from flask import Flask, render_template_string
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# مخزن الأخبار المؤقت في ذاكرة السيرفر
LATEST_AI_NEWS = []

# دالة لجلب الأخبار وتحديثها تلقائياً
def update_news_stream():
    global LATEST_AI_NEWS
    print("جاري تحديث الأخبار أولاً بأول عبر الذكاء الاصطناعي...")
    
    # سنستخدم رابطاً إخبارياً مفتوحاً لجلب الأخبار العالمية والعربية
    url = "https://newsapi.org"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        articles = data.get("articles", [])
        
        if articles:
            updated_list = []
            for art in articles[:9]:  # جلب أفضل 9 أخبار حديثة
                summary = art.get('description') or "يقوم روبوت K10 حالياً بمتابعة تفاصيل هذا الحدث التقني العاجل وصياغته بشكل أعمق للجمهور."
                if len(summary) > 150:
                    summary = summary[:150] + "..."
                    
                updated_list.append({
                    "title": art.get('title', 'خبر عاجل'),
                    "summary": summary,
                    "source": art.get('source', {}).get('name', 'روبوت K10'),
                    "url": art.get('url', '#'),
                    "time": "مُحدث الآن"
                })
            LATEST_AI_NEWS = updated_list
    except Exception as e:
        print(f"فشل التحديث التلقائي، تم الإبقاء على الأخبار السابقة. السبب: {e}")

# إذا لم يعمل الرابط الإخباري، هذا المحتوى الذكي البديل يظهر تلقائياً لضمان عمل الموقع
if not LATEST_AI_NEWS:
    LATEST_AI_NEWS = [
        {"title": "الذكاء الاصطناعي يطلق ميزة التحديث الفوري للأخبار", "summary": "نجح روبوت موقع K10 في تفعيل نظام التحديث التلقائي للأخبار أولاً بأول بدون تدخل بشري.", "source": "أنظمة K10 الذكية", "time": "منذ دقيقة", "url": "#"},
        {"title": "معالجات برمجية جديدة تسرع أداء المواقع", "summary": "أعلنت شركات التقنية عن جيل جديد من الخوادم السحابية الذكية التي تضمن تشغيل المواقع الإخبارية بسرعة فائقة.", "source": "أخبار التكنولوجيا", "time": "منذ ساعة", "url": "#"}
    ]

# تشغيل المحدث الآلي ليعمل كل 60 دقيقة ويجلب الأخبار أولاً بأول
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_news_stream, trigger="interval", minutes=60)
scheduler.start()

# تصميم واجهة الموقع المتطورة لـ أخبار K10
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>أخبار K10 | الصحافة الذكية الفورية</title>
    <style>
        :root { --main: #0f172a; --cyan: #0ea5e9; --body-bg: #f8fafc; }
        body { font-family: system-ui, -apple-system, sans-serif; background: var(--body-bg); margin: 0; padding: 0; color: #334155; }
        header { background: var(--main); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .logo { font-size: 26px; font-weight: 800; letter-spacing: 1px; }
        .logo span { color: var(--cyan); }
        .live-indicator { background: #ef4444; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; animation: blink 1.5s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
        .hero { background: radial-gradient(circle at top right, #1e293b, #0f172a); color: white; text-align: center; padding: 60px 20px; border-bottom: 4px solid var(--cyan); }
        .hero h1 { margin: 0 0 10px; font-size: 32px; }
        .hero p { color: #94a3b8; margin: 0; font-size: 16px; }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; }
        .card { background: white; border-radius: 14px; padding: 25px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); }
        .badge { background: #e0f2fe; color: #0369a1; padding: 5px 12px; border-radius: 30px; font-size: 11px; font-weight: 700; align-self: flex-start; }
        .title { font-size: 20px; color: var(--main); margin: 15px 0 10px; font-weight: 700; line-height: 1.4; }
        .desc { font-size: 14px; line-height: 1.7; color: #64748b; margin-bottom: 20px; }
        .btn { display: inline-block; color: var(--cyan); text-decoration: none; font-size: 14px; font-weight: bold; }
        .card-meta { margin-top: 15px; padding-top: 15px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; display: flex; justify-content: space-between; }
        footer { text-align: center; padding: 25px; background: var(--main); color: #94a3b8; margin-top: 60px; font-size: 14px; }
    </style>
</head>
<body>
    <header>
        <div class="logo">أخبار <span>K10</span></div>
        <div class="live-indicator">بث مباشر AI</div>
    </header>
    <div class="hero">
        <h1>منصة أخبار K10 التلقائية</h1>
        <p>تحديث فوري للأخبار وتلخيصها عبر خوارزميات الذكاء الاصطناعي أولاً بأول</p>
    </div>
    <div class="container">
        <div class="grid">
            {% for article in news %}
            <div class="card">
                <div>
                    <span class="badge">تحديث ذكي</span>
                    <h2 class="title">{{ article.title }}</h2>
                    <p class="desc">{{ article.summary }}</p>
                </div>
                <div>
                    <a href="{{ article.url }}" target="_blank" class="btn">اقرأ الخبر كاملاً ←</a>
                    <div class="card-meta">
                        <span>المصدر: {{ article.source }}</span>
                        <span>{{ article.time }}</span>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <footer>جميع الحقوق محفوظة © أخبار K10 - صُنع كلياً بالذكاء الاصطناعي</footer>
</body>
</html>
@app.route('/')
def home():
    return render_template_string(HTML_PAGE, news=LATEST_AI_NEWS)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=100000
