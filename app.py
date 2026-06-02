import os
import pandas as pd
import random
from flask import Flask, render_template_string, request, redirect, url_for, session, abort, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'instituto_amigos_ultra_secure_2026')

# رابط جوجل شيت المباشر بصيغة CSV
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdTMPVAfLN18RG6mLNXwycXhra4STzYPIiy7fvzCpeio0SfksLG4YNw78vA-djsSTG4rNSv2qdoXS8/pub?output=csv"

# الفهرس الكامل للمستويات التعليمية
syllabus = {
    "A1.1": ["HOLA, ¿QUÉ TAL?", "EL ESPAÑOL Y YO", "TRABAJO AQUÍ", "¡ME GUSTAN LAS TAPAS!"],
    "A1.2": ["EN FAMILIA", "MI BARRIO", "MI DÍA A DÍA", "DE VACACIONES"],
    "A1.3": ["COMPRAR Y COMER EN ALICANTE", "¡BUEN FIN DE SEMANA!", "INTERCAMBIO DE CASA", "ESTA ES MI VIDA"],
    "A2.1": ["NUEVA ETAPA", "PARA TI Y PARA MÍ", "UN AÑO ESPECIAL", "CON TUS MANوس"],
    "A2.2": ["¿CÓMO ERA ANTES?", "¿Y QUÉ PASÓ?", "HOY COCINO YO", "¡ME SIENTO BIEN!"],
    "A2.3": ["TE INVITO", "UNA CIUDAD IDEAL", "NOSOTROS Y EL TRABAJO", "¡ESTAMOS AL DÍA!"],
    "B1.1": ["SEGUIMوس JUNTOS", "UN VIAJE INOLVIDABLE", "UN MUNDO MEJOR", "HABLANDO DEL FUTURO"],
    "B1.2": ["ENTRE NOSOTROS", "NUESTRO PLANETA", "¡CÁMARA, ACCIÓN!", "BUENO Y SANO"],
    "B1.3": ["MENSAJES CON EFECTO", "UN PASEO CULTURAL", "DE AQUÍ PARA ALLÁ", "UN MUNDO IMPRESIONANTE"],
    "B2.1": ["ASÍ HABLAMOS, ASÍ SOMOS", "LA ESCUELA DE LA VIDA", "NUEVOS MUNDوس LABORALES", "¡QUÉ ILUSIÓN!"],
    "B2.2": ["PEGADOS AL MÓVIL", "MENTE SANA EN CUERPO SANO", "¡HOGAR, DULCE HOGار!", "A FLOR DE PIEL"],
    "B2.3": ["LUGARES ESPECIALES", "ROMPIENDO ESQUEMAS", "¡NO TE QUEJES TANTO!", "MIRANDO HACIA ADELANTE"]
}

# عبارات تحفيزية
motivational_quotes = [
    "النجاح هو مجموع مجهودات صغيرة تتكرر كل يوم. استمر في تعلم الإسبانية!",
    "تعلم لغة جديدة هو امتلاك روح ثانية. أنت تبلي بلاءً حسناً!",
    "رحلة الألف ميل تبدأ بكلمة إسبانية واحدة. ابدأ دروسك اليوم!",
    "كل يوم تتعلم فيه شيئاً جديداً، تقترب خطوة من طموحك في Instituto Amigos.",
    "لا تتوقف حتى تصبح فخوراً بقدرتك على التحدث بطلاقة!"
]

def get_student_data(username, password):
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        df['username'] = df['username'].astype(str).str.strip()
        df['password'] = df['password'].astype(str).str.strip()
        df['level'] = df['level'].astype(str).str.strip()
        
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
    <title>تسجيل الدخول | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <style>
        body { 
            background: #fdfdfd; 
            background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url('https://www.transparenttextures.com/patterns/cubes.png');
            font-family: 'Cairo', sans-serif; 
            display: flex; align-items: center; justify-content: center; height: 100vh; margin:0; 
        }
        .card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border-top: 6px solid #e52421; text-align: center; width: 380px; position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(to right, #e52421, #ffd100, #e52421); }
        h1 { font-family: 'Montserrat', sans-serif; color: #e52421; margin-top: 10px; font-size: 28px; }
        p { color: #555; font-size: 15px; margin-bottom: 25px; }
        input { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #eee; border-radius: 10px; text-align: center; box-sizing: border-box; background: #fafafa; font-size: 15px; }
        button { width: 100%; padding: 14px; background: #e52421; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; margin-top: 10px; }
        button:hover { background: #c31e1b; transform: translateY(-2px); }
        .logo-login { width: 100px; margin-bottom: 10px; }
        .error { color: #e52421; margin-bottom: 15px; font-weight: bold; background: #ffebeb; padding: 10px; border-radius: 8px; font-size: 13px; }
    </style>
</head>
<body>
    <div class="card">
        <img src="https://i.ibb.co/L9p8qR7/logo.png" class="logo-login" alt="Logo">
        <h1>Instituto Amigos</h1>
        <p>مرحباً بك في بوابتك لتعلم الإسبانية</p>
        {% if error %} <div class="error">{{ error }}</div> {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="اسم المستخدم" required>
            <input type="password" name="password" placeholder="كلمة المرور" required>
            <button type="submit">دخول للمنصة</button>
        </form>
    </div>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة الطالب | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { 
            --primary: #e52421; 
            --primary-dark: #c31e1b; 
            --accent: #ffd100; 
            --secondary: #008cba; 
            --bg-body: #fdfdfd; 
            --text-main: #1e293b; 
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }
        
        body { 
            background-color: var(--bg-body); 
            /* خلفية خفيفة بألوان إسبانيا */
            background-image: 
                linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)),
                linear-gradient(to bottom, var(--primary) 0%, var(--primary) 15%, var(--accent) 15%, var(--accent) 85%, var(--primary) 85%, var(--primary) 100%);
            background-attachment: fixed;
            color: var(--text-main); 
            padding: 20px 15px; 
        }

        .container { max-width: 1100px; margin: 0 auto; position: relative; z-index: 1; }

        .main-header { 
            background: white; 
            color: var(--text-main); 
            padding: 25px; 
            border-radius: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            box-shadow: 0 5px 20px rgba(0,0,0,0.05); 
            margin-bottom: 25px;
            border-right: 8px solid var(--primary);
        }

        .institute-brand { display: flex; align-items: center; gap: 15px; }
        .institute-brand img { width: 60px; height: 60px; object-fit: contain; }
        .institute-brand h1 { font-family: 'Montserrat', sans-serif; font-size: 22px; color: var(--primary); }

        .user-profile { display: flex; align-items: center; gap: 15px; padding-right: 20px; border-right: 2px solid #eee; }
        .avatar-circle { width: 55px; height: 55px; background: var(--accent); color: #333; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; box-shadow: 0 4px 10px rgba(255, 209, 0, 0.3); }

        .motivation-banner {
            background: #fff9e6;
            border: 1px dashed var(--accent);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 15px;
            color: #856404;
            font-size: 15px;
            animation: fadeIn 1s ease;
        }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

        .level-badge { background: var(--primary); color: white; padding: 6px 15px; border-radius: 50px; font-weight: 700; font-size: 14px; }
        
        .logout-btn { color: #888; text-decoration: none; font-size: 18px; transition: 0.3s; margin-right: 15px; }
        .logout-btn:hover { color: var(--primary); }

        .tabs-nav { display: flex; gap: 10px; margin-bottom: 25px; background: white; padding: 8px; border-radius: 15px; width: fit-content; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
        .tab-trigger { border: none; font-size: 15px; font-weight: 700; color: #666; padding: 10px 20px; cursor: pointer; transition: 0.3s; border-radius: 10px; background: transparent; }
        .tab-trigger.active { background: var(--primary); color: white; }

        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .course-card { background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.03); transition: 0.3s; border: 1px solid #f0f0f0; display: flex; flex-direction: column; }
        .course-card:hover { transform: translateY(-5px); box-shadow: 0 12px 25px rgba(0,0,0,0.08); }
        
        .card-banner { height: 100px; background: #fafafa; display: flex; align-items: center; justify-content: center; position: relative; border-bottom: 1px solid #f9f9f9; }
        .placeholder-icon { font-size: 40px; color: #ddd; }
        .lesson-tag { position: absolute; top: 10px; right: 10px; background: var(--accent); color: #333; padding: 3px 10px; border-radius: 50px; font-size: 11px; font-weight: 800; }

        .card-body { padding: 20px; text-align: center; }
        .card-body h4 { font-size: 17px; margin-bottom: 15px; color: #333; height: 50px; display: flex; align-items: center; justify-content: center; }
        
        .card-action-btn { display: block; background: #f8f8f8; color: #444; padding: 12px; text-decoration: none; border-radius: 12px; font-weight: 700; font-size: 14px; transition: 0.3s; }
        .course-card:hover .card-action-btn { background: var(--primary); color: white; }

        .btn-exercise-color { color: var(--secondary); border: 1px solid var(--secondary); background: transparent; }
        .course-card:hover .btn-exercise-color { background: var(--secondary); color: white; }
    </style>
</head>
<body>
    <div class="container">
        <header class="main-header">
            <div class="institute-brand">
                <img src="https://i.ibb.co/L9p8qR7/logo.png" alt="Instituto Amigos">
                <div>
                    <h1>Instituto Amigos</h1>
                    <span class="level-badge">مستوى {{ student.level }}</span>
                </div>
            </div>

            <div class="user-profile">
                <div class="user-info" style="text-align: left; margin-left: 15px;">
                    <p style="font-size: 12px; color: #999;">مرحباً بك،</p>
                    <h2 style="font-size: 18px;">{{ student.username }}</h2>
                </div>
                <div class="avatar-circle">{{ student.username[0] | upper }}</div>
                <a href="/logout" class="logout-btn" title="تسجيل الخروج"><i class="fa-solid fa-right-from-bracket"></i></a>
            </div>
        </header>

        <div class="motivation-banner">
            <i class="fa-solid fa-lightbulb" style="font-size: 24px;"></i>
            <p><strong>نصيحة اليوم:</strong> {{ quote }}</p>
        </div>

        <nav class="tabs-nav">
            <button class="tab-trigger active" onclick="switchTab(event, 'lectures-tab')"><i class="fa-solid fa-play-circle"></i> المحاضرات</button>
            <button class="tab-trigger" onclick="switchTab(event, 'exercises-tab')"><i class="fa-solid fa-spell-check"></i> التمارين</button>
        </nav>

        <div id="lectures-tab" class="tab-content active" style="display: block;">
            <div class="cards-grid">
                {% for lesson in lessons %}
                <div class="course-card">
                    <div class="card-banner">
                        <span class="lesson-tag">Unidad {{ loop.index }}</span>
                        <i class="fa-solid fa-book placeholder-icon"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ lesson }}</h4>
                        <a href="/page/{{ student.level }}/lesson{{ loop.index }}.html" class="card-action-btn">مشاهدة الدرس <i class="fa-solid fa-arrow-left"></i></a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="exercises-tab" class="tab-content" style="display: none;">
            <div class="cards-grid">
                {% for lesson in lessons %}
                <div class="course-card">
                    <div class="card-body" style="padding-top:30px;">
                        <div style="font-size: 35px; color: var(--secondary); margin-bottom: 10px;"><i class="fa-solid fa-feather-pointed"></i></div>
                        <h4>{{ lesson }}</h4>
                        <a href="/page/{{ student.level }}/exercise{{ loop.index }}.html" class="card-action-btn btn-exercise-color">ابدأ التقييم <i class="fa-solid fa-pencil"></i></a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <script>
        function switchTab(evt, tabId) {
            const tabContents = document.getElementsByClassName("tab-content");
            for (let i = 0; i < tabContents.length; i++) tabContents[i].style.display = "none";
            const tabTriggers = document.getElementsByClassName("tab-trigger");
            for (let i = 0; i < tabTriggers.length; i++) tabTriggers[i].classList.remove("active");
            document.getElementById(tabId).style.display = "block";
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
            error = "اسم المستخدم أو كلمة المرور غير صحيحة."
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    student = session['user']
    level = student['level']
    level_lessons = syllabus.get(level, ["الدرس 1", "الدرس 2", "الدرس 3", "الدرس 4"])
    quote = random.choice(motivational_quotes)
    return render_template_string(DASHBOARD_HTML, student=student, lessons=level_lessons, quote=quote)

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
