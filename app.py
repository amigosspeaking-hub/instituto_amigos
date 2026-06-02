import os
import pandas as pd
import random
from flask import Flask, render_template_string, request, redirect, url_for, session, abort, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'instituto_amigos_ultra_secure_2026')

GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdTMPVAfLN18RG6mLNXwycXhra4STzYPIiy7fvzCpeio0SfksLG4YNw78vA-djsSTG4rNSv2qdoXS8/pub?output=csv"

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

# الجمل التحفيزية الجديدة (بدون إنجليزي وبدون جملة البلبل)
motivation_quotes = [
    "عاش يا بطل، الاستمرارية هي سر النجاح في أي لغة.",
    "كل درس بتخلصه بيقربك خطوة لحلمك، كمل وماتوقفش!",
    "المذاكرة النهاردة هي طلاقتك بكرة، شد حيلك!",
    "مافيش حاجة صعبة على واحد بيحاول كل يوم، إحنا واثقين فيك!",
    "خطوة بخطوة هتوصل، المهم تفضل مكمل على نفس الحماس.",
    "تعبك النهاردة هترتاح بيه بكرة، ركز في درسك واعمل اللي عليك.",
    "رحلة الألف ميل بتبدأ بخطوة، وأنت قطعت شوط كبير.. استمر!"
]

def get_student_data(username, password):
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL, dtype=str)
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary-red: #e52421; --primary-gold: #ffd100; }
        body { 
            background: #fcfbf7; 
            font-family: 'Cairo', sans-serif; 
            display: flex; align-items: center; justify-content: center; height: 100vh; margin:0; 
            overflow: hidden; position: relative;
        }
        
        /* تصميم الأشكال المرسومة والخلفيات الثقافية */
        .doodle-container {
            position: absolute; display: flex; flex-direction: column; align-items: center;
            opacity: 0.65; z-index: 0; color: #333;
        }
        .doodle-container i { font-size: 38px; margin-bottom: 5px; color: #444; }
        .doodle-container span { font-family: 'Reenie Beanie', cursive; font-size: 28px; font-weight: bold; color: var(--primary-red); }
        
        /* توزيع الأشكال على الشاشة */
        .d-1 { top: 12%; left: 15%; animation: float 6s ease-in-out infinite; transform: rotate(-10deg); }
        .d-2 { bottom: 15%; right: 15%; animation: float 5s ease-in-out infinite reverse; transform: rotate(15deg); }
        .d-3 { bottom: 15%; left: 15%; animation: float 7s ease-in-out infinite; transform: rotate(-8deg); }
        .d-4 { top: 15%; right: 15%; animation: float 8s ease-in-out infinite; transform: rotate(12deg); }
        .d-5 { top: 45%; left: 8%; transform: rotate(-15deg); opacity: 0.4; }
        .d-6 { top: 50%; right: 8%; transform: rotate(12deg); opacity: 0.4; }

        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-12px) rotate(3deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        .card { 
            background: white; padding: 40px; border-radius: 15px; 
            box-shadow: 5px 5px 0px rgba(0,0,0,0.05); 
            border: 3px solid #333; 
            text-align: center; width: 380px; position: relative; z-index: 1;
        }
        
        .logo-img { width: 120px; height: auto; margin-bottom: 10px; border-radius: 50%; border: 3px solid var(--primary-gold); }
        h1 { color: #333; margin-bottom: 5px; font-size: 24px; font-weight: 700; }
        p.subtitle { color: #666; font-size: 14px; margin-bottom: 25px; }
        
        .input-group { position: relative; margin: 15px 0; }
        input { 
            width: 100%; padding: 12px; border: 2px solid #333; border-radius: 8px; 
            text-align: center; box-sizing: border-box; font-size: 15px;
            font-family: 'Cairo', sans-serif; transition: all 0.2s;
        }
        input:focus { border-color: var(--primary-red); outline: none; box-shadow: 3px 3px 0px rgba(229, 36, 33, 0.2); }
        
        button { 
            width: 100%; padding: 12px; background: var(--primary-red); color: white; 
            border: 2px solid #333; border-radius: 8px; font-weight: bold; cursor: pointer; 
            font-size: 16px; font-family: 'Cairo', sans-serif; transition: all 0.2s;
            margin-top: 10px; box-shadow: 3px 3px 0px #333;
        }
        button:hover { transform: translate(-2px, -2px); box-shadow: 5px 5px 0px #333; }
        
        .error { color: var(--primary-red); margin-bottom: 15px; font-size: 13px; font-weight: bold; background: #ffebeb; padding: 8px; border-radius: 5px; border: 1px solid var(--primary-red); }
        
        /* أزرار السوشيال ميديا في صفحة الدخول */
        .social-links { margin-top: 25px; display: flex; justify-content: center; gap: 15px; }
        .social-btn {
            display: inline-flex; align-items: center; justify-content: center;
            width: 40px; height: 40px; border-radius: 50%; color: white; text-decoration: none;
            font-size: 18px; transition: 0.3s; border: 2px solid #333; box-shadow: 2px 2px 0px #333;
        }
        .social-btn:hover { transform: translateY(-3px); box-shadow: 4px 4px 0px #333; }
        .fb { background: #1877F2; }
        .ig { background: #E4405F; }
        .tt { background: #000000; }
        .wa { background: #25D366; }
    </style>
</head>
<body>
    <!-- أشكال الثقافة واللغة -->
    <div class="doodle-container d-1">
        <i class="fa-regular fa-sun"></i>
        <span>Sol</span>
    </div>
    
    <div class="doodle-container d-2">
        <i class="fa-solid fa-guitar"></i>
        <span>Música</span>
    </div>

    <div class="doodle-container d-3">
        <i class="fa-solid fa-pepper-hot"></i>
        <span>Picante</span>
    </div>

    <div class="doodle-container d-4">
        <i class="fa-regular fa-comment-dots"></i>
        <span>¡Hola!</span>
    </div>

    <div class="doodle-container d-5">
        <span style="font-size: 35px; color: #333;">Familia</span>
    </div>

    <div class="doodle-container d-6">
        <span style="font-size: 35px; color: #333;">Gracias</span>
    </div>

    <div class="card">
        <img src="/static/assets/logo.png" alt="Instituto Amigos Logo" class="logo-img" onerror="this.src='https://ui-avatars.com/api/?name=IA&background=ffd100&color=e52421&size=120'">
        
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

        <div class="social-links">
            <a href="https://www.facebook.com/institutoamigos1" target="_blank" class="social-btn fb" title="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="https://www.instagram.com/instituto_amigos1/" target="_blank" class="social-btn ig" title="Instagram"><i class="fab fa-instagram"></i></a>
            <a href="https://www.tiktok.com/@espanolconamigos" target="_blank" class="social-btn tt" title="TikTok"><i class="fab fa-tiktok"></i></a>
            <a href="https://wa.me/+201108425280" target="_blank" class="social-btn wa" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        </div>
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
    <title>لوحتك التعليمية | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { 
            --primary: #e52421; --primary-dark: #c31e1b; 
            --accent: #ffd100; --secondary: #2c3e50; 
            --bg-body: #f4f7f6; --text-main: #1e293b; --text-muted: #64748b; 
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }
        body { background-color: var(--bg-body); color: var(--text-main); }
        
        /* الشريط العلوي */
        .top-nav {
            background: white; padding: 12px 30px; display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06); position: sticky; top: 0; z-index: 100;
        }
        .brand-area { display: flex; align-items: center; gap: 15px; }
        .brand-area img { width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid var(--accent); }
        .brand-area h1 { font-size: 18px; font-weight: 900; color: var(--secondary); margin: 0; }
        .brand-area h1 span { color: var(--primary); }

        /* منطقة اليسار (السوشيال + الأزرار) - تنسيق جديد وواسع */
        .top-left-container { display: flex; align-items: center; gap: 25px; }
        
        /* السوشيال ميديا */
        .social-icons { display: flex; gap: 12px; align-items: center; }
        .social-icons a {
            display: flex; align-items: center; justify-content: center;
            width: 36px; height: 36px; border-radius: 50%;
            background: #f0f3f5; color: var(--text-muted); text-decoration: none;
            font-size: 16px; transition: all 0.3s ease;
        }
        .social-icons a:hover { background: var(--primary); color: white; transform: translateY(-2px); }
        
        /* الخط الفاصل */
        .v-divider { width: 2px; height: 30px; background-color: #e2e8f0; }

        /* أزرار المستخدم */
        .user-buttons { display: flex; align-items: center; gap: 15px; }
        .level-badge { background: #eef2f5; color: var(--secondary); padding: 8px 18px; border-radius: 50px; font-size: 13px; font-weight: 700; border: 1px solid #d1d9e0; }
        .logout-btn { 
            display: flex; align-items: center; gap: 8px;
            background: #ffebeb; color: var(--primary); padding: 8px 18px; border-radius: 8px; 
            text-decoration: none; font-size: 14px; font-weight: 700; transition: 0.3s; 
        }
        .logout-btn:hover { background: var(--primary); color: white; }

        .main-content { max-width: 1200px; margin: 30px auto; padding: 0 15px; }
        
        .welcome-section {
            background: linear-gradient(135deg, var(--secondary) 0%, #1a2530 100%);
            color: white; padding: 40px; border-radius: 24px;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08); margin-bottom: 35px; overflow: hidden; position: relative;
        }
        .user-welcome-info h2 { font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        .user-welcome-info p { font-size: 16px; color: rgba(255,255,255,0.8); max-width: 500px; }
        
        .motivation-box {
            background: rgba(255, 209, 0, 0.15); border: 1px solid var(--accent);
            color: var(--accent); padding: 20px; border-radius: 16px; text-align: center;
            width: 300px; backdrop-filter: blur(5px); z-index: 1;
        }

        .tabs-nav { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .tab-trigger { background: none; border: none; font-size: 16px; font-weight: 700; color: var(--text-muted); padding: 10px 25px; cursor: pointer; transition: 0.3s; border-radius: 12px; }
        .tab-trigger.active { background: var(--primary); color: white; }

        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
        .course-card { background: white; border-radius: 20px; overflow: hidden; border: 1px solid #f0f3f5; transition: 0.3s; display: flex; flex-direction: column; }
        .course-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .card-header { padding: 20px; background: #fafbfc; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
        .lesson-number { font-size: 13px; font-weight: 800; color: var(--primary); background: rgba(229, 36, 33, 0.1); padding: 5px 12px; border-radius: 50px; }
        .card-body { padding: 25px 30px; text-align: center; flex-grow: 1; }
        .card-body h4 { font-size: 18px; font-weight: 800; color: var(--secondary); margin-bottom: 25px; }
        .card-action-btn { display: block; width: 100%; padding: 14px; text-decoration: none; border-radius: 12px; font-weight: 700; font-size: 15px; transition: 0.2s; }
        .btn-lecture { background: var(--primary); color: white; }
        .btn-exercise { background: var(--accent); color: var(--secondary); }
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="brand-area">
            <img src="/static/assets/logo.png" alt="Logo" onerror="this.src='https://ui-avatars.com/api/?name=IA&background=ffd100&color=e52421'">
            <h1>Instituto <span>Amigos</span></h1>
        </div>
        
        <div class="top-left-container">
            <div class="social-icons">
                <a href="https://www.facebook.com/institutoamigos1" target="_blank" title="Facebook"><i class="fab fa-facebook-f"></i></a>
                <a href="https://www.instagram.com/instituto_amigos1/" target="_blank" title="Instagram"><i class="fab fa-instagram"></i></a>
                <a href="https://www.tiktok.com/@espanolconamigos" target="_blank" title="TikTok"><i class="fab fa-tiktok"></i></a>
                <a href="https://wa.me/+201108425280" target="_blank" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
            </div>
            
            <div class="v-divider"></div>
            
            <div class="user-buttons">
                <span class="level-badge"><i class="fa-solid fa-graduation-cap"></i> مستواك: {{ student.level }}</span>
                <a href="/logout" class="logout-btn">خروج <i class="fa-solid fa-arrow-right-from-bracket"></i></a>
            </div>
        </div>
    </nav>

    <div class="main-content">
        <header class="welcome-section">
            <div class="user-welcome-info">
                <h2>أهلاً بيك يا {{ student.username }}! 👋</h2>
                <p>جاهز لدرس النهاردة؟ كمل في طريقك وإحنا في ضهرك دايماً!</p>
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
                        <i class="fa-solid fa-book-open" style="color: #888;"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ lesson }}</h4>
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
                        <span class="lesson-number" style="color: var(--secondary);">Ejercicio {{ loop.index }}</span>
                        <i class="fa-solid fa-star" style="color: var(--accent);"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ lesson }}</h4>
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
