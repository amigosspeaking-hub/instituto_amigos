import os
import pandas as pd
from flask import Flask, render_template_string, request, redirect, url_for, session, abort, render_template

app = Flask(__name__)
app.secret_key = 'instituto_amigos_ultra_secure_2026'

# رابط جوجل شيت الذي أرسلته
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdTMPVAfLN18RG6mLNXwycXhra4STzYPIiy7fvzCpeio0SfksLG4YNw78vA-djsSTG4rNSv2qdoXS8/pub?output=csv"

# الفهرس الكامل للمستويات
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
    <style>
        body { background: #f5f7fa; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin:0; }
        .card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #e52421; text-align: center; width: 350px; }
        h1 { color: #e52421; margin-bottom: 5px; font-size: 26px; }
        p { color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; text-align: center; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #e52421; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px; }
        .error { color: red; margin-bottom: 10px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Instituto Amigos 🇪🇸</h1>
        <p>منصة الطلاب التعليمية</p>
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
    <title>لوحة الطالب الذكية | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #e52421; --primary-dark: #c31e1b; --accent: #ffd100; --secondary: #008cba; --bg-body: #f8fafc; --text-main: #1e293b; --text-muted: #64748b; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }
        body { background-color: var(--bg-body); color: var(--text-main); padding: 30px 15px; }
        .container { max-width: 1100px; margin: 0 auto; }
        .main-header { background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%); color: white; padding: 35px; border-radius: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px rgba(229, 36, 33, 0.2); margin-bottom: 35px; }
        .user-profile { display: flex; align-items: center; gap: 20px; }
        .avatar-circle { width: 70px; height: 70px; background: var(--accent); color: #333; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 900; }
        .level-badge { background: rgba(255, 209, 0, 0.2); color: var(--accent); border: 2px solid var(--accent); padding: 8px 20px; border-radius: 50px; font-weight: 700; font-size: 16px; }
        .logout-btn { background: white; color: var(--primary); padding: 10px 22px; text-decoration: none; border-radius: 12px; font-weight: 700; font-size: 14px; transition: all 0.3s ease; margin-right: 10px; }
        .tabs-nav { display: flex; gap: 15px; margin-bottom: 30px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .tab-trigger { background: none; border: none; font-size: 18px; font-weight: 700; color: var(--text-muted); padding: 10px 20px; cursor: pointer; transition: all 0.3s; position: relative; }
        .tab-trigger.active { color: var(--primary); }
        .tab-trigger.active::after { content: ''; position: absolute; bottom: -12px; left: 0; width: 100%; height: 4px; background: var(--primary); border-radius: 10px; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
        .course-card { background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 15px rgba(0,0,0,0.04); border: 1px solid #f1f5f9; transition: all 0.3s ease; display: flex; flex-direction: column; }
        .card-banner { height: 120px; background: #e2e8f0; position: relative; display: flex; align-items: center; justify-content: center; }
        .placeholder-icon { font-size: 45px; color: var(--text-muted); }
        .lesson-tag { position: absolute; top: 15px; right: 15px; background: rgba(0,0,0,0.6); color: white; padding: 4px 12px; border-radius: 50px; font-size: 12px; font-weight: 700; }
        .card-body { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; }
        .card-body h4 { font-size: 18px; font-weight: 700; margin-bottom: 20px; color: var(--text-main); text-align: center; }
        .card-action-btn { display: block; text-align: center; background: var(--primary); color: white; padding: 12px; text-decoration: none; border-radius: 12px; font-weight: 700; font-size: 15px; margin-top: auto; transition: all 0.3s; }
        .course-card:hover .card-action-btn { background: var(--primary-dark); }
        .btn-exercise-color { background: var(--secondary); }
        .course-card:hover .btn-exercise-color { background: #007399; }
    </style>
</head>
<body>
    <div class="container">
        <header class="main-header">
            <div class="user-profile">
                <div class="avatar-circle">{{ student.username[0] | upper }}</div>
                <div class="user-info">
                    <h2>¡Hola, {{ student.username }}! 👋</h2>
                    <p>مرحباً بك في لوحتك التعليمية الفخمة</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="level-badge"><i class="fa-solid fa-graduation-cap"></i> المستوى: {{ student.level }}</div>
                <a href="/logout" class="logout-btn"><i class="fa-solid fa-sign-out-alt"></i> خروج</a>
            </div>
        </header>

        <nav class="tabs-nav">
            <button class="tab-trigger active" onclick="switchTab(event, 'lectures-tab')"><i class="fa-solid fa-book-open"></i> المحاضرات والدروس</button>
            <button class="tab-trigger" onclick="switchTab(event, 'exercises-tab')"><i class="fa-solid fa-pen-to-square"></i> التمارين والاختبارات</button>
        </nav>

        <div id="lectures-tab" class="tab-content active">
            <div class="cards-grid">
                {% for lesson in lessons %}
                <div class="course-card">
                    <div class="card-banner"><span class="lesson-tag">الدرس {{ loop.index }}</span><i class="fa-solid fa-book-bookmark placeholder-icon"></i></div>
                    <div class="card-body">
                        <h4>{{ lesson }}</h4>
                        <a href="/page/{{ student.level }}/lesson{{ loop.index }}.html" class="card-action-btn">ادخل لشرح المحاضرة <i class="fa-solid fa-chevron-left"></i></a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="exercises-tab" class="tab-content">
            <div class="cards-grid">
                {% for lesson in lessons %}
                <div class="course-card">
                    <div class="card-body" style="padding-top:35px;">
                        <div style="font-size: 40px; color: var(--secondary); margin-bottom: 15px; text-align: center;"><i class="fa-solid fa-star"></i></div>
                        <h4>🎯 تمرين: {{ lesson }}</h4>
                        <a href="/page/{{ student.level }}/exercise{{ loop.index }}.html" class="card-action-btn btn-exercise-color">ابدأ التقييم الفوري <i class="fa-solid fa-play"></i></a>
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
            error = "اسم المستخدم أو كلمة المرور غير صحيحة."
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    student = session['user']
    level = student['level']
    level_lessons = syllabus.get(level, ["الدرس 1", "الدرس 2", "الدرس 3", "الدرس 4"])
    return render_template_string(DASHBOARD_HTML, student=student, lessons=level_lessons)

@app.route('/page/<path:filename>')
def serve_page(filename):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    student = session['user']
    student_level = student['level']
    
    if not filename.startswith(student_level + "/"):
        abort(403)
        
    try:
        # تمرير بيانات الطالب لصفحات الـ HTML الفرعية
        return render_template(filename, student=student)
    except:
        abort(404)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)