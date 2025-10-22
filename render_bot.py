from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, jsonify
import random
import os
from datetime import datetime
import threading
import requests
import time

# === إعدادات البوت ===
TOKEN = "8446070901:AAEEl7gFxqyA_cExC5yGXzygAcZMdjIipmI"
CHANNEL_USERNAME = "@Flix1211"

# === تخزين البيانات ===
bot_data = {
    "bot_name": "البوت الإسلامي",
    "channel": CHANNEL_USERNAME,
    "last_message": "لم يتم إرسال رسائل بعد",
    "last_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_messages": 0,
    "status": "🟢 يعمل على Render",
    "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "messages_history": [],
    "monitor_pings": 0,
    "last_ping": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

islamic_messages = [
    "📖 {قُلْ هُوَ اللَّهُ أَحَدٌ، اللَّهُ الصَّمَدُ، لَمْ يَلِدْ وَلَمْ يُولَدْ، وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ} - سورة الإخلاص",
    "🌙 قال رسول الله ﷺ: 'تبسمك في وجه أخيك صدقة'",
    "🙏 اللهم إني أسألك علماً نافعاً، ورزقاً طيباً، وعملاً متقبلاً",
    "💫 سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر",
    "📖 {رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ} - سورة البقرة",
    "🕌 {إِنَّ الصَّلَاةَ كَانَتْ عَلَى الْمُؤْمِنِينَ كِتَابًا مَوْقُوتًا} - سورة النساء",
    "🌿 قال رسول الله ﷺ: 'الكلمة الطيبة صدقة'",
    "🕋 {وَأَقِيمُوا الصَّلَاةَ وَآتُوا الزَّكَاةَ وَارْكَعُوا مَعَ الرَّاكِعِينَ} - سورة البقرة",
    "🌟 {وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا} - سورة الطلاق",
    "📚 قال رسول الله ﷺ: 'طلب العلم فريضة على كل مسلم'"
]

# === تطبيق ويب للعرض ===
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>البوت الإسلامي - Render</title>
        <style>
            body { font-family: Arial; background: #f0f8ff; padding: 40px; text-align: center; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
            h1 { color: #2c5aa0; }
            .stats { background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .message { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-right: 4px solid #2c5aa0; }
            .monitor { background: #e8f5e8; padding: 15px; border-radius: 10px; margin: 15px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🕌 البوت الإسلامي</h1>
            <p>يعمل على Render Cloud 24/7</p>
            
            <div class="stats">
                <h3>📊 الإحصائيات</h3>
                <p><strong>القناة:</strong> """ + bot_data["channel"] + """</p>
                <p><strong>عدد الرسائل:</strong> """ + str(bot_data["total_messages"]) + """</p>
                <p><strong>آخر رسالة:</strong> """ + bot_data["last_message"] + """</p>
                <p><strong>الوقت:</strong> """ + bot_data["last_time"] + """</p>
                <p><strong>الحالة:</strong> """ + bot_data["status"] + """</p>
            </div>

            <div class="monitor">
                <h3>📡 نظام المراقبة</h3>
                <p><strong>عدد طلبات المراقبة:</strong> """ + str(bot_data["monitor_pings"]) + """</p>
                <p><strong>آخر طلب مراقبة:</strong> """ + bot_data["last_ping"] + """</p>
                <p><strong>نظام المراقبة نشط</strong> ✅ يمنع إيقاف الخدمة</p>
            </div>
            
            <div class="message">
                <h3>📨 آخر الرسائل</h3>
                <p>""" + bot_data["last_message"] + """</p>
                <small>""" + bot_data["last_time"] + """</small>
            </div>
            
            <p>⏰ البوت يرسل رسائل تلقائية كل ساعة إلى القناة</p>
            <p>🔄 نظام المراقبة يعمل كل 10 دقائق للحفاظ على التشغيل</p>
        </div>
    </body>
    </html>
    """

@app.route('/api/data')
def api_data():
    return jsonify(bot_data)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/ping')
def ping():
    """نقطة نهاية للمراقبة"""
    bot_data["monitor_pings"] += 1
    bot_data["last_ping"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] طلب مراقبة #{bot_data['monitor_pings']}")
    return jsonify({"status": "pong", "pings": bot_data["monitor_pings"]})

def update_bot_data(message):
    """تحديث بيانات البوت"""
    bot_data["last_message"] = message
    bot_data["last_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot_data["total_messages"] += 1
    bot_data["messages_history"].append({
        "message": message,
        "time": bot_data["last_time"]
    })
    if len(bot_data["messages_history"]) > 10:
        bot_data["messages_history"].pop(0)

# === دوال بوت التلجرام ===
async def send_to_channel(context: ContextTypes.DEFAULT_TYPE):
    try:
        message = random.choice(islamic_messages)
        await context.bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=message,
            parse_mode='Markdown'
        )
        update_bot_data(message)
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] تم إرسال: {message[:50]}...")
    except Exception as e:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] خطأ: {e}")
        bot_data["status"] = f"🔴 خطأ: {str(e)}"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🕌 البوت الإسلامي يعمل على السحابة!\n\n"
        f"📊 الإحصائيات:\n"
        f"• القناة: {CHANNEL_USERNAME}\n"
        f"• الرسائل المرسلة: {bot_data['total_messages']}\n"
        f"• آخر رسالة: {bot_data['last_time']}\n"
        f"• يعمل منذ: {bot_data['start_time']}\n\n"
        f"🌐 الموقع: https://your-app-name.onrender.com"
    )

def run_flask_app():
    """تشغيل تطبيق Flask"""
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 بدء خادم Flask على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot():
    """تشغيل بوت التلجرام"""
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start_command))
        
        job_queue = application.job_queue
        if job_queue:
            # إرسال رسالة كل ساعة (3600 ثانية)
            job_queue.run_repeating(send_to_channel, interval=3600, first=5)
            print("✅ تم تفعيل الجدولة التلقائية - رسائل كل ساعة")
        
        print("🤖 بوت التلجرام يعمل على Render...")
        application.run_polling()
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
        bot_data["status"] = f"🔴 خطأ: {str(e)}"

def start_self_monitoring():
    """بدء نظام المراقبة الذاتية"""
    def monitor_loop():
        # انتظر حتى يعمل الخادم
        time.sleep(10)
        
        while True:
            try:
                # احصل على رابط التطبيق من متغير بيئي أو استخدم افتراضي
                app_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://your-app-name.onrender.com')
                
                # أرسل طلب مراقبة إلى التطبيق نفسه
                response = requests.get(f"{app_url}/api/ping", timeout=10)
                
                if response.status_code == 200:
                    print(f"📡 [{datetime.now().strftime('%H:%M:%S')}] المراقبة نشطة - طلب #{bot_data['monitor_pings']}")
                else:
                    print(f"⚠️  [{datetime.now().strftime('%H:%M:%S')}] استجابة مراقبة غير طبيعية: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] خطأ في المراقبة: {e}")
            except Exception as e:
                print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] خطأ غير متوقع في المراقبة: {e}")
            
            # انتظر 10 دقائق قبل الطلب التالي
            time.sleep(600)  # 600 ثانية = 10 دقائق
    
    # تشغيل المراقبة في thread منفصل
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    print("🔄 بدء نظام المراقبة الذاتية (طلبات كل 10 دقائق)")

if __name__ == "__main__":
    print("🚀 بدء التشغيل الكامل على Render...")
    
    # تحديث حالة البوت
    bot_data["status"] = "🟢 يعمل - البوت والويب والمراقبة"
    
    # تشغيل Flask في thread منفصل
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # بدء نظام المراقبة الذاتية
    start_self_monitoring()
    
    # تشغيل البوت بعد تأخير بسيط لضمان تشغيل Flask أولاً
    time.sleep(5)
    
    # تشغيل البوت
    run_bot()
