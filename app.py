import os
import pandas as pd
import random
import json
from flask import Flask, render_template_string, request, redirect, url_for, session, abort, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'instituto_amigos_ultra_secure_2026')

# رابط جوجل شيت المباشر بصيغة CSV
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdTMPVAfLN18RG6mLNXwycXhra4STzYPIiy7fvzCpeio0SfksLG4YNw78vA-djsSTG4rNSv2qdoXS8/pub?output=csv"

# 1. الفهرس الكامل للمستويات التعليمية
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

# 2. روابط جداول المذاكرة من GitHub حسب المستوى (بتتفتح في شاشة تانية)
SCHEDULE_DATA = {
    "A1.1": "https://yourusername.github.io/your-repo/schedules/a1_1.html",
    "A1.2": "https://yourusername.github.io/your-repo/schedules/a1_2.html",
    "A1.3": "https://yourusername.github.io/your-repo/schedules/a1_3.html",
    "A2.1": "https://yourusername.github.io/your-repo/schedules/a2_1.html",
    "A2.2": "https://yourusername.github.io/your-repo/schedules/a2_2.html",
    "A2.3": "https://yourusername.github.io/your-repo/schedules/a2_3.html",
    "B1.1": "https://yourusername.github.io/your-repo/schedules/b1_1.html",
    "B1.2": "https://yourusername.github.io/your-repo/schedules/b1_2.html",
    "B1.3": "https://yourusername.github.io/your-repo/schedules/b1_3.html",
    "B2.1": "https://yourusername.github.io/your-repo/schedules/b2_1.html",
    "B2.2": "https://yourusername.github.io/your-repo/schedules/b2_2.html",
    "B2.3": "https://yourusername.github.io/your-repo/schedules/b2_3.html"
}

# 3. روابط الألعاب من GitHub حسب المستوى (بتتفتح في شاشة تانية)
GAMES_DATA = {
    "A1.1": "https://yourusername.github.io/your-repo/games/a1_1.html",
    "A1.2": "https://yourusername.github.io/your-repo/games/a1_2.html",
    "A1.3": "https://yourusername.github.io/your-repo/games/a1_3.html",
    "A2.1": "/page/A2.1/juego-estudiante1.htm",
    "A2.2": "https://yourusername.github.io/your-repo/games/a2_2.html",
    "A2.3": "https://yourusername.github.io/your-repo/games/a2_3.html",
    "B1.1": "https://yourusername.github.io/your-repo/games/b1_1.html",
    "B1.2": "https://yourusername.github.io/your-repo/games/b1_2.html",
    "B1.3": "https://yourusername.github.io/your-repo/games/b1_3.html",
    "B2.1": "https://yourusername.github.io/your-repo/games/b2_1.html",
    "B2.2": "https://yourusername.github.io/your-repo/games/b2_2.html",
    "B2.3": "https://yourusername.github.io/your-repo/games/b2_3.html"
}

# 4. مكتبة فيديوهات اليوتيوب مقسمة تلقائياً حسب كل مستوى فرعي
VIDEOS_DATA = {
    "A1.1": [
        {"title": "مراجعة قواعد النطق الأساسية والأبجدية", "youtube_id": "dQw4w9WgXcQ"},
        {"title": "أدوات التعريف والتنكير في الإسبانية", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "A1.2": [
        {"title": "شرح مفردات العائلة والأقارب بالتفصيل", "youtube_id": "dQw4w9WgXcQ"},
        {"title": "الأفعال الروتينية اليومية وتصريفها", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "A1.3": [
        {"title": "كيف تتسوق وتطلب الطعام داخل المطعم", "youtube_id": "dQw4w9WgXcQ"},
        {"title": "وصف الأماكن والاتجاهات داخل المدينة", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "A2.1": [
        {"title": "Un día muy especial", "youtube_id": "7dgZvDijGP0"},
        {"title": "Soy un manitas", "youtube_id": "fnC6LeUHcq0"}
    ],
    "A2.2": [
        {"title": "استخدامات زمن الماضي المستمر لوصف الطفولة", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "A2.3": [
        {"title": "صيغ الأمر والطلب بطريقة مهذبة", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "B1.1": [
        {"title": "قواعد التعبير عن المستقبل والخطط البعيدة", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "B1.2": [
        {"title": "تعبيرات النقاش وإبداء الرأي الشخصي بحرية", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "B1.3": [
        {"title": "روابط الجمل المتقدمة وكتابة المقالات", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "B2.1": [
        {"title": "التعمق في صيغ الشك والاحتمالية الصعبة", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "B2.2": [
        {"title": "مصطلحات تقنية متقدمة لإدارة حوار عملي", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "B2.3": [
        {"title": "مراجعة شاملة لإتقان المحادثة السريعة والطلاقة", "youtube_id": "dQw4w9WgXcQ"}
    ]
}

# 5. مواضيع عجلة التحدث مخصصة لكل مستوى
WHEEL_TOPICS = {
    "A1.1": [
        "قدم نفسك بالكامل (الاسم، العمر، الجنسية، ومكان السكن).",
        "تحدث عن الألوان والأسماء المفضلة لديك داخل غرفتك.",
        "اذكر خمسة أشياء تستخدمها يومياً في حقيبتك أو فصلك الدراسي."
    ],
    "A1.2": [
        "صف عائلتك (عدد الأفراد، وظائفهم، وأشكالهم).",
        "تحدث بالتفصيل عن روتينك الصباحي من وقت الاستيقاظ.",
        "ما هو طعامك المفضل؟ واذكر المكونات الأساسية له بالأسبانية."
    ],
    "A1.3": [
        "تخيل أنك في السوبرماركت، تحدث عن المنتجات التي تشتريها.",
        "صف مدينتك الحالية وما هي الأماكن المفضلة للزوار فيها.",
        "كيف تقضي عطلة نهاية الأسبوع النموذجية بالنسبة لك؟"
    ],
    "A2.1": [
        "تحدث عن الهواية المفضلة التي بدأت ممارستها مؤخراً ولماذا اخترتها.",
        "صف أعز أصدقائك واذكر الموقف الذي جمعكم أول مرة.",
        "تحدث عما فعلته في عطلة الأسبوع الماضي بالكامل باستخدام زمن الماضي."
    ],
    "A2.2": [
        "احكِ لنا كيف كانت حياتك وشكلك في مرحلة الطفولة وزمن المدرسة.",
        "تحدث عن وصفة طبخ أعددتها بنفسك سابقاً واشرح خطواتها.",
        "ماذا تفعل عندما تشعر بالمرض أو التعب؟ صف تجربة سابقة."
    ],
    "A2.3": [
        "وجه دعوة لصديق لزيارة مكان ما واقترح عليه الأنشطة والوقت المحتمل.",
        "صف ملامح مدينتك المثالية التي تتمنى العيش فيها في المستقبل.",
        "تحدث عن وظيفة أحلامك وما هي المهارات المطلوبة للعمل بها."
    ],
    "B1.1": [
        "احكِ لنا عن رحلة مميزة قمت بها ولا يمكن أن تنساها أبدًا.",
        "ما هي خططك وطموحاتك الشخصية والمهنية للسنوات الثلاث القادمة؟",
        "تحدث عن فيلم سينمائي أو كتاب قرأته مؤخراً واشرح فكرته الأساسية."
    ],
    "B1.2": [
        "تحدث عن إيجابيات وسلبيات وسائل التواصل الاجتماعي وتأثيرها علينا.",
        "ما هو أسلوب الحياة الصحي من وجهة نظرك؟ واذكر عاداتك اليومية.",
        "كيف يمكن للأفراد المساهمة في حماية كوكب الأرض من التلوث؟"
    ],
    "B1.3": [
        "تحدث عن أهمية الفنون والموسيقى وتأثيرها في ثقافات الشعوب المختلفة.",
        "احكِ عن تجربة شخصية صعبة مررت بها وكيف تغلبت عليها بنجاح.",
        "عبر عن رأيك الشخصي حول التعليم عن بُعد مقارنة بالتعليم التقليدي."
    ],
    "B2.1": [
        "كيف تطورت شخصيتك وأفكارك مقارنة بما كنت عليه قبل خمس سنوات؟",
        "ما هي أهم التحديات التي تواجه الشباب في سوق العمل المعاصر؟",
        "تحدث عن مفهوم النجاح الشخصي وكيف تقيسه في حياتك."
    ],
    "B2.2": [
        "ناقش ظاهرة إدمان الهواتف الذكية وكيف تؤثر على الترابط الأسري.",
        "ما هي برأيك أفضل الطرق للحفاظ على التوازن بين الصحة النفسية والجسدية؟",
        "احكِ عن موقف حرج جداً واجهته وكيف تداركت الأمر بذكاء."
    ],
    "B2.3": [
        "تحدث عن مكان استثنائي وغريب زرته أو قرأت عنه وتمنيت الذهاب إليه.",
        "عبر عن تطلعاتك المستقبلية طويلة المدى ودور لغة الإسبانية في تحقيقها.",
        "كيف تتعامل مع المشكلات والشكاوى اليومية في محيط العمل أو الدراسة؟"
    ]
}

# 6. الجمل التحفيزية
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
        
        .doodle-container {
            position: absolute; display: flex; flex-direction: column; align-items: center;
            opacity: 0.65; z-index: 0; color: #333;
        }
        .doodle-container i { font-size: 38px; margin-bottom: 5px; color: #444; }
        .doodle-container span { font-family: 'Reenie Beanie', cursive; font-size: 28px; font-weight: bold; color: var(--primary-red); }
        
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
    <div class="doodle-container d-1"><i class="fa-regular fa-sun"></i><span>Sol</span></div>
    <div class="doodle-container d-2"><i class="fa-solid fa-guitar"></i><span>Música</span></div>
    <div class="doodle-container d-3"><i class="fa-solid fa-pepper-hot"></i><span>Picante</span></div>
    <div class="doodle-container d-4"><i class="fa-regular fa-comment-dots"></i><span>¡Hola!</span></div>
    <div class="doodle-container d-5"><span style="font-size: 35px; color: #333;">Familia</span></div>
    <div class="doodle-container d-6"><span style="font-size: 35px; color: #333;">Gracias</span></div>

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
        
        .top-nav {
            background: white; padding: 12px 30px; display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06); position: sticky; top: 0; z-index: 100;
        }

        .top-right-container { display: flex; align-items: center; gap: 20px; }
        .user-buttons { display: flex; align-items: center; gap: 15px; }
        .logout-btn { 
            display: flex; align-items: center; gap: 8px;
            background: #ffebeb; color: var(--primary); padding: 8px 18px; border-radius: 8px; 
            text-decoration: none; font-size: 14px; font-weight: 700; transition: 0.3s; 
        }
        .logout-btn:hover { background: var(--primary); color: white; }
        .level-badge { background: #eef2f5; color: var(--secondary); padding: 8px 18px; border-radius: 50px; font-size: 13px; font-weight: 700; border: 1px solid #d1d9e0; }
        
        .v-divider { width: 2px; height: 30px; background-color: #e2e8f0; }

        .social-icons { display: flex; gap: 10px; align-items: center; }
        .social-icons a {
            display: flex; align-items: center; justify-content: center;
            width: 36px; height: 36px; border-radius: 50%;
            background: #f0f3f5; color: var(--text-muted); text-decoration: none;
            font-size: 16px; transition: all 0.3s ease;
        }
        .social-icons a:hover { background: var(--primary); color: white; transform: translateY(-2px); }

        .brand-area { display: flex; align-items: center; gap: 15px; }
        .brand-area img { width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid var(--accent); }
        .brand-area h1 { font-size: 20px; font-weight: 900; color: var(--secondary); margin: 0; }
        .brand-area h1 span { color: var(--primary); }

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

        .tabs-nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 25px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .tab-trigger { 
            background: none; border: none; font-size: 15px; font-weight: 700; color: var(--text-muted); 
            padding: 10px 20px; cursor: pointer; transition: 0.3s; border-radius: 12px; 
            display: flex; align-items: center; gap: 8px;
        }
        .tab-trigger:hover { background: #eef2f5; }
        .tab-trigger.active { background: var(--primary); color: white; }

        .tab-content { display: none; animation: fadeIn 0.4s ease; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
        .course-card { background: white; border-radius: 20px; overflow: hidden; border: 1px solid #f0f3f5; transition: 0.3s; display: flex; flex-direction: column; }
        .course-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .card-header { padding: 20px; background: #fafbfc; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center;}
        .lesson-number { font-size: 13px; font-weight: 800; color: var(--primary); background: rgba(229, 36, 33, 0.1); padding: 5px 12px; border-radius: 50px; }
        .card-body { padding: 25px 30px; text-align: center; flex-grow: 1; }
        .card-body h4 { font-size: 18px; font-weight: 800; color: var(--secondary); margin-bottom: 25px; }
        
        .card-action-btn { display: inline-block; width: 100%; padding: 14px; text-decoration: none; border-radius: 12px; font-weight: 700; font-size: 15px; transition: 0.2s; box-sizing: border-box; }
        .btn-lecture { background: var(--primary); color: white; }
        .btn-exercise { background: var(--accent); color: var(--secondary); }

        .video-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }

        .wheel-box { text-align: center; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
        .wheel-display { 
            font-size: 22px; font-weight: 800; color: var(--secondary); padding: 40px 20px; 
            margin: 20px auto; max-width: 700px; min-height: 150px; 
            display: flex; align-items: center; justify-content: center;
            border: 3px dashed var(--accent); border-radius: 20px; background: #fffdf5;
            transition: all 0.2s ease;
        }
        .spin-btn { 
            background: var(--primary); color: white; border: none; padding: 15px 40px; 
            font-size: 20px; font-weight: 900; border-radius: 50px; cursor: pointer; 
            transition: 0.3s; box-shadow: 0 5px 15px rgba(229, 36, 33, 0.3);
        }
        .spin-btn:hover { background: var(--primary-dark); transform: translateY(-3px); }
        .spin-btn:disabled { background: #ccc; cursor: not-allowed; transform: none; box-shadow: none;}
        .spinning { animation: shake 0.1s infinite; color: var(--primary); }
        @keyframes shake { 0% { transform: translateX(0); } 25% { transform: translateX(-2px); } 50% { transform: translateX(2px); } 100% { transform: translateX(0); } }
        
        .timer-display { font-size: 30px; font-weight: 900; color: var(--primary); margin-top: 20px; display: none;}
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="top-right-container">
            <div class="user-buttons">
                <a href="/logout" class="logout-btn">خروج <i class="fa-solid fa-arrow-right-from-bracket"></i></a>
                <span class="level-badge"><i class="fa-solid fa-graduation-cap"></i> مستواك: {{ student.level }}</span>
            </div>
            <div class="v-divider"></div>
            <div class="social-icons">
                <a href="https://www.facebook.com/institutoamigos1" target="_blank" title="Facebook"><i class="fab fa-facebook-f"></i></a>
                <a href="https://www.instagram.com/instituto_amigos1/" target="_blank" title="Instagram"><i class="fab fa-instagram"></i></a>
                <a href="https://www.tiktok.com/@espanolconamigos" target="_blank" title="TikTok"><i class="fab fa-tiktok"></i></a>
                <a href="https://wa.me/+201108425280" target="_blank" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
            </div>
        </div>

        <div class="brand-area" dir="ltr">
            <img src="/static/assets/logo.png" alt="Logo" onerror="this.src='https://ui-avatars.com/api/?name=IA&background=ffd100&color=e52421'">
            <h1>Instituto <span>Amigos</span></h1>
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
            <button class="tab-trigger" onclick="switchTab(event, 'schedule-tab')"><i class="fa-solid fa-calendar-days"></i> جدول المذاكرة</button>
            <button class="tab-trigger" onclick="switchTab(event, 'games-tab')"><i class="fa-solid fa-gamepad"></i> الألعاب</button>
            <button class="tab-trigger" onclick="switchTab(event, 'videos-tab')"><i class="fa-brands fa-youtube"></i> الفيديوهات</button>
            <button class="tab-trigger" onclick="switchTab(event, 'wheel-tab')"><i class="fa-solid fa-dharmachakra"></i> عجلة التحدث</button>
        </nav>

        <!-- 1. تبويب المحاضرات -->
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

        <!-- 2. تبويب التمارين -->
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

        <!-- 3. تبويب جدول المذاكرة (يفتح في صفحة جديدة) -->
        <div id="schedule-tab" class="tab-content">
            <h3 style="margin-bottom: 20px; color: var(--secondary);"><i class="fa-solid fa-calendar-check"></i> خطتك الأسبوعية للمذاكرة</h3>
            <div class="cards-grid">
                <div class="course-card">
                    <div class="card-header" style="justify-content: center; background: #f8fafc; padding: 30px;">
                        <i class="fa-solid fa-calendar-days" style="font-size: 50px; color: var(--secondary);"></i>
                    </div>
                    <div class="card-body">
                        <h4>جدول المذاكرة لمستوى {{ student.level }}</h4>
                        <p style="color: var(--text-muted); margin-bottom: 20px; font-size: 14px;">اضغط هنا عشان تفتح الخطة الأسبوعية الخاصة بمستواك في صفحة جديدة.</p>
                        <a href="{{ schedule_url }}" target="_blank" class="card-action-btn" style="background: var(--secondary); color: white;">افتح الجدول <i class="fa-solid fa-external-link-alt"></i></a>
                    </div>
                </div>
            </div>
        </div>

        <!-- 4. تبويب الألعاب (يفتح في صفحة جديدة) -->
        <div id="games-tab" class="tab-content">
            <h3 style="margin-bottom: 20px; color: var(--secondary);"><i class="fa-solid fa-puzzle-piece"></i> العب واتعلم</h3>
            <div class="cards-grid">
                <div class="course-card">
                    <div class="card-header" style="justify-content: center; background: #f8fafc; padding: 30px;">
                        <i class="fa-solid fa-gamepad" style="font-size: 50px; color: #2ecc71;"></i>
                    </div>
                    <div class="card-body">
                        <h4>ألعاب وتدريبات مستوى {{ student.level }}</h4>
                        <p style="color: var(--text-muted); margin-bottom: 20px; font-size: 14px;">استمتع بالتدريبات التفاعلية والأنشطة الممتعة الخاصة بمستواك، اضغط لتفتحها في صفحة جديدة.</p>
                        <a href="{{ game_url }}" target="_blank" class="card-action-btn" style="background: #2ecc71; color: white;">ادخل العب <i class="fa-solid fa-external-link-alt"></i></a>
                    </div>
                </div>
            </div>
        </div>

        <!-- 5. تبويب الفيديوهات -->
        <div id="videos-tab" class="tab-content">
            <h3 style="margin-bottom: 20px; color: var(--secondary);"><i class="fa-solid fa-film"></i> مكتبة الشروحات المرئية لمستوى {{ student.level }}</h3>
            <div class="cards-grid">
                {% for video in videos_list %}
                <div class="course-card" style="padding: 15px;">
                    <div class="video-container">
                        <iframe src="https://www.youtube.com/embed/{{ video.youtube_id }}" title="{{ video.title }}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                    <h4 style="margin-top: 15px; font-size: 16px;">{{ video.title }}</h4>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- 6. تبويب عجلة التحدث -->
        <div id="wheel-tab" class="tab-content">
            <div class="wheel-box">
                <h3 style="color: var(--secondary); margin-bottom: 10px;"><i class="fa-solid fa-microphone-lines"></i> عجلة التحدث والطلاقة</h3>
                <p style="color: var(--text-muted);">اضغط على الزر ليتم اختيار موضوع عشوائي مناسب لمستواك الحالي ({{ student.level }}). تحدث عنه لمدة دقيقة إلى دقيقتين بدون توقف!</p>
                
                <div id="topicDisplay" class="wheel-display">
                    اضغط على "لف العجلة" لبدء التحدي!
                </div>
                
                <button id="spinBtn" class="spin-btn" onclick="spinWheel()">لف العجلة <i class="fa-solid fa-rotate"></i></button>
                <div id="timerDisplay" class="timer-display">02:00</div>
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

        const levelTopics = {{ topics_json | safe }};
        
        function spinWheel() {
            const btn = document.getElementById("spinBtn");
            const display = document.getElementById("topicDisplay");
            const timerDisplay = document.getElementById("timerDisplay");
            
            btn.disabled = true;
            timerDisplay.style.display = "none";
            display.classList.add("spinning");
            
            let counter = 0;
            let spinInterval = setInterval(() => {
                const randomTopic = levelTopics[Math.floor(Math.random() * levelTopics.length)];
                display.innerText = randomTopic;
                counter++;
                
                if(counter > 20) {
                    clearInterval(spinInterval);
                    display.classList.remove("spinning");
                    
                    const finalTopic = levelTopics[Math.floor(Math.random() * levelTopics.length)];
                    display.innerHTML = `<span style="color: var(--primary); font-size: 26px;">🎯 ${finalTopic}</span>`;
                    
                    btn.innerText = "جرب موضوع تاني";
                    btn.disabled = false;
                    
                    startTimer(120, timerDisplay);
                }
            }, 100);
        }

        let timerInterval;
        function startTimer(duration, display) {
            clearInterval(timerInterval);
            display.style.display = "block";
            let timer = duration, minutes, seconds;
            
            timerInterval = setInterval(function () {
                minutes = parseInt(timer / 60, 10);
                seconds = parseInt(timer % 60, 10);

                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;

                display.textContent = minutes + ":" + seconds;

                if (--timer < 0) {
                    clearInterval(timerInterval);
                    display.textContent = "انتهى الوقت! أحسنت 👏";
                }
            }, 1000);
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
    
    student_schedule_url = SCHEDULE_DATA.get(level, "https://yourusername.github.io/your-repo/schedules/default.html")
    student_game_url = GAMES_DATA.get(level, "https://yourusername.github.io/your-repo/games/default.html")
    
    student_videos = VIDEOS_DATA.get(level, [{"title": "فيديو ترحيبي بالمستوى", "youtube_id": "dQw4w9WgXcQ"}])
    
    random_quote = random.choice(motivation_quotes)
    
    student_wheel_topics = WHEEL_TOPICS.get(level, ["تحدث عن مهاراتك اللغوية الحالية."])
    topics_json = json.dumps(student_wheel_topics, ensure_ascii=False)
    
    return render_template_string(
        DASHBOARD_HTML, 
        student=student, 
        lessons=level_lessons, 
        quote=random_quote,
        topics_json=topics_json,
        schedule_url=student_schedule_url,
        game_url=student_game_url,
        videos_list=student_videos
    )

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
