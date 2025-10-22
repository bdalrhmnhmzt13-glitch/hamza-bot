# أضف هذا إلى بداية الكود
import requests
import threading

def advanced_monitor_system():
    """نظام مراقبة متقدم للنسخ المجانية"""
    
    def ping_network():
        while True:
            try:
                # عنوان تطبيقك على Render
                app_url = os.environ.get('RENDER_EXTERNAL_URL', '')
                
                if app_url:
                    # طلب إلى التطبيق نفسه
                    requests.get(f"{app_url}/api/ping", timeout=10)
                    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] تم إرسال طلب إحياء")
                
                # طلبات إلى خدمات خارجية للحفاظ على النشاط
                external_services = [
                    "https://www.google.com",
                    "https://httpbin.org/get",
                    "https://api.github.com"
                ]
                
                for service in external_services:
                    try:
                        requests.get(service, timeout=5)
                    except:
                        pass
                        
            except Exception as e:
                print(f"❌ خطأ في الإحياء: {e}")
            
            # انتظر 8 دقائق فقط (أقل من 15 دقيقة)
            time.sleep(480)
    
    # تشغيل النظام في thread منفصل
    monitor_thread = threading.Thread(target=ping_network, daemon=True)
    monitor_thread.start()
    print("🚀 نظام الإحياء المتقدم يعمل كل 8 دقائق")

# استدعاء النظام في main
if __name__ == "__main__":
    advanced_monitor_system()
    # باقي الكود...
