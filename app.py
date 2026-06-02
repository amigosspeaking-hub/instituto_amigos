import os
import pandas as pd
import random
from flask import Flask, render_template_string, request, redirect, url_for, session, abort, render_template

app = Flask(__name__)
# استخدام مفتاح سري ثابت، ويفضل دائماً قراءته من البيئة المحيطة Environment Variables في بيئة الإنتاج
app.secret_key = os.environ.get('SECRET_KEY', 'instituto_amigos_ultra_secure_2026')

# رابط جوجل شيت المباشر بصيغة CSV
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdTMPVAfLN18RG6mLNXwycXhra4STzYPIiy7fvzCpeio0SfksLG4YNw78vA-djsSTG4rNSv2qdoXS8/pub?output=csv"

# الفهرس الكامل للمستويات التعليمية
syllabus = {
    "A1.1": ["HOLA, ¿QUÉ TAL?", "EL ESPAÑOL Y YO", "TRABAJO AQUÍ", "¡ME GUSTAN LAS TAPAS!"],
    "A1.2": ["EN FAMILIA", "MI BARRIO", "MI DÍA A DÍA", "DE VACACIONES"],
    "A1.3": ["COMPRAR Y COMER EN ALICANTE", "¡BUEN FIN DE SEMANA!", "INTERCAMBIO DE CASA", "ESTA ES MI VIDA"],
    "A2.1": ["NUEVA ETAPA", "PARA TI Y PARA MÍ", "UN AÑO ESPECIAL", "CON TUS MANOS"],
    "A2.2": ["¿CÓMO ERA ANTES?", "¿Y QUÉ PASÓ?", "HOY COCINO YO", "¡ME SIENTO BIEN!"],
    "A2.3": ["TE INVITO", "UNA CIUDAD IDEAL", "NOSOTROS Y EL TRABAJO", "¡ESTAMOS AL DÍA!"],
    "B1.1": ["SEGUIMOS JUNTOS", "UN VIAJE INOLVIDABLE", "UN MUNDO MEJOR", "HABLANDO DEL FUTURO"],
    "B1.2": ["ENTRE NOSOTROS", "NUESTRO PLANETA", "¡CÁMARA, ACCIÓN!", "BUENO Y SANO"],
    "B1.3": ["MENSAJES CON EFECTO", "UN PASEO CULTURAL", "DE AQUÍ PARA ALLÁ", "UN MUNDO IMPRESIONANTE"],
    "B2.1": ["ASÍ HABLAMOS, ASÍ SOMOS", "LA ESCUELA DE LA VIDA", "NUEVOS MUNDOS LABORALES", "¡QUÉ ILUSIÓN!"],
    "B2.2": ["PEGADOS AL MÓVIL", "MENTE SANA EN CUERPO SANO", "¡HOGAR, DULCE HOGAR!", "A FLOR DE PIEL"],
    "B2.3": ["LUGARES ESPECIALES", "ROMPIENDO ESQUEMAS", "¡NO TE QUEJES TANTO!", "MIRANDO HACIA ADELANTE"]
}

# جمل تحفيزية بالمصري
motivation_quotes = [
    "شد حيلك يا بطل، الإسباني محتاج استمرارية بس!",
    "كل يوم ربع ساعة مذاكرة بتعمل فرق كبير.. كمل!",
    "احنا وراك لحد ما تبقى فل في اللغة.. يالا بينا!",
    "تعب النهاردة هو نجاح بكرة.. متكسلش عن درس النهاردة!"
]

def get_student_data(username, password):
    try:
        # قراءة البيانات كنصوص بشكل إجباري لحل مشكلة عدم الدخول
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL, dtype=str)
        # ملء الخانات الفارغة لتجنب أخطاء المقارنة
        df.fillna('', inplace=True)
        
        df.columns = df.columns.str.strip()
        df['username'] = df['username'].str.strip()
        df['password'] = df['password'].str.strip()
        df['level'] = df['level'].str.strip()
        
        user_row = df[(df['username'] == str(username).strip()) & (df['password'] == str(password).strip())]
        if not user_row.empty:
            return user_row.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error checking Google Sheet: {e}")
        return None

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>يالا بينا.. دخول | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Reenie+Beanie&display=swap" rel="stylesheet">
    <style>
        :root { --primary-red: #e52421; --primary-gold: #ffd100; }
        body { 
            background: #fdfcf5; 
            background-image: url('https://www.transparenttextures.com/patterns/lined-paper.png');
            font-family: 'Cairo', sans-serif; 
            display: flex; align-items: center; justify-content: center; height: 100vh; margin:0; 
            overflow: hidden;
            position: relative;
        }
        /* تنسيق الرسومات اليدوية */
        .spain-doodle { position: absolute; z-index: 0; opacity: 0.8; }
        .doodle-1 { top: 15%; left: 10%; width: 120px; animation: float 6s ease-in-out infinite; }
        .doodle-2 { bottom: 15%; right: 10%; width: 140px; transform: rotate(15deg); animation: float 5s ease-in-out infinite reverse; }
        
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-15px) rotate(5deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        .card { 
            background: white; padding: 40px; border-radius: 15px; 
            box-shadow: 5px 5px 0px rgba(0,0,0,0.05); 
            border: 3px solid #333; 
            text-align: center; width: 360px; position: relative; z-index: 1;
        }
        
        .logo-img { width: 120px; height: auto; margin-bottom: 15px; }
        
        h1 { color: #333; margin-bottom: 5px; font-size: 24px; font-weight: 700; }
        p.subtitle { color: #666; font-size: 14px; margin-bottom: 25px; }
        
        .input-group { position: relative; margin: 15px 0; }
        input { 
            width: 100%; padding: 12px; border: 2px solid #333; border-radius: 8px; 
            text-align: center; box-sizing: border-box; font-size: 15px;
            font-family: 'Cairo', sans-serif;
            background: #fff;
            transition: all 0.2s;
        }
        input:focus { border-color: var(--primary-red); outline: none; box-shadow: 3px 3px 0px rgba(229, 36, 33, 0.2); }
        
        button { 
            width: 100%; padding: 12px; background: var(--primary-red); color: white; 
            border: 2px solid #333; border-radius: 8px; font-weight: bold; cursor: pointer; 
            font-size: 16px; font-family: 'Cairo', sans-serif; transition: all 0.2s;
            margin-top: 10px;
            box-shadow: 3px 3px 0px #333;
        }
        button:hover { transform: translate(-2px, -2px); box-shadow: 5px 5px 0px #333; }
        button:active { transform: translate(1px, 1px); box-shadow: 1px 1px 0px #333; }

        .error { 
            color: var(--primary-red); margin-bottom: 15px; font-size: 13px; font-weight: bold;
            background: #ffebeb; padding: 8px; border-radius: 5px; border: 1px solid var(--primary-red);
        }
        .handwritten-noto { font-family: 'Reenie Beanie', cursive; font-size: 24px; color: #888; margin-top: 15px; }
    </style>
</head>
<body>
    <svg viewBox="0 0 100 100" class="spain-doodle doodle-1">
      <circle cx="50" cy="50" r="20" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" fill="none" />
      <line x1="50" y1="10" x2="50" y2="22" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" stroke-linecap="round"/>
      <line x1="50" y1="78" x2="50" y2="90" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" stroke-linecap="round"/>
      <line x1="10" y1="50" x2="22" y2="50" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" stroke-linecap="round"/>
      <line x1="78" y1="50" x2="90" y2="50" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" stroke-linecap="round"/>
      <line x1="22" y1="22" x2="30" y2="30" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" stroke-linecap="round"/>
      <line x1="78" y1="78" x2="70" y2="70" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" stroke-linecap="round"/>
      <line x1="22" y1="78" x2="30" y2="70" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" stroke-linecap="round"/>
      <line x1="78" y1="22" x2="70" y2="30" stroke="rgba(229, 36, 33, 0.4)" stroke-width="4" stroke-linecap="round"/>
    </svg>

    <svg viewBox="0 0 100 100" class="spain-doodle doodle-2">
      <path d="M30 70 C20 80, 10 70, 20 60 C30 50, 40 60, 50 50 C60 40, 70 30, 80 20 L85 25 C75 35, 65 45, 55 55 C45 65, 35 75, 30 70 Z" stroke="rgba(255, 209, 0, 0.6)" stroke-width="3" fill="none" stroke-linejoin="round"/>
      <circle cx="35" cy="65" r="8" stroke="rgba(255, 209, 0, 0.6)" stroke-width="3" fill="none"/>
      <line x1="35" y1="65" x2="80" y2="20" stroke="rgba(255, 209, 0, 0.6)" stroke-width="2"/>
    </svg>

    <div class="card">
        <img src="/static/assets/logo.png" alt="Instituto Amigos Logo" class="logo-img" onerror="this.style.display='none'">
        
        <h1>بوابتك للأسباني 👋</h1>
        <p class="subtitle">اكتب بياناتك ويالا بينا ع المنصة التعليمية</p>
        
        {% if error %} <div class="error">{{ error }}</div> {% endif %}
        
        <form method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="اسم المستخدم بتاعك" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="كلمة المرور" required>
            </div>
            <button type="submit">ادخل للمنصة <i class="fa-solid fa-arrow-left"></i></button>
        </form>
        <div class="handwritten-noto">¡Vamos a estudiar!</div>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحتك التعليمية | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { 
            --primary: #e52421; 
            --primary-dark: #c31e1b; 
            --accent: #ffd100; 
            --accent-hover: #ffdf4d;
            --secondary: #2c3e50; 
            --bg-body: #f4f7f6; 
            --text-main: #1e293b; 
            --text-muted: #64748b; 
            --shadow-sm: 0 2px 8px rgba(0,0,0,0.06);
            --shadow-md: 0 10px 25px rgba(0,0,0,0.08);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }
        body { background-color: var(--bg-body); color: var(--text-main); padding: 0; margin: 0; }
        
        .top-nav {
            background: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center;
            box-shadow: var(--shadow-sm); position: sticky; top: 0; z-index: 100;
        }
        .brand-area { display: flex; align-items: center; gap: 15px; }
        .brand-area img { width: 50px; height: auto; border-radius: 50%; border: 2px solid var(--accent); }
        .brand-area h1 { font-size: 18px; font-weight: 900; color: var(--secondary); }
        .brand-area h1 span { color: var(--primary); }

        .user-actions { display: flex; align-items: center; gap: 15px; }
        .level-tag { background: #eef2f5; color: var(--secondary); padding: 8px 15px; border-radius: 50px; font-size: 13px; font-weight: 700; border: 1px solid #d1d9e0; }
        .logout-btn { color: var(--text-muted); text-decoration: none; font-size: 14px; font-weight: 600; transition: color 0.2s; }
        .logout-btn:hover { color: var(--primary); }

        .main-content { max-width: 1200px; margin: 30px auto; padding: 0 15px; }
        
        .welcome-section {
            background: linear-gradient(135deg, var(--secondary) 0%, #1a2530 100%);
            color: white; padding: 40px; border-radius: 24px;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: var(--shadow-md); margin-bottom: 35px;
            position: relative; overflow: hidden;
        }
        .welcome-section::before {
            content: '¡Hola!'; position: absolute; font-size: 150px; font-weight: 900;
            color: rgba(255,255,255,0.03); bottom: -30px; left: -20px;
        }
        .user-welcome-info h2 { font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        .user-welcome-info p { font-size: 16px; color: rgba(255,255,255,0.8); max-width: 500px; }
        
        .motivation-box {
            background: rgba(255, 209, 0, 0.15); border: 1px solid var(--accent);
            color: var(--accent); padding: 20px; border-radius: 16px; text-align: center;
            width: 300px; backdrop-filter: blur(5px); z-index: 1;
        }
        .motivation-box i { font-size: 24px; margin-bottom: 10px; display: block; }
        .motivation-box p { font-size: 14px; font-weight: 700; line-height: 1.5; color: white; }

        .tabs-nav { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .tab-trigger { 
            background: none; border: none; font-size: 16px; font-weight: 700; color: var(--text-muted); 
            padding: 10px 25px; cursor: pointer; transition: all 0.3s; border-radius: 12px;
        }
        .tab-trigger:hover { background: rgba(0,0,0,0.03); color: var(--secondary); }
        .tab-trigger.active { background: var(--primary); color: white; box-shadow: var(--shadow-sm); }

        .tab-content { display: none; }
        .tab-content.active { display: block; animation: fadeIn 0.4s ease; }

        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
        
        .course-card { 
            background: white; border-radius: 20px; overflow: hidden; 
            box-shadow: var(--shadow-sm); border: 1px solid #f0f3f5; 
            transition: all 0.3s ease; display: flex; flex-direction: column; 
        }
        .course-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-md); border-color: #d1d9e0; }

        .card-header { 
            padding: 20px; background: #fafbfc; border-bottom: 1px solid #eee;
            display: flex; align-items: center; justify-content: space-between;
        }
        .lesson-number { font-size: 13px; font-weight: 800; color: var(--primary); background: rgba(229, 36, 33, 0.1); padding: 5px 12px; border-radius: 50px; }
        .lesson-icon { font-size: 20px; color: var(--text-muted); }

        .card-body { padding: 25px 30px; text-align: center; flex-grow: 1; display: flex; flex-direction: column; justify-content: center; }
        .card-body h4 { font-size: 18px; font-weight: 800; color: var(--secondary); margin-bottom: 10px; line-height: 1.4; height: 50px; display: flex; align-items: center; justify-content: center; }
        .card-body p { font-size: 13px; color: var(--text-muted); margin-bottom: 25px; }

        .card-action-btn { 
            display: inline-flex; align-items: center; justify-content: center; gap: 8px;
            width: 100%; text-align: center; 
            padding: 14px; text-decoration: none; border-radius: 12px; 
            font-weight: 700; font-size: 15px; transition: all 0.2s ease; 
        }
        .btn-lecture { background: var(--primary); color: white; }
        .btn-lecture:hover { background: var(--primary-dark); }
        
        .btn-exercise { background: var(--accent); color: var(--secondary); }
        .btn-exercise:hover { background: var(--accent-hover); }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="brand-area">
            <img src="/static/assets/logo.png" alt="Instituto Amigos Logo" onerror="this.style.display='none'">
            <h1>Instituto <span>Amigos</span></h1>
        </div>
        <div class="user-actions">
            <span class="level-tag"><i class="fa-solid fa-graduation-cap"></i> مستواك: {{ student.level }}</span>
            <a href="/logout" class="logout-btn"><i class="fa-solid fa-sign-out-alt"></i> خروج</a>
        </div>
    </nav>

    <div class="main-content">
        <header class="welcome-section">
            <div class="user-welcome-info">
                <h2>منور يا {{ student.username }}!</h2>
                <p>يالا بينا نشد حيلنا النهاردة ع المذاكرة.. الإسباني مستنيك يا بطل!</p>
            </div>
            <div class="motivation-box">
                <i class="fa-solid fa-lightbulb"></i>
                <p>{{ quote }}</p>
            </div>
        </header>

        <nav class="tabs-nav">
            <button class="tab-trigger active" onclick="switchTab(event, 'lectures-tab')"><i class="fa-solid fa-video"></i> المحاضرات والشرح</button>
            <button class="tab-trigger" onclick="switchTab(event, 'exercises-tab')"><i class="fa-solid fa-pen-ruler"></i> التمارين والتقييم</button>
        </nav>

        <div id="lectures-tab" class="tab-content active">
            <div class="cards-grid">
                {% for lesson in lessons %}
                <div class="course-card">
                    <div class="card-header">
                        <span class="lesson-number">Unidad {{ loop.index }}</span>
                        <i class="fa-solid fa-book-open lesson-icon"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ lesson }}</h4>
                        <p>ادخل وشوف شرح المحاضرة دي بالتفصيل يا بطل.</p>
                        <a href="/page/{{ student.level }}/lesson{{ loop.index }}.html" class="card-action-btn btn-lecture">ابدأ الشرح <i class="fa-solid fa-play-circle"></i></a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="exercises-tab" class="tab-content">
            <div class="cards-grid">
                {% for lesson in lessons %}
                <div class="course-card">
                    <div class="card-header">
                        <span class="lesson-number">Ejercicio {{ loop.index }}</span>
                        <i class="fa-solid fa-star lesson-icon" style="color: var(--accent);"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ lesson }}</h4>
                        <p>تمرين سريع على المحاضرة عشان تثبت المعلومة في دماغك.</p>
                        <a href="/page/{{ student.level }}/exercise{{ loop.index }}.html" class="card-action-btn btn-exercise">ابدأ التمرين <i class="fa-solid fa-pencil"></i></a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <script>
        function switchTab(evt, tabId) {
            const tabContents = document.getElementsByClassName("tab-content");
            for (let i = 0; i < tabContents.length; i++) tabContents[i].classList.remove("active");
            
            const tabTriggers = document.getElementsByClassName("tab-trigger");
            for (let i = 0; i < tabTriggers.length; i++) tabTriggers[i].classList.remove("active");
            
            document.getElementById(tabId).classList.add("active");
            evt.currentTarget.classList.add("active");
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        student = get_student_data(username, password)
        if student:
            session['user'] = student
            return redirect(url_for('dashboard'))
        else:
            error = "اسم المستخدم أو الباسورد غلط.. جرب تاني!"
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    student = session['user']
    level = student['level']
    level_lessons = syllabus.get(level, ["Unidad 1", "Unidad 2", "Unidad 3", "Unidad 4"])
    
    random_quote = random.choice(motivation_quotes)
    
    return render_template_string(DASHBOARD_HTML, student=student, lessons=level_lessons, quote=random_quote)

@app.route('/page/<path:filename>')
def serve_page(filename):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    student = session['user']
    student_level = student['level']
    
    if not filename.startswith(student_level + "/"):
        abort(403)
        
    try:
        return render_template(filename, student=student)
    except Exception as e:
        print(f"Template load error: {e}")
        abort(404)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/healthz')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
