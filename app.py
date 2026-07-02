import os
import pandas as pd
import random
import json
from datetime import timedelta
from flask import Flask, render_template_string, request, redirect, url_for, session, abort, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'instituto_amigos_ultra_secure_2026')

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# =====================================================================
# [ روابط جوجل شيت ]
# =====================================================================
STUDENT_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdTMPVAfLN18RG6mLNXwycXhra4STzYPIiy7fvzCpeio0SfksLG4YNw78vA-djsSTG4rNSv2qdoXS8/pub?output=csv"
TEACHER_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8XNmds7FrrXWcDd8mwrD0AGc7e1tU_-ACrJ-vVF7UYsL36COnRtxiEoaMq9VhauxPyUGJqfEGak8X/pub?gid=854861638&single=true&output=csv" 
SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbychpxvHbr8JbOBoha0qTegQUtsVd8l0aPnt1V_7CyJniWSjGGbk1djI2Tzk3HrPa8x/exec'

# =====================================================================
# [ 1. المحاضرات - LESSONS_DATA ]
# =====================================================================
LESSONS_DATA = {
    "demo": [
        {"title": "HOLA, ¿QUÉ TAL?", "file": "lesson1.html"},
        {"title": "EL ESPAÑOL Y YO", "file": "lesson2.html"}
    ],
    "A1.1": [
        {"title": "HOLA, ¿QUÉ TAL?", "file": "lesson1.html"},
        {"title": "EL ESPAÑOL Y YO", "file": "lesson2.html"},
        {"title": "TRABAJO AQUÍ", "file": "lesson3.html"},
        {"title": "¡ME GUSTAN LAS TAPAS!", "file": "lesson4.html"}
    ],
    "A1.2": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "A1.3": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "A2.1": [
        {"title": "NUEVA ETAPA", "file": "A2.1_Libro_Unidad_1.html"},
        {"title": "PARA TI Y PARA MÍ", "file": "Unidad 02.htm"},
        {"title": "UN AÑO ESPECIAL", "file": "A2.1_Libro_Unidad_3.html"},
        {"title": "CON TUS MANOS", "file": "A2.1_Libro_Unidad_4.html"}
    ],
    "A2.2": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "A2.3": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "B1.1": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "B1.2": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "B1.3": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "B2.1": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "B2.2": [{"title": "درس تجريبي", "file": "lesson1.html"}],
    "B2.3": [{"title": "درس تجريبي", "file": "lesson1.html"}]
}

# =====================================================================
# [ 2. التمارين - EXERCISES_DATA ]
# =====================================================================
EXERCISES_DATA = {
    "demo": [
        {"title": "تمرين: HOLA, ¿QUÉ TAL?", "file": "exercise1.html"},
        {"title": "تمرين: EL ESPAÑOL Y YO", "file": "exercise2.html"}
    ],
    "A1.1": [
        {"title": "تمرين: HOLA, ¿QUÉ TAL?", "file": "exercise1.html"},
        {"title": "تمرين: EL ESPAÑOL Y YO", "file": "exercise2.html"},
        {"title": "تمرين: TRABAJO AQUÍ", "file": "exercise3.html"},
        {"title": "تمرين: ¡ME GUSTAN LAS TAPAS!", "file": "exercise4.html"}
    ],
    "A1.2": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "A1.3": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "A2.1": [
        {"title": "تمرين: NUEVA ETAPA", "file": "A2.1_U1_Eje.html"},
        {"title": "تمرين: PARA TI Y PARA MÍ", "file": "A2.1_U2_Eje.html"},
        {"title": "تمرين: UN AÑO ESPECIAL", "file": "A2.1U3Eje.html"},
        {"title": "تمرين: CON TUS MANOS", "file": "exercise4.html"}
    ],
    "A2.2": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "A2.3": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "B1.1": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "B1.2": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "B1.3": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "B2.1": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "B2.2": [{"title": "تمرين تجريبي", "file": "exercise1.html"}],
    "B2.3": [{"title": "تمرين تجريبي", "file": "exercise1.html"}]
}

# =====================================================================
# [ 3. الكلمات - VOCAB_DATA ]
# =====================================================================
VOCAB_DATA = {
    "demo": [
        {"title": "كلمات: HOLA, ¿QUÉ TAL?", "file": "vocab1.html"},
        {"title": "كلمات: EL ESPAÑOL Y YO", "file": "vocab2.html"}
    ],
    "A1.1": [
        {"title": "كلمات: HOLA, ¿QUÉ TAL?", "file": "vocab1.html"},
        {"title": "كلمات: EL ESPAÑOL Y YO", "file": "vocab2.html"},
        {"title": "كلمات: TRABAJO AQUÍ", "file": "vocab3.html"},
        {"title": "كلمات: ¡ME GUSTAN LAS TAPAS!", "file": "vocab4.html"}
    ],
    "A1.2": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "A1.3": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "A2.1": [
        {"title": "كلمات: NUEVA ETAPA", "file": "A2.1_Vocab_Unidad_1.html"},
        {"title": "كلمات: PARA TI Y PARA MÍ", "file": "A2.1_Vocab_Unidad_2.html"},
        {"title": "كلمات: UN AÑO ESPECIAL", "file": "A2.1_Vocab_Unidad_3.html"},
        {"title": "كلمات: CON TUS MANOS", "file": "vocab4.html"}
    ],
    "A2.2": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "A2.3": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "B1.1": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "B1.2": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "B1.3": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "B2.1": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "B2.2": [{"title": "كلمات تجريبية", "file": "vocab1.html"}],
    "B2.3": [{"title": "كلمات تجريبية", "file": "vocab1.html"}]
}

# =====================================================================
# [ 4. جداول المذاكرة - SCHEDULES_DATA ]
# =====================================================================
SCHEDULES_DATA = {
    "demo": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}
    ],
    "A1.1": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "A1.2": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "A1.3": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "A2.1": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "A2.1_Plan_Unidad_1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "A2.1_Plan_Unidad_2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "A2.1_Plan_Unidad_3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "gadwal4.html"}
    ],
    "A2.2": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "A2.3": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "B1.1": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "B1.2": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "B1.3": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "B2.1": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "B2.2": [{"title": "جدول تجريبي", "file": "schedule1.html"}],
    "B2.3": [{"title": "جدول تجريبي", "file": "schedule1.html"}]
}

# =====================================================================
# [ 5. الألعاب الفردية - GAMES_DATA ]
# =====================================================================
GAMES_DATA = {
    "demo": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}
    ],
    "A1.1": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "A1.2": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "A1.3": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "A2.1": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "juego-estudiante1.htm"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "Unidad 02 - Juego _Est.htm"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "A2.2": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "A2.3": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "B1.1": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "B1.2": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "B1.3": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "B2.1": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "B2.2": [{"title": "لعبة تجريبية", "file": "game1.html"}],
    "B2.3": [{"title": "لعبة تجريبية", "file": "game1.html"}]
}

# =====================================================================
# [ 6. الشادوينج - SHADOWING_DATA ]
# =====================================================================
SHADOWING_DATA = {
    "demo": [
        {"title": "شادوينج: HOLA, ¿QUÉ TAL?", "file": "shadowing1.html"},
        {"title": "شادوينج: EL ESPAÑOL Y YO", "file": "shadowing2.html"}
    ],
    "A1.1": [
        {"title": "شادوينج: HOLA, ¿QUÉ TAL?", "file": "shadowing1.html"},
        {"title": "شادوينج: EL ESPAÑOL Y YO", "file": "shadowing2.html"},
        {"title": "شادوينج: TRABAJO AQUÍ", "file": "shadowing3.html"},
        {"title": "شادوينج: ¡ME GUSTAN LAS TAPAS!", "file": "shadowing4.html"}
    ],
    "A1.2": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "A1.3": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "A2.1": [
        {"title": "شادوينج: NUEVA ETAPA", "file": "A2.1_Shadowing_Unidad_1.html"},
        {"title": "شادوينج: PARA TI Y PARA MÍ", "file": "A2.1_Shadowing_Unidad_2.html"},
        {"title": "شادوينج: UN AÑO ESPECIAL", "file": "A2.1_Shadowing_Unidad_3.html"},
        {"title": "شادوينج: CON TUS MANOS", "file": "shadowing4.html"}
    ],
    "A2.2": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "A2.3": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "B1.1": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "B1.2": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "B1.3": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "B2.1": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "B2.2": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}],
    "B2.3": [{"title": "شادوينج تجريبي", "file": "shadowing1.html"}]
}

# =====================================================================
# [ 7. الفيديوهات - VIDEOS_DATA ]
# =====================================================================
VIDEOS_DATA = {
    "demo": [
        {"title": "مراجعة قواعد النطق الأساسية والأبجدية", "youtube_id": "dQw4w9WgXcQ"},
        {"title": "أدوات التعريف والتنكير في الإسبانية", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "A1.1": [
        {"title": "مراجعة قواعد النطق الأساسية والأبجدية", "youtube_id": "dQw4w9WgXcQ"},
        {"title": "أدوات التعريف والتنكير في الإسبانية", "youtube_id": "dQw4w9WgXcQ"}
    ],
    "A1.2": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "A1.3": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "A2.1": [
        {"title": "Un día muy especial", "youtube_id": "7dgZvDijGP0"},
        {"title": "Soy un manitas", "youtube_id": "fnC6LeUHcq0"}
    ],
    "A2.2": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "A2.3": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "B1.1": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "B1.2": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "B1.3": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "B2.1": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "B2.2": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}],
    "B2.3": [{"title": "فيديو تجريبي", "youtube_id": "dQw4w9WgXcQ"}]
}

# =====================================================================
# [ 8. الألعاب الجماعية - MULTIPLAYER_GAMES_DATA ]
# =====================================================================
MULTIPLAYER_GAMES_DATA = {
    "demo": [
        {"title": "لعبة كاهوت جماعية 1", "file": "multi1.html"},
        {"title": "لعبة تفاعلية للفصل", "file": "multi2.html"}
    ],
    "A1.1": [
        {"title": "لعبة كاهوت جماعية 1", "file": "multi1.html"},
        {"title": "لعبة تفاعلية للفصل", "file": "multi2.html"}
    ],
    "A1.2": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "A1.3": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "A2.1": [
        {"title": "Unidad 2", "file": "Unidad 02 - Juego _Grupo.htm"}
    ],
    "A2.2": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "A2.3": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "B1.1": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "B1.2": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "B1.3": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "B2.1": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "B2.2": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}],
    "B2.3": [{"title": "لعبة جماعية تجريبية", "file": "multi1.html"}]
}

# =====================================================================
# [ 9. عجلة التحدث - WHEEL_TOPICS ]
# =====================================================================
WHEEL_TOPICS = {
    "demo": [
        "قدم نفسك بالكامل: اسمك وسنك وبلدك وظيفتك.",
        "تحدث عن الألوان المفضلة لديك ولماذا تحبها.",
        "اذكر 5 أشياء تستخدمها كل يوم في غرفتك أو حقيبتك.",
        "اوصف الطقس اليوم بالإسبانية (حار، بارد، مشمس).",
        "قول أيام الأسبوع وقول ماذا تفعل في كل يوم.",
        "اتكلم عن أكلتك المفضلة ومشروبك المفضل.",
        "عرّف صاحبك المقرب: اسمه وشكله وأين يعيش.",
        "قول الأرقام من 1 لـ 20 وبعدين العد العكسي من 20 إلى 1.",
        "اوصف أوضتك في البيت: ماذا يوجد فيها من أثاث؟",
        "سلم على شخص جديد وعرّفه بنفسك وبأسرتك.",
        "تحدث عن أفراد عائلتك (الأب، الأم، الإخوة والأخوات).",
        "اذكر أوقات اليوم ووجباتك الثلاثة (الإفطار، الغداء، العشاء).",
        "تحدث عن حيوانك المفضل ولماذا تحبه.",
        "اذكر 5 دول تتحدث الإسبانية وجنسيات أهلها.",
        "تحدث عن روتينك الصباحي البسيط: متى تستيقظ وماذا تفعل أولاً."
    ],
    "A1.1": [
        "قدم نفسك بالكامل: اسمك وسنك وبلدك وظيفتك.",
        "تحدث عن الألوان المفضلة لديك ولماذا تحبها.",
        "اذكر 5 أشياء تستخدمها كل يوم في غرفتك أو حقيبتك.",
        "اوصف الطقس اليوم بالإسبانية (حار، بارد، مشمس).",
        "قول أيام الأسبوع وقول ماذا تفعل في كل يوم.",
        "اتكلم عن أكلتك المفضلة ومشروبك المفضل.",
        "عرّف صاحبك المقرب: اسمه وشكله وأين يعيش.",
        "قول الأرقام من 1 لـ 20 وبعدين العد العكسي من 20 إلى 1.",
        "اوصف أوضتك في البيت: ماذا يوجد فيها من أثاث؟",
        "سلم على شخص جديد وعرّفه بنفسك وبأسرتك.",
        "تحدث عن أفراد عائلتك (الأب، الأم، الإخوة والأخوات).",
        "اذكر أوقات اليوم ووجباتك الثلاثة (الإفطار، الغداء، العشاء).",
        "تحدث عن حيوانك المفضل ولماذا تحبه.",
        "اذكر 5 دول تتحدث الإسبانية وجنسيات أهلها.",
        "تحدث عن روتينك الصباحي البسيط: متى تستيقظ وماذا تفعل أولاً."
    ],
    "A1.2": [
        "تحدث عن روتينك اليومي بالتفصيل من الصباح حتى المساء.",
        "اوصف بيتك أو شقتك بالتفصيل (عدد الغرف والأثاث الموجود).",
        "ماذا تفعل عادة في وقت فراغك وعطلة نهاية الأسبوع؟",
        "تحدث عن مدينتك أو حيك وماذا يوجد به من أماكن وخدمات.",
        "كيف تقضي يوم العطلة مع عائلتك أو أصدقائك؟",
        "تحدث عن رياضتك المفضلة وكم مرة تمارسها في الأسبوع.",
        "اذكر كيف تذهب إلى العمل أو الجامعة وما هي وسائل المواصلات.",
        "تخيل أنك في مطعم إسباني: اطلب وجبتك المفضلة وتحدث مع النادل.",
        "تحدث عن فصلك المفضل من فصول السنة الأربعة ولماذا.",
        "اوصف ملابس ارتديتها اليوم أو تحب ارتدائها في المناسبات.",
        "تحدث عن مهنة تحبها وماذا يفعل أصحاب هذه المهنة يومياً.",
        "اسأل زميلك 5 أسئلة للتعرف على هواياته واهتماماته.",
        "تحدث عن سوق أو متجر تحب التسوق فيه وماذا تشتري منه.",
        "اوصف حفلة عيد ميلاد حضرتها وكيف كان الاحتفال.",
        "تحدث عن اللغات التي تتحدثها ولماذا قررت تعلم اللغة الإسبانية."
    ],
    "A1.3": [
        "تحدث عن رحلة قمت بها في الماضي القريب وماذا أعجبك فيها.",
        "قارن بين مدينتك الحالية ومدينتك المفضلة للسفر والعطلات.",
        "ما هي خططك لعطلة نهاية الأسبوع القادمة؟",
        "تحدث عن وجبة قمت بطهيها أو تحب أن تتعلم طهيها.",
        "اوصف صديقاً لم تره منذ فترة طويلة وتذكر ذكرياتكم معاً.",
        "تحدث عن مكان سياحي شهير في مصر أو إسبانيا وتنصح بزيارته.",
        "كيف تحتفل مع أسرتك بالأعياد والمناسبات الرسمية؟",
        "تحدث عن برنامج تلفزيوني أو مسلسل تتابعه بانتظام.",
        "اوصف حديقة أو مكان طبيعي تحب قضاء الوقت فيه للاسترخاء.",
        "ما هي العادات الصحية التي تحرص على القيام بها يومياً؟",
        "تحدث عن هدية مميزة تلقيتها أو قدمتها لشخص عزيز.",
        "اوصف كيف كانت طفولتك وألعابتك المفضلة عندما كنت صغيراً.",
        "تحدث عن يوم استثنائي أو موقف طريف حدث لك مؤخراً.",
        "اذكر 3 نصائح لشخص يبدأ تعلم اللغة الإسبانية حديثاً.",
        "تحدث عن مشروع صغير أو فكرة تحب تنفيذها في المستقبل."
    ],
    "A2.1": [
        "تحدث عن هواية جديدة بدأت ممارستها مؤخراً ولماذا اخترتها.",
        "صف أعز أصدقائك: شخصيته، طباعه، واهتماماته المشتركة معك.",
        "تحدث بالتفصيل عما فعلته في عطلة الأسبوع الماضي.",
        "اوصف تجربتك في تعلم اللغة الإسبانية والتحديات التي تجاوزتها.",
        "اتكلم عن أحلامك وأهدافك المهنية والشخصية للسنوات القادمة.",
        "لو سافرت إلى إسبانيا غداً، ما هي أول 3 مدن ستزورها ولماذا؟",
        "اوصف احتفالك بعيد ميلادك الأخير ومن كان معك.",
        "اتكلم عن فيلم أو مسلسل شاهدته مؤخراً ولخص قصته ورأيك فيه.",
        "صف شخصية تاريخية أو عامة تحبها وتقدر إنجازاتها.",
        "قارن بين حياتك وطريقة تفكيرك الآن وقبل 5 سنوات.",
        "تحدث عن أهم كتاب قرأته أو قصة أثرت في تفكيرك.",
        "اوصف موقفاً واجهت فيه مشكلة وكيف استطعت حلها بحكمة.",
        "ما رأيك في استخدام وسائل التواصل الاجتماعي وأثرها على حياتنا؟",
        "تحدث عن ثقافة أو عادات دولة إسبانية أو أمريكية لاتينية تثير فضولك.",
        "صف يوماً مثالياً بالنسبة لك من البداية حتى النهاية."
    ],
    "A2.2": [
        "تحدث عن تجربة سفر غيرت نظرتك للحياة أو عرفتك على ثقافة جديدة.",
        "ما هي الصفات التي تجعل الشخص مديراً أو قائداً ناجحاً في رأيك؟",
        "تحدث عن أهم اختراع تكنولوجي في حياتك ولا تستغني عنه أبداً.",
        "لو كان بإمكانك العيش في أي حقبة زمنية، أي فترة ستختار ولماذا؟",
        "تحدث عن أهمية الحفاظ على البيئة وماذا يمكننا فعله يومياً.",
        "اوصف مناسبة تقليدية أو عرس حضرتها وكيف كانت الطقوس والعادات.",
        "ما هي النصيحة الذهبية التي قدمها لك أحد والديك أو أساتذتك وتعمل بها؟",
        "تحدث عن الفرق بين الحياة في الريف الهادئ والحياة في المدن المزدحمة.",
        "كيف تتعامل مع التوتر وضغوط العمل أو المذاكرة؟",
        "صف وجبة طعام غريبة أو جديدة جربتها لأول مرة وكيف كان انطباعك.",
        "تحدث عن دور الفنون والموسيقى في التعبير عن ثقافة الشعوب.",
        "ما هي المهارة التي تتمنى إتقانها خلال الستة أشهر القادمة؟",
        "تحدث عن تجربة تطوعية أو مساعدة قدمتها لشخص أو للمجتمع.",
        "اوصف كيف تطورت أساليب التعليم والتعلم عبر الإنترنت في السنوات الأخيرة.",
        "تحدث عن طموحك الشخصي وكيف تقيس النجاح في حياتك."
    ],
    "A2.3": [
        "ناقش إيجابيات وسلبيات العمل عن بُعد (Remote Work) مقارنة بالعمل المكتبي.",
        "تحدث عن قضية اجتماعية تشغلك وكيف يمكن للمجتمع التعامل معها.",
        "كيف تؤثر ممارسة الرياضة بانتظام على الصحة النفسية والجسدية؟",
        "تحدث عن شخص يعتبر قدوة وملهم لك في مجال تخصصك أو عملك.",
        "ما هو رأيك في القراءة الإلكترونية مقابل الكتب الورقية التقليدية؟",
        "اوصف رحلة استكشافية تتمنى القيام بها في الطبيعة أو الجبال.",
        "تحدث عن كيفية تنظيم وقتك والتوازن بين العمل والحياة الشخصية.",
        "ما هي أهمية تعلم لغات متعددة في عالمنا العالمي المتصل اليوم؟",
        "ناقش تأثير الإعلانات التجارية على عادات التسوق لدى المستهلكين.",
        "تحدث عن أهمية الصداقة الحقيقية وكيف نحافظ عليها على مر السنين.",
        "لو كنت تمتلك ميزانية لإنشاء مشروع خدمي في مدينتك، ماذا سيكون؟",
        "اوصف تجربة ثقافية أو فنية (مسرحية، معرض، حفلة) أثارت إعجابك.",
        "كيف يمكن للشباب الاستعداد لوظائف المستقبل في ظل التطور التكنولوجي؟",
        "تحدث عن أهم درس تعلمته من خطأ أو فشل مررت به في الماضي.",
        "شاركنا وجهة نظرك عن أهمية السفر والتعرف على شعوب العالم."
    ],
    "B1.1": [
        "ناقش دور التكنولوجيا والذكاء الاصطناعي في تغيير سوق العمل المستقبلي.",
        "تحدث عن تجربة تحدي صعب مررت به وكيف طورت من مهاراتك الشخصية.",
        "ما هي المقومات الأساسية لبناء مجتمع صحي ومستدام في رأيك؟",
        "قارن بين العادات الغذائية الحديثة والتقليدية وتأثيرها على الصحة العامة.",
        "تحدث عن أثر السينما والمسرح في تشكيل الوعي العام وثقافة الشباب.",
        "كيف يمكن للتعليم المستمر (Lifelong Learning) أن يساعد في التطور المهني؟",
        "ناقش ظاهرة العولمة وتأثيرها على الهوية الثقافية للمجتمعات المحلية.",
        "تحدث عن كتاب أو مقال علمي قرأته وأحدث تغييراً في تفكيرك.",
        "ما هي العوامل التي تجعل مدينة ما مكاناً مثالياً للعيش والاستقرار؟",
        "كيف يمكننا تشجيع السياحة البيئية والحفاظ على المعالم الطبيعية؟",
        "تحدث عن دور الشباب في العمل التطوعي ومبادرات خدمة المجتمع.",
        "ناقش العلاقة بين المال والسعادة وهل يحقق المال الرضا النفسي الكامل؟",
        "كيف تؤثر وسائل الإعلام الحديثة في صياغة الرأي العام؟",
        "تحدث عن أهمية المرونة وتقبل التغيير في مواجهة أزمات الحياة.",
        "صف مشروعاً ريادياً تتمنى إطلاقه لحل مشكلة يومية في مجتمعك."
    ],
    "B1.2": [
        "ناقش التحديات البيئية العالمية مثل التغير المناخي وكيفية الحد منها.",
        "تحدث عن أهمية التنوع الثقافي في بيئة العمل الدولية.",
        "كيف يؤثر الإجهاد الرقمي (Digital Fatigue) على إنتاجية الأفراد وعلاقاتهم؟",
        "قارن بين وسائل النقل المستدامة والتقليدية وأثرها على تخطيط المدن.",
        "تحدث عن قيمة العمل الجماعي وكيفية إدارة الخلافات داخل الفريق.",
        "ما رأيك في تطور الصحافة الإلكترونية وتراجع الصحف المطبوعة؟",
        "تحدث عن استراتيجيات إدارة المالية الشخصية والادخار للشباب.",
        "كيف يمكن للأدب والفنون أن تكون جسراً للسلام والتفاهم بين الشعوب؟",
        "ناقش تأثير العمل الأكاديمي والبحث العلمي في تقدم الأمم.",
        "تحدث عن أهمية الصحة العقلية والدعم النفسي في بيئات العمل الحديثة.",
        "ما هو دور الطاقات المتجددة في تأمين مستقبل الأرض للأجيال القادمة؟",
        "اوصف كيفية بناء علامة تجارية شخصية (Personal Branding) ناجحة.",
        "ناقش العوامل المؤثرة في اتخاذ القرارات المصيرية في الحياة.",
        "تحدث عن تطور التجارة الإلكترونية وتغيير سلوك المستهلك.",
        "شاركنا برأيك في كيفية تنمية مهارات التفكير النقدي لدى الطلاب."
    ],
    "B1.3": [
        "ناقش الأبعاد الأخلاقية لاستخدام التكنولوجيا الحيوية والذكاء الاصطناعي.",
        "تحدث عن استراتيجيات التفاوض الفعال وحل النزاعات في الحياة اليومية.",
        "كيف يساهم الحفاظ على التراث التاريخي في تعزيز الانتماء الوطني؟",
        "قارن بين أساليب القيادة الكلاسيكية والقيادة الملهمة في الشركات الحديثة.",
        "تحدث عن أثر الاقتصاد التشاركي (Sharing Economy) على الخدمات التقليدية.",
        "ما هي التحديات التي تواجه المبدعين والفنانين في العصر الرقمي؟",
        "ناقش أهمية التوازن بين النمو الاقتصادي وحماية الموارد الطبيعية.",
        "تحدث عن دور الرياضة العالمية في تعزيز التقارب الدبلوماسي والثقافي.",
        "كيف يمكن للمؤسسات التعليمية دمج المهارات الناعمة في المناهج الدراسية؟",
        "ناقش دور المرأة القيادي وأثره في تنمية المجتمع والاقتصاد.",
        "تحدث عن تطور مفهوم الرفاهية والنجاح في المجتمعات المعاصرة.",
        "كيف يؤثر التصميم المعماري للمدن على نفسية السكان وتفاعلهم؟",
        "ناقش أهمية القراءة التحليلية في مواجهة الأخبار المضللة (Fake News).",
        "تحدث عن أهمية الابتكار وريادة الأعمال في خلق فرص عمل جديدة.",
        "شاركنا رؤيتك لمستقبل العلاقات الإنسانية في ظل التطور الافتراضي."
    ],
    "B2.1": [
        "حلل أثر التحول الرقمي الشامل على استدامة الأعمال والشركات الكبرى.",
        "ناقش مسؤولية الأفراد والمؤسسات تجاه تحقيق أهداف التنمية المستدامة.",
        "تحدث عن تأثير التغيرات الديموغرافية والشيخوخة على أنظمة الرعاية الصحية.",
        "كيف يمكن للمجتمعات تحقيق التوازن بين الابتكار التقني وحماية الخصوصية؟",
        "ناقش أهمية التبادل الثقافي الدولي في الحد من النزاعات العالمية.",
        "تحدث عن استراتيجيات بناء المرونة المؤسسية وإدارة المخاطر.",
        "حلل تطور المفاهيم الحديثة للمواطنة العالمية في القرن الحادي والعشرين.",
        "ناقش دور الملكية الفكرية في حماية الإبداع وتشجيع الابتكار.",
        "تحدث عن العلاقة المعقدة بين حرية التعبير والمسؤولية الاجتماعية.",
        "كيف يؤثر التضخم والأزمات الاقتصادية على النمط الاستهلاكي للطبقة الوسطى؟",
        "حلل دور الفلسفة والفنون في معالجة القضايا الوجودية للإنسان المعاصر.",
        "ناقش مستقبل المدن الذكية وكيفية دمج الذكاء الاصطناعي في المرافق العامة.",
        "تحدث عن أهمية الأمن السيبراني في حماية البنية التحتية للدول.",
        "حلل أثر التغير السريع في أنماط العمل على العقود والتشريعات العمالية.",
        "شاركنا تحليلك لكيفية إعادة تشكيل الهوية الوطنية في ظل الرقمنة."
    ],
    "B2.2": [
        "ناقش التطور التاريخي والمستقبلي للاتفاقيات الدولية للمناخ وحماية البيئة.",
        "حلل التداعيات الاجتماعية والنفسية للاعتماد المتزايد على الروبوتات الخدمية.",
        "تحدث عن دور الدبلوماسية الثقافية والقوة الناعمة في العلاقات الدولية.",
        "كيف يمكن للنظم المالية الحديثة والعملات الرقمية إعادة تشكيل الاقتصاد العالمي؟",
        "ناقش الأبعاد الأخلاقية والقانونية لتحرير الجينات والتعديل الوراثي.",
        "تحدث عن أهمية الحفاظ على اللغات المهددة بالانقراض كجزء من التراث الإنساني.",
        "حلل تأثير الاقتصاد الدائري (Circular Economy) على تقليل النفايات والاستدامة.",
        "ناقش دور مؤسسات المجتمع المدني في مراقبة الأداء الحكومي وتعزيز الشفافية.",
        "تحدث عن التحديات التي تواجه سلاسل الإمداد العالمية في أوقات الأزمات.",
        "كيف يمكن للتعليم العالي مواءمة مخرجاته مع سرعة التغير التقني المعاصر؟",
        "حلل تأثير الثقافة الاستهلاكية السريعة (Fast Consumerism) على القيم الاجتماعية.",
        "ناقش العلاقة بين التخطيط العمراني المستدام والحد من الفوارق الطبقية.",
        "تحدث عن أهمية أخلاقيات الذكاء الاصطناعي في منع التحيز والخوارزميات المضللة.",
        "حلل دور وسائل الإعلام المستقلة في تعزيز الديمقراطية وحقوق الإنسان.",
        "شاركنا رؤيتك لتحديات التكامل الاقتصادي بين الدول النامية ومستقبلها."
    ],
    "B2.3": [
        "حلل الأثر الفلسفي والاجتماعي للتقنيات العصبية وتداخلها مع العقل البشري.",
        "ناقش مستقبل الحوكمة العالمية في مواجهة الأزمات العابرة للحدود.",
        "تحدث عن الأبعاد التنافسية للأمن الغذائي والمائي في ظل التغيرات الجيوسياسية.",
        "كيف يمكن للتكنولوجيا أن تسهم في القضاء على الفقر وتعزيز العدالة الاجتماعية؟",
        "ناقش التحديات الأخلاقية لتقنيات الواقع الافتراضي والميتافيرس على الهوية.",
        "تحدث عن دور الطاقة النووية والهيدروجين الأخضر كخيارات لإنقاذ المناخ العالمي.",
        "حلل أثر السياسات النقدية للبنوك المركزية على الاستقرار المالي الدولي.",
        "ناقش دور الإبداع والابتكار المفتوح في تطوير صناعات الأدوية والرعاية الصحية.",
        "تحدث عن التوازن الحرج بين الأمن القومي وحريات الأفراد المدنية في العصر الرقمي.",
        "حلل ظاهرة الهجرة العالمية وأثرها الاقتصادي والثقافي على الدول المستضيفة.",
        "ناقش مستقبل قطاع الفضاء واستغلال الموارد خارج كوكب الأرض.",
        "تحدث عن أهمية الحفاظ على التنوع البيولوجي في حماية التوازن البيئي للأرض.",
        "حلل كيف تؤثر الخوارزميات التنبؤية على حرية الإرادة واختيارات البشر.",
        "ناقش استراتيجيات تحقيق التحول العادل نحو الاقتصاد الأخضر دون إضرار بالعمالة.",
        "شاركنا تحليلك الفلسفي لمفهوم التقدم الإنساني وهل يقاس بالتكنولوجيا أم بالأخلاق."
    ]
}

# =====================================================================
# [ الجمل التحفيزية ]
# =====================================================================
motivation_quotes = [
    {"ar": "عاش يا بطل، الاستمرارية هي سر النجاح في أي لغة!", "es": "¡La constancia es la clave del éxito!"},
    {"ar": "كل درس بتخلصه بيقربك خطوة لحلمك، كمل وماتوقفش!", "es": "¡Sigue adelante, vas muy bien!"},
    {"ar": "المذاكرة النهاردة هي طلاقتك بكرة، شد حيلك!", "es": "¡Esfuérzate hoy para triunfar mañana!"},
    {"ar": "مافيش حاجة صعبة على واحد بيحاول كل يوم، إحنا واثقين فيك!", "es": "¡Con esfuerzo todo es posible!"},
    {"ar": "خطوة بخطوة هتوصل، المهم تفضل مكمل على نفس الحماس.", "es": "¡Paso a paso llegarás muy lejos!"},
    {"ar": "تعبك النهاردة هترتاح بيه بكرة، ركز في درسك واعمل اللي عليك.", "es": "¡Tu esfuerzo de hoy es el éxito de mañana!"},
    {"ar": "رحلة الألف ميل بتبدأ بخطوة، وأنت قطعت شوط كبير.. استمر!", "es": "¡Un viaje de mil millas comienza con un paso!"},
    {"ar": "اللغة مش بس كلمات، اللغة ثقافة وحياة جديدة بتفتحلك أبواب العالم.", "es": "¡Un nuevo idioma es una nueva vida!"},
    {"ar": "غلطاتك في النطق والتحدث هي أكبر معلم ليك، اتكلم وماتخفش!", "es": "¡El error es el mejor maestro, habla sin miedo!"},
    {"ar": "فخورين بمجهودك اليومي في المنصة، كمل وهتشوف النتيجة بنفسك.", "es": "¡Estamos muy orgullosos de tu dedicación!"},
    {"ar": "كل ربع ساعة بتذاكرها بتعمل فرق كبير في مستواك على المدى البعيد.", "es": "¡Cada minuto de práctica cuenta!"},
    {"ar": "سر إتقان الإسبانية هو الممارسة اليومية والاستماع المستمر.", "es": "¡Practica y escucha todos los días!"},
    {"ar": "أنت أقوى من أي صعوبة، واللغة الإسبانية هتكون أسهل مع كل تمرين.", "es": "¡Eres capaz de lograr todo lo que te propongas!"},
    {"ar": "استمتع برحلة التعلم، كل كلمة جديدة بتتعلمها هي انتصار ليك.", "es": "¡Disfruta el camino del aprendizaje!"},
    {"ar": "جهدك اليوم يفتح لك أبواب الفرص والمنح والوظائف غداً.", "es": "¡El conocimiento te abrirá todas las puertas!"},
    {"ar": "مستواك بيتحسن كل يوم حتى لو مش حاسس، الاستمرار هو المفتاح!", "es": "¡Mejoras cada día, sigue adelante!"},
    {"ar": "لا تقارن نفسك بحد، قارن مستواك النهاردة بمستواك الشهر اللي فات.", "es": "¡Compárate solo con tu versión de ayer!"},
    {"ar": "الحماس بيخليك تبدأ، لكن الالتزام والروتين هم اللي بيوصلوك للنجاح.", "es": "¡La disciplina supera a la motivación!"},
    {"ar": "لما تتعب افتكر أنت بدأت ليه، الإسبانية هتغير مستقبلك للأفضل!", "es": "¡Recuerda siempre por qué empezaste!"},
    {"ar": "ابتسم وأنت بتذاكر، أنت بتبني نسخة أفضل وأذكى من نفسك!", "es": "¡Sonríe, estás construyendo un futuro brillante!"},
    {"ar": "التدريب اليومي بيصنع المعجزات، استمر على نفس الجدول.", "es": "¡La práctica diaria hace al maestro!"},
    {"ar": "كل سؤال بتجاوبه صح هو خطوة جديدة نحو الطلاقة التامة.", "es": "¡Cada respuesta correcta te acerca a la fluidez!"},
    {"ar": "النجاح هو مجموع مجهودات صغيرة بتتكرر كل يوم بانتظام.", "es": "¡El éxito es la suma de pequeños esfuerzos!"},
    {"ar": "أنت في المكان الصح، ومعاك أفضل المناهج والتمارين.. انطلق!", "es": "¡Estás en el lugar correcto para aprender!"},
    {"ar": "ما تخافش من المحادثة، الإسباني لغة جميلة وسهلة لما تمارسها بحب.", "es": "¡Hablar español es fácil y divertido!"},
    {"ar": "تذكر دائماً: من يزرع الاجتهاد يحصد التفوق والتميز.", "es": "¡Quien siembra esfuerzo, cosecha éxito!"},
    {"ar": "أصعب جزء هو البداية، وأنت بالفعل بدأت وقطعت شوط رائع!", "es": "¡Lo más difícil es empezar, y ya estás aquí!"},
    {"ar": "اللغة الإسبانية بيتحدث بها أكثر من 500 مليون شخص، وأنت بقيت واحد منهم!", "es": "¡Ya eres parte del mundo hispanohablante!"},
    {"ar": "استمع جيداً، ردد بصوت عالٍ، واكتب بيدك.. هكذا تتقن اللغات!", "es": "¡Escucha, repite y escribe para dominar el idioma!"},
    {"ar": "نحن معك في كل خطوة، فخورين بك وبإصرارك على التميز!", "es": "¡Estamos contigo en cada paso del camino!"}
]

# =====================================================================
# [ دوال مساعدة ]
# =====================================================================
def get_user_data(username, password, role='student'):
    url = TEACHER_SHEET_CSV_URL if role == 'teacher' else STUDENT_SHEET_CSV_URL
    try:
        df = pd.read_csv(url, dtype=str)
        df.fillna('', inplace=True)
        df.columns = df.columns.str.strip()
        df['username'] = df['username'].str.strip()
        df['password'] = df['password'].str.strip()
        user_row = df[(df['username'] == str(username).strip()) & (df['password'] == str(password).strip())]
        if not user_row.empty:
            user_dict = user_row.iloc[0].to_dict()
            if str(user_dict.get('level', '')).strip().lower() == 'demo':
                user_dict['level'] = 'demo'
            return user_dict
    except Exception as e:
        print(f"Error checking Google Sheet ({role}): {e}")
    
    if role == 'student' and str(username).strip().lower() == 'demo' and str(password).strip() in ['demo', 'demo123', '123456']:
        return {'username': str(username).strip(), 'level': 'demo'}
    return None

def get_all_students_levels():
    try:
        df = pd.read_csv(STUDENT_SHEET_CSV_URL, dtype=str)
        df.fillna('', inplace=True)
        df.columns = df.columns.str.strip()
        df['username'] = df['username'].str.strip()
        df['level'] = df['level'].str.strip()
        return dict(zip(df['username'], df['level']))
    except Exception as e:
        print("Error fetching students levels:", e)
        return {}

# =====================================================================
# [ شاشة دخول الطالب - STUDENT_LOGIN_HTML ]
# =====================================================================
STUDENT_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دخول الطلبة | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Reenie+Beanie&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary-red: #e52421; --primary-gold: #ffd100; }
        * { box-sizing: border-box; }
        body { background: #fcfbf7; font-family: 'Cairo', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin:0; overflow-x: hidden; position: relative; padding: 15px; }
        .float-word { position: absolute; font-family: 'Reenie Beanie', cursive; font-size: 26px; color: rgba(0,0,0,0.06); font-weight: bold; pointer-events: none; z-index: 0; }
        .fw1 { top: 5%; left: 10%; transform: rotate(-12deg); font-size: 40px; color: rgba(229,36,33,0.08); }
        .fw2 { top: 8%; right: 12%; transform: rotate(8deg); font-size: 35px; }
        .fw3 { bottom: 12%; left: 8%; transform: rotate(5deg); font-size: 38px; color: rgba(255,209,0,0.15); }
        .fw4 { bottom: 8%; right: 10%; transform: rotate(-10deg); font-size: 32px; }
        .fw5 { top: 40%; left: 3%; transform: rotate(-20deg); font-size: 30px; }
        .fw6 { top: 35%; right: 5%; transform: rotate(15deg); font-size: 28px; }
        .fw7 { top: 60%; left: 5%; transform: rotate(10deg); font-size: 34px; color: rgba(229,36,33,0.06); }
        .fw8 { top: 70%; right: 8%; transform: rotate(-5deg); font-size: 30px; }
        .fw9 { top: 20%; left: 40%; transform: rotate(3deg); font-size: 22px; }
        .fw10 { bottom: 25%; right: 35%; transform: rotate(-8deg); font-size: 24px; }
        .doodle-container { position: absolute; display: flex; flex-direction: column; align-items: center; opacity: 0.65; z-index: 0; color: #333; }
        .doodle-container i { font-size: 38px; margin-bottom: 5px; color: #444; }
        .doodle-container span { font-family: 'Reenie Beanie', cursive; font-size: 28px; font-weight: bold; color: var(--primary-red); }
        .d-1 { top: 12%; left: 15%; animation: float 6s ease-in-out infinite; transform: rotate(-10deg); }
        .d-2 { bottom: 15%; right: 15%; animation: float 5s ease-in-out infinite reverse; transform: rotate(15deg); }
        .d-3 { bottom: 15%; left: 15%; animation: float 7s ease-in-out infinite; transform: rotate(-8deg); }
        .d-4 { top: 15%; right: 15%; animation: float 8s ease-in-out infinite; transform: rotate(12deg); }
        @keyframes float { 0% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-12px) rotate(3deg); } 100% { transform: translateY(0px) rotate(0deg); } }
        .card { background: white; padding: 32px 25px; border-radius: 15px; box-shadow: 5px 5px 0px rgba(0,0,0,0.05); border: 3px solid #333; text-align: center; width: 100%; max-width: 365px; margin: 15px auto; position: relative; z-index: 1; }
        .logo-img { width: 100px; height: auto; margin-bottom: 8px; border-radius: 50%; border: 3px solid var(--primary-gold); }
        h1 { color: #333; margin-bottom: 5px; font-size: 22px; font-weight: 900; }
        h1 .es-word { color: var(--primary-red); font-family: 'Reenie Beanie', cursive; font-size: 28px; }
        p.subtitle { color: #666; font-size: 13px; margin-bottom: 20px; }
        .input-group { position: relative; margin: 15px 0; }
        .input-group i.field-icon { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); color: #aaa; font-size: 16px; }
        input { width: 100%; padding: 12px 40px 12px 12px; border: 2px solid #333; border-radius: 8px; text-align: center; box-sizing: border-box; font-size: 15px; font-family: 'Cairo', sans-serif; transition: all 0.2s; }
        input[type="password"] { direction: ltr; text-align: center; font-family: 'Cairo', sans-serif; padding: 12px 40px 12px 12px; }
        input::placeholder { text-align: center; font-family: 'Cairo', sans-serif; }
        input:focus { border-color: var(--primary-red); outline: none; box-shadow: 3px 3px 0px rgba(229, 36, 33, 0.2); }
        button { width: 100%; padding: 12px; background: var(--primary-red); color: white; border: 2px solid #333; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; font-family: 'Cairo', sans-serif; transition: all 0.2s; margin-top: 10px; box-shadow: 3px 3px 0px #333; }
        button:hover { transform: translate(-2px, -2px); box-shadow: 5px 5px 0px #333; }
        .error { color: var(--primary-red); margin-bottom: 15px; font-size: 13px; font-weight: bold; background: #ffebeb; padding: 8px; border-radius: 5px; border: 1px solid var(--primary-red); }
        .lang-strip { display: flex; justify-content: center; gap: 20px; margin-top: 20px; padding-top: 15px; border-top: 2px dashed #eee; }
        .lang-strip .lang-item { text-align: center; }
        .lang-strip .es { font-family: 'Reenie Beanie', cursive; font-size: 22px; color: var(--primary-red); font-weight: bold; }
        .lang-strip .ar { font-size: 13px; color: #888; }
        .social-links { margin-top: 20px; display: flex; justify-content: center; gap: 15px; }
        .social-btn { display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; color: white; text-decoration: none; font-size: 18px; transition: 0.3s; border: 2px solid #333; box-shadow: 2px 2px 0px #333; }
        .social-btn:hover { transform: translateY(-3px); box-shadow: 4px 4px 0px #333; }
        .fb { background: #1877F2; } .ig { background: #E4405F; } .tt { background: #000000; } .wa { background: #25D366; }
        .teacher-link { display: inline-block; margin-top: 20px; color: #555; text-decoration: none; font-weight: bold; font-size: 14px; border-bottom: 2px dashed #ccc; padding-bottom: 2px; transition: 0.3s; }
        .teacher-link:hover { color: #e52421; border-color: #e52421; }
        @media (max-width: 500px) { .card { width: calc(100% - 24px); max-width: 340px; padding: 24px 16px; } .doodle-container { display: none; } }
    </style>
</head>
<body>
    <span class="float-word fw1">¡Hola!</span>
    <span class="float-word fw2">ازيك!</span>
    <span class="float-word fw3">Amigos</span>
    <span class="float-word fw4">صحاب</span>
    <span class="float-word fw5">Gracias</span>
    <span class="float-word fw6">شكراً</span>
    <span class="float-word fw7">Familia</span>
    <span class="float-word fw8">عيلة</span>
    <span class="float-word fw9">Bonito</span>
    <span class="float-word fw10">جميل</span>
    <div class="doodle-container d-1"><i class="fa-regular fa-sun"></i><span>Sol</span></div>
    <div class="doodle-container d-2"><i class="fa-solid fa-guitar"></i><span>Música</span></div>
    <div class="doodle-container d-3"><i class="fa-solid fa-pepper-hot"></i><span>Picante</span></div>
    <div class="doodle-container d-4"><i class="fa-regular fa-comment-dots"></i><span>¡Vamos!</span></div>
    <div class="card">
        <img src="/static/assets/logo.png" alt="Logo" class="logo-img" onerror="this.src='https://ui-avatars.com/api/?name=IA&background=ffd100&color=e52421'">
        <h1>بوابتك لـ <span class="es-word">Español</span> 👋</h1>
        <p class="subtitle">اكتب بياناتك ويالا بينا ع المنصة التعليمية</p>
        {% if error %} <div class="error"><i class="fa-solid fa-triangle-exclamation"></i> {{ error }}</div> {% endif %}
        <form method="POST">
            <div class="input-group">
                <i class="fa-solid fa-user field-icon"></i>
                <input type="text" name="username" placeholder="اسم المستخدم بتاعك | Usuario" required>
            </div>
            <div class="input-group">
                <i class="fa-solid fa-lock field-icon"></i>
                <input type="password" name="password" placeholder="كلمة المرور | Contraseña" required>
            </div>
            <button type="submit"><i class="fa-solid fa-arrow-right-to-bracket"></i> ادخل للمنصة | Entrar</button>
        </form>
        <a href="/teacher_login" class="teacher-link"><i class="fa-solid fa-chalkboard-user"></i> الدخول كمدرس | Acceso Profesores</a>
        <div class="lang-strip">
            <div class="lang-item"><span class="es" dir="ltr" style="display:inline-block;">¡Aprende!</span><br><span class="ar">اتعلم!</span></div>
            <div class="lang-item"><span class="es" dir="ltr" style="display:inline-block;">¡Habla!</span><br><span class="ar">اتكلم!</span></div>
            <div class="lang-item"><span class="es" dir="ltr" style="display:inline-block;">¡Practica!</span><br><span class="ar">اتمرن!</span></div>
        </div>
        <div class="social-links">
            <a href="https://www.facebook.com/institutoamigos1" target="_blank" class="social-btn fb"><i class="fab fa-facebook-f"></i></a>
            <a href="https://www.instagram.com/instituto_amigos1/" target="_blank" class="social-btn ig"><i class="fab fa-instagram"></i></a>
            <a href="https://www.tiktok.com/@espanolconamigos" target="_blank" class="social-btn tt"><i class="fab fa-tiktok"></i></a>
            <a href="https://wa.me/+201108425280" target="_blank" class="social-btn wa"><i class="fab fa-whatsapp"></i></a>
        </div>
    </div>
</body>
</html>
"""

# =====================================================================
# [ شاشة دخول المدرس - TEACHER_LOGIN_HTML ]
# =====================================================================
TEACHER_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دخول المدرسين | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { box-sizing: border-box; }
        body { background: #1a1a2e; color: white; font-family: 'Cairo', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin:0; padding: 15px; }
        .card { background: #16213e; padding: 32px 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 2px solid #0f3460; text-align: center; width: 100%; max-width: 365px; margin: 15px auto; }
        h1 { color: #f39c12; font-size: 24px; font-weight: 900; margin-bottom: 5px; }
        .input-group { margin: 15px 0; }
        input { width: 100%; padding: 12px; border: 2px solid #0f3460; background: #1a1a2e; color: white; border-radius: 8px; text-align: center; font-family: 'Cairo', sans-serif; }
        input[type="password"] { direction: ltr; text-align: center; font-family: 'Cairo', sans-serif; }
        input::placeholder { text-align: center; font-family: 'Cairo', sans-serif; }
        button { width: 100%; padding: 12px; background: #e67e22; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 10px; }
        .student-link { display: inline-block; margin-top: 20px; color: #aaa; text-decoration: none; font-size: 14px; transition: 0.3s; }
        .student-link:hover { color: #fff; }
        .error { color: #fff; margin-bottom: 15px; font-weight: bold; background: #e74c3c; padding: 8px; border-radius: 5px; }
        @media (max-width: 500px) { .card { width: calc(100% - 24px); max-width: 340px; padding: 24px 16px; } }
    </style>
</head>
<body>
    <div class="card">
        <i class="fa-solid fa-chalkboard-user" style="font-size: 50px; color: #f39c12; margin-bottom: 15px;"></i>
        <h1>بوابة المدرسين 👨‍🏫</h1>
        <p style="color: #aaa; margin-bottom: 25px;">أدخل بياناتك للوصول للوحة التحكم</p>
        {% if error %} <div class="error">{{ error }}</div> {% endif %}
        <form method="POST">
            <div class="input-group"><input type="text" name="username" placeholder="اسم المستخدم | Usuario" required></div>
            <div class="input-group"><input type="password" name="password" placeholder="كلمة المرور | Contraseña" required></div>
            <button type="submit">تسجيل الدخول | Entrar</button>
        </form>
        <a href="/" class="student-link"><i class="fa-solid fa-arrow-right"></i> رجوع لصفحة الطلبة | Volver</a>
    </div>
</body>
</html>
"""

# =====================================================================
# [ لوحة الطالب - DASHBOARD_HTML ]
# =====================================================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحتك التعليمية | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Reenie+Beanie&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #e52421; --primary-dark: #c31e1b; --accent: #ffd100; --secondary: #2c3e50; --bg-body: #f4f7f6; --text-main: #1e293b; --text-muted: #64748b; --vocab-color: #8e44ad; --shadow-color: #e67e22; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }
        body { background-color: var(--bg-body); color: var(--text-main); }
        .top-nav { background: white; padding: 12px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); position: sticky; top: 0; z-index: 100; }
        .top-right-container { display: flex; align-items: center; gap: 20px; }
        .user-buttons { display: flex; align-items: center; gap: 15px; }
        .logout-btn { display: flex; align-items: center; gap: 8px; background: #ffebeb; color: var(--primary); padding: 8px 18px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: 700; transition: 0.3s; }
        .logout-btn:hover { background: var(--primary); color: white; }
        .level-badge { background: #eef2f5; color: var(--secondary); padding: 8px 18px; border-radius: 50px; font-size: 13px; font-weight: 700; border: 1px solid #d1d9e0; }
        .brand-area { display: flex; align-items: center; gap: 15px; }
        .brand-area img { width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid var(--accent); }
        .brand-area h1 { font-size: 20px; font-weight: 900; color: var(--secondary); margin: 0; }
        .brand-area h1 span { color: var(--primary); }
        .main-content { max-width: 1200px; margin: 30px auto; padding: 0 15px; }
        .welcome-section { background: linear-gradient(135deg, var(--secondary) 0%, #1a2530 100%); color: white; padding: 40px; border-radius: 24px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; overflow: hidden; position: relative; }
        .welcome-section::before { content: "¡Hola!  Amigos  Español  ازيك  يلا بينا"; position: absolute; top: 0; left: 0; right: 0; bottom: 0; font-family: 'Reenie Beanie', cursive; font-size: 60px; color: rgba(255,255,255,0.03); display: flex; align-items: center; justify-content: center; letter-spacing: 30px; pointer-events: none; overflow: hidden; }
        .user-welcome-info { z-index: 1; }
        .user-welcome-info h2 { font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        .user-welcome-info h2 .es-greet { font-family: 'Reenie Beanie', cursive; color: var(--accent); font-size: 38px; }
        .user-welcome-info p { font-size: 16px; color: rgba(255,255,255,0.8); max-width: 500px; }
        .motivation-box { background: rgba(255, 209, 0, 0.15); border: 1px solid var(--accent); color: var(--accent); padding: 20px; border-radius: 16px; text-align: center; width: 300px; backdrop-filter: blur(5px); z-index: 1; }
        .motivation-boxes-wrap { display: flex; flex-direction: column; gap: 10px; width: 360px; max-width: 100%; z-index: 1; }
        .m-box { padding: 12px 16px; border-radius: 14px; backdrop-filter: blur(8px); display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 13.5px; line-height: 1.5; transition: 0.3s; }
        .m-box:hover { transform: translateY(-2px); }
        .m-ar { background: rgba(255, 255, 255, 0.95); color: var(--secondary); border-right: 4px solid var(--accent); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .m-es { background: rgba(229, 36, 33, 0.92); color: white; border-left: 4px solid var(--accent); box-shadow: 0 4px 15px rgba(229,36,33,0.25); text-align: left; }
        .m-icon { font-size: 18px; flex-shrink: 0; }
        .m-ar .m-icon { color: var(--primary); }
        .m-es .m-icon { color: var(--accent); }
        .tabs-nav { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 25px; background: white; padding: 12px; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); }
        .tab-trigger { background: none; border: 2px solid transparent; font-size: 13px; font-weight: 700; color: var(--text-muted); padding: 10px 16px; cursor: pointer; transition: 0.3s; border-radius: 12px; display: flex; align-items: center; gap: 6px; white-space: nowrap; }
        .tab-trigger:hover { background: #f0f3f5; border-color: #e2e8f0; }
        .tab-trigger.active { background: var(--primary); color: white; border-color: var(--primary); }
        .tab-content { display: none; animation: fadeIn 0.4s ease; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .section-header { display: flex; align-items: center; gap: 15px; margin-bottom: 20px; padding: 15px 20px; background: white; border-radius: 16px; border-right: 5px solid var(--primary); }
        .section-header.vocab-header { border-right-color: var(--vocab-color); }
        .section-header.schedule-header { border-right-color: var(--secondary); }
        .section-header.games-header { border-right-color: #2ecc71; }
        .section-header.shadow-header { border-right-color: var(--shadow-color); }
        .section-header .sec-icon { font-size: 28px; }
        .section-header .sec-title { font-size: 20px; font-weight: 800; color: var(--secondary); }
        .section-header .sec-subtitle { font-size: 13px; color: var(--text-muted); }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 20px; }
        .course-card { background: white; border-radius: 20px; overflow: hidden; border: 1px solid #f0f3f5; transition: 0.3s; display: flex; flex-direction: column; }
        .course-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .card-header { padding: 18px 20px; background: #fafbfc; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
        .lesson-number { font-size: 12px; font-weight: 800; padding: 5px 12px; border-radius: 50px; }
        .ln-red { color: var(--primary); background: rgba(229, 36, 33, 0.1); }
        .ln-gold { color: #b8860b; background: rgba(255, 209, 0, 0.2); }
        .ln-blue { color: var(--secondary); background: rgba(0,140,186,0.1); }
        .ln-green { color: #2ecc71; background: rgba(46,204,113,0.1); }
        .ln-purple { color: var(--vocab-color); background: rgba(142, 68, 173, 0.1); }
        .ln-orange { color: var(--shadow-color); background: rgba(230, 126, 34, 0.1); }
        .card-body { padding: 25px 20px; text-align: center; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .card-body h4 { font-size: 16px; font-weight: 800; color: var(--secondary); margin-bottom: 8px; }
        .card-action-btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; width: 100%; padding: 13px; text-decoration: none; border-radius: 12px; font-weight: 700; font-size: 14px; transition: 0.2s; }
        .card-action-btn:hover { filter: brightness(1.1); transform: translateY(-1px); }
        .btn-lecture { background: var(--primary); color: white; }
        .btn-exercise { background: var(--accent); color: var(--secondary); }
        .btn-schedule { background: var(--secondary); color: white; }
        .btn-game { background: #2ecc71; color: white; }
        .btn-vocab { background: var(--vocab-color); color: white; }
        .btn-shadow { background: var(--shadow-color); color: white; }
        .video-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 15px; }
        .video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
        .wheel-container-wrapper { background: white; padding: 35px 25px; border-radius: 24px; box-shadow: 0 12px 35px rgba(0,0,0,0.06); text-align: center; position: relative; }
        .wheel-header h3 { font-size: 24px; font-weight: 900; color: var(--secondary); margin-bottom: 8px; }
        .wheel-header p { font-size: 14px; color: var(--text-muted); }
        .wheel-pointer { position: absolute; top: -18px; left: 50%; transform: translateX(-50%); z-index: 10; font-size: 42px; color: #e52421; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); }
        .spin-btn { background: linear-gradient(135deg, var(--primary) 0%, #c31e1b 100%); color: white; border: none; padding: 16px 45px; font-size: 20px; font-weight: 900; border-radius: 50px; cursor: pointer; transition: 0.3s; box-shadow: 0 8px 20px rgba(229,36,33,0.3); display: inline-flex; align-items: center; gap: 10px; }
        .spin-btn:hover:not(:disabled) { transform: translateY(-3px) scale(1.02); box-shadow: 0 12px 25px rgba(229,36,33,0.4); }
        .spin-btn:disabled { background: #95a5a6; cursor: not-allowed; transform: none; box-shadow: none; }
        .winner-topic-card { background: linear-gradient(135deg, #fffcf0 0%, #fff9db 100%); border: 3px solid var(--accent); border-radius: 20px; padding: 25px; margin: 25px auto; max-width: 750px; box-shadow: 0 8px 25px rgba(255,209,0,0.2); animation: fadeInScale 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        @keyframes fadeInScale { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
        .winner-badge { display: inline-block; background: var(--secondary); color: var(--accent); font-weight: 800; font-size: 13px; padding: 6px 16px; border-radius: 50px; margin-bottom: 12px; }
        .winner-text { font-size: 22px; font-weight: 900; color: #1e293b; line-height: 1.6; margin: 10px 0 15px; }
        .timer-display { font-size: 18px; font-weight: 800; color: var(--primary); background: white; padding: 10px 20px; border-radius: 12px; display: inline-block; border: 1px solid #fee2e2; }
        .timer-display span { font-size: 24px; font-weight: 900; }
        
        .topic-recorder-animated { animation: fadeInSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
        @keyframes fadeInSlideUp {
            from { opacity: 0; transform: translateY(30px) scale(0.96); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .timer-display-box { background: #fff1f2; border: 2px solid #fecdd3; padding: 10px 24px; border-radius: 50px; display: inline-flex; align-items: center; gap: 12px; margin-top: 10px; }
        .timer-label { font-size: 15px; font-weight: 800; color: #991b1b; }
        .timer-digits { font-size: 26px; font-weight: 900; font-family: monospace; color: #e52421; }
        .timer-digits.running { animation: pulseTimer 1s infinite; }
        @keyframes pulseTimer { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        .success-banner { background: #d1fae5; color: #065f46; font-weight: 800; padding: 12px 18px; border-radius: 12px; margin-bottom: 18px; display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 14.5px; border: 1px solid #6ee7b7; }
        .after-record-buttons { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-top: 15px; }
        .btn-spin-again { background: linear-gradient(135deg, #8e44ad 0%, #6c3483 100%); color: white; box-shadow: 0 6px 16px rgba(142,68,173,0.3); }
        .btn-spin-again:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(142,68,173,0.4); }
        .pro-recorder-card { background: #1e293b; color: white; border-radius: 24px; padding: 30px; margin: 30px auto 10px; max-width: 750px; box-shadow: 0 15px 35px rgba(15,23,42,0.4); text-align: right; border: 1px solid #334155; }
        .recorder-header { display: flex; align-items: center; gap: 15px; border-bottom: 1px solid #334155; padding-bottom: 18px; margin-bottom: 22px; }
        .rec-icon { width: 50px; height: 50px; border-radius: 14px; background: rgba(229,36,33,0.15); color: #ef4444; display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0; }
        .rec-title h4 { font-size: 18px; font-weight: 900; color: white; margin: 0 0 4px; }
        .rec-title span { font-size: 13px; color: #94a3b8; }
        .recorder-visualizer { background: #0f172a; border-radius: 16px; padding: 18px 24px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #1e293b; margin-bottom: 22px; }
        .status-indicator { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 15px; }
        .status-dot { width: 12px; height: 12px; border-radius: 50%; background: #64748b; display: inline-block; transition: 0.3s; }
        .status-dot.active-rec { background: #ef4444; box-shadow: 0 0 12px #ef4444; animation: pulseRec 1s infinite; }
        @keyframes pulseRec { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.3); opacity: 0.6; } 100% { transform: scale(1); opacity: 1; } }
        .rec-timer { font-family: monospace; font-size: 26px; font-weight: 900; color: #38bdf8; }
        .recorder-actions { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-bottom: 15px; }
        .pro-btn { padding: 14px 28px; border-radius: 14px; font-size: 15px; font-weight: 800; border: none; cursor: pointer; transition: 0.3s; display: inline-flex; align-items: center; gap: 10px; }
        .btn-record { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; box-shadow: 0 6px 16px rgba(239,68,68,0.3); }
        .btn-record:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(239,68,68,0.4); }
        .btn-record:disabled { background: #475569; color: #94a3b8; cursor: not-allowed; box-shadow: none; }
        .btn-stop { background: #334155; color: white; border: 1px solid #475569; }
        .btn-stop:hover:not(:disabled) { background: #475569; transform: translateY(-2px); }
        .btn-stop:disabled { background: #1e293b; color: #475569; border-color: #334155; cursor: not-allowed; }
        .btn-reset { background: #d97706; color: white; }
        .btn-reset:hover { background: #b45309; transform: translateY(-2px); }
        .playback-area { background: #0f172a; padding: 20px; border-radius: 16px; margin-top: 20px; border: 1px dashed #334155; text-align: center; }
        .custom-audio-player { width: 100%; height: 45px; margin-bottom: 15px; }
        .pro-download-btn { display: inline-flex; align-items: center; gap: 10px; background: #10b981; color: white; text-decoration: none; padding: 12px 26px; border-radius: 12px; font-weight: 800; font-size: 14px; transition: 0.3s; box-shadow: 0 4px 14px rgba(16,185,129,0.3); }
        .pro-download-btn:hover { background: #059669; transform: translateY(-2px); }
        @media (max-width: 768px) {
            .welcome-section { flex-direction: column; text-align: center; gap: 20px; padding: 25px 20px; }
            .motivation-boxes-wrap { width: 100%; max-width: 400px; margin: 0 auto; }
            .top-nav { flex-direction: column; gap: 15px; padding: 15px; text-align: center; }
            .tabs-nav { justify-content: center; overflow-x: auto; flex-wrap: nowrap; padding: 10px; }
            .tab-trigger { flex-shrink: 0; }
            .cards-grid { grid-template-columns: 1fr; gap: 15px; }
            .wheel-container-wrapper { padding: 20px 15px; }
            .pro-recorder-card { padding: 20px 15px; }
        }
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="top-right-container">
            <div class="user-buttons">
                <a href="/logout" class="logout-btn"><i class="fa-solid fa-arrow-right-from-bracket"></i> خروج</a>
                <span class="level-badge"><i class="fa-solid fa-graduation-cap"></i> مستواك: {{ student.level }}</span>
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
            <div class="motivation-boxes-wrap">
                <div class="m-box m-ar">
                    <i class="fa-solid fa-quote-right m-icon"></i>
                    <span>{{ quote.ar if quote is mapping else quote }}</span>
                </div>
                <div class="m-box m-es" dir="ltr">
                    <i class="fa-solid fa-quote-left m-icon"></i>
                    <span>{{ quote.es if quote is mapping else "" }}</span>
                </div>
            </div>
        </header>

        <nav class="tabs-nav">
            <button class="tab-trigger active" onclick="switchTab(event, 'lectures-tab')"><i class="fa-solid fa-video"></i> الدروس | Lecciones</button>
            <button class="tab-trigger" onclick="switchTab(event, 'exercises-tab')"><i class="fa-solid fa-pen-ruler"></i> التمارين | Ejercicios</button>
            <button class="tab-trigger" onclick="switchTab(event, 'vocab-tab')"><i class="fa-solid fa-spell-check"></i> الكلمات | Vocabulario</button>
            <button class="tab-trigger" onclick="switchTab(event, 'schedule-tab')"><i class="fa-solid fa-calendar-days"></i> الجداول | Planes</button>
            <button class="tab-trigger" onclick="switchTab(event, 'shadowing-tab')"><i class="fa-solid fa-headphones"></i> الشادوينج | Shadowing</button>
            <button class="tab-trigger" onclick="switchTab(event, 'games-tab')"><i class="fa-solid fa-gamepad"></i> الألعاب | Juegos</button>
            <button class="tab-trigger" onclick="switchTab(event, 'videos-tab')"><i class="fa-brands fa-youtube"></i> فيديوهات | Videos</button>
            <button class="tab-trigger" onclick="switchTab(event, 'wheel-tab')"><i class="fa-solid fa-dharmachakra"></i> العجلة | Rueda</button>
        </nav>

        <div id="lectures-tab" class="tab-content active">
            <div class="section-header">
                <i class="fa-solid fa-book-open sec-icon" style="color: var(--primary);"></i>
                <div><div class="sec-title">الدروس والشرح</div></div>
            </div>
            <div class="cards-grid">
                {% for item in lessons_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number ln-red">Unidad {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn btn-lecture" target="_blank"><span>ابدأ الشرح</span> <span style="opacity: 0.9; font-size: 0.95em; font-family: sans-serif;">| Empezar Lección</span></a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="exercises-tab" class="tab-content">
            <div class="section-header">
                <i class="fa-solid fa-pen-ruler sec-icon" style="color: #b8860b;"></i>
                <div><div class="sec-title">التمارين والتقييم</div></div>
            </div>
            <div class="cards-grid">
                {% for item in exercises_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number ln-gold">Ejercicio {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn btn-exercise" target="_blank"><span>ابدأ التمرين</span> <span style="opacity: 0.9; font-size: 0.95em; font-family: sans-serif;">| Empezar Ejercicio</span></a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="vocab-tab" class="tab-content">
            <div class="section-header vocab-header">
                <i class="fa-solid fa-language sec-icon" style="color: var(--vocab-color);"></i>
                <div><div class="sec-title">📖 الكلمات</div></div>
            </div>
            <div class="cards-grid">
                {% for item in vocab_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number ln-purple">الدرس {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn btn-vocab" target="_blank"><span>افتح الكلمات</span> <span style="opacity: 0.9; font-size: 0.95em; font-family: sans-serif;">| Vocabulario</span></a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="schedule-tab" class="tab-content">
            <div class="section-header schedule-header">
                <i class="fa-solid fa-calendar-check sec-icon" style="color: var(--secondary);"></i>
                <div><div class="sec-title">الجداول</div></div>
            </div>
            <div class="cards-grid">
                {% for item in schedules_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number ln-blue">الجدول {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn btn-schedule" target="_blank"><span>افتح الجدول</span> <span style="opacity: 0.9; font-size: 0.95em; font-family: sans-serif;">| Plan de Estudio</span></a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="shadowing-tab" class="tab-content">
            <div class="section-header shadow-header">
                <i class="fa-solid fa-headphones sec-icon" style="color: var(--shadow-color);"></i>
                <div><div class="sec-title">الشادوينج</div></div>
            </div>
            <div class="cards-grid">
                {% for item in shadowing_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number ln-orange">الدرس {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn btn-shadow" target="_blank"><span>ابدأ الشادوينج</span> <span style="opacity: 0.9; font-size: 0.95em; font-family: sans-serif;">| Shadowing</span></a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="games-tab" class="tab-content">
            <div class="section-header games-header">
                <i class="fa-solid fa-puzzle-piece sec-icon" style="color: #2ecc71;"></i>
                <div><div class="sec-title">الألعاب</div></div>
            </div>
            <div class="cards-grid">
                {% for item in games_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number ln-green">لعبة {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn btn-game" target="_blank"><span>ادخل العب</span> <span style="opacity: 0.9; font-size: 0.95em; font-family: sans-serif;">| Jugar</span></a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="videos-tab" class="tab-content">
            <div class="section-header">
                <i class="fa-brands fa-youtube sec-icon" style="color: #ff0000;"></i>
                <div><div class="sec-title">الفيديوهات</div></div>
            </div>
            <div class="cards-grid">
                {% for video in videos_list %}
                <div class="course-card" style="padding: 15px;">
                    <div class="video-container">
                        <iframe src="https://www.youtube.com/embed/{{ video.youtube_id }}" allowfullscreen></iframe>
                    </div>
                    <h4 style="margin-top: 15px;">{{ video.title }}</h4>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="wheel-tab" class="tab-content">
            <div class="wheel-container-wrapper">
                <div class="wheel-header">
                    <h3><i class="fa-solid fa-dharmachakra" style="color: var(--primary);"></i> عجلة التحدث التفاعلية | Rueda de Conversación</h3>
                    <p id="wheelSubtitle">اضغط على زر الدوران لاختيار موضوع عشوائي للتحدث، ثم سجل إجابتك بصوتك!</p>
                </div>
                
                <!-- 1. العجلة الدوارة -->
                <div id="wheelSpinSection">
                    <div class="wheel-canvas-area" style="position: relative; margin: 25px auto; width: 380px; max-width: 100%;">
                        <div class="wheel-pointer"><i class="fa-solid fa-caret-down"></i></div>
                        <canvas id="wheelCanvas" width="380" height="380" style="max-width: 100%; height: auto; border-radius: 50%; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 6px solid #2c3e50; background: white;"></canvas>
                    </div>

                    <div style="text-align: center; margin-bottom: 25px;">
                        <button id="spinBtn" class="spin-btn" onclick="startWheelSpin()"><i class="fa-solid fa-rotate-right"></i> لف العجلة | ¡Girar Rueda!</button>
                    </div>
                </div>

                <!-- 2. كارت الموضوع واستوديو التسجيل (يظهر مكان العجلة بانيميشن بعد توقفها) -->
                <div id="topicAndRecorderSection" class="topic-recorder-animated" style="display: none;">
                    <div class="winner-topic-card">
                        <div class="winner-badge">🎯 الموضوع المختار لتحدي التحدث | Tema Seleccionado</div>
                        <div id="winnerTopicText" class="winner-text"></div>
                        <div class="timer-display-box">
                            <span class="timer-label">⏱️ الوقت المقترح للتحدث:</span>
                            <span id="speakingTimerEl" class="timer-digits">02:00</span>
                        </div>
                    </div>

                    <div class="pro-recorder-card">
                        <div class="recorder-header">
                            <div class="rec-icon"><i class="fa-solid fa-studio-vinari"></i></div>
                            <div class="rec-title">
                                <h4>استوديو التسجيل الصوتي | Estudio de Grabación</h4>
                                <span>اضغط على (ابدأ التسجيل) ليبدأ عداد الوقت وميكروفون التسجيل</span>
                            </div>
                        </div>

                        <div class="recorder-visualizer">
                            <div class="status-indicator">
                                <span class="status-dot" id="statusDot"></span>
                                <span id="recStatusText">جاهز للتسجيل، اضغط الزر أدناه | Listo para grabar</span>
                            </div>
                            <div class="rec-timer" id="recTimerText">00:00</div>
                        </div>

                        <div class="recorder-actions">
                            <button id="startRecordBtn" onclick="startRecording()" class="pro-btn btn-record">
                                <i class="fa-solid fa-microphone"></i> <span>ابدأ التسجيل | Grabar</span>
                            </button>
                            <button id="stopRecordBtn" onclick="stopRecording()" class="pro-btn btn-stop" disabled>
                                <i class="fa-solid fa-square"></i> <span>إيقاف وحفظ | Detener</span>
                            </button>
                        </div>

                        <div id="playbackArea" class="playback-area" style="display: none;">
                            <div class="success-banner">
                                <i class="fa-solid fa-circle-check"></i> تم حفظ التسجيل وإيقاف العداد! يمكنك الاستماع أو التحميل أو لف العجلة مرة أخرى.
                            </div>
                            <audio id="audioPlayback" controls class="custom-audio-player"></audio>
                            <div class="after-record-buttons">
                                <a id="downloadRecordBtn" href="#" download="mi_respuesta_espanol.webm" class="pro-download-btn">
                                    <i class="fa-solid fa-cloud-arrow-down"></i> تحميل المقطع الصوتي | Descargar Audio
                                </a>
                                <button onclick="resetToSpinAgain()" class="pro-btn btn-spin-again">
                                    <i class="fa-solid fa-rotate-right"></i> لف العجلة لموضوع جديد | ¡Girar de Nuevo!
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function switchTab(evt, tabId) {
            document.querySelectorAll(".tab-content").forEach(el => el.classList.remove("active"));
            document.querySelectorAll(".tab-trigger").forEach(el => el.classList.remove("active"));
            document.getElementById(tabId).classList.add("active");
            evt.currentTarget.classList.add("active");
            if(tabId === 'wheel-tab') {
                setTimeout(drawWheel, 50);
            }
        }
        const levelTopics = {{ topics_json | safe }};
        const colorsPalette = ["#e52421", "#f39c12", "#2ecc71", "#2980b9", "#8e44ad", "#16a085", "#d35400", "#27ae60", "#c0392b", "#2c3e50"];
        let wheelAngle = 0;
        let isSpinningWheel = false;

        function drawWheel() {
            const canvas = document.getElementById("wheelCanvas");
            if (!canvas) return;
            const ctx = canvas.getContext("2d");
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const radius = centerX - 10;
            const numSlices = levelTopics.length;
            const sliceAngle = (2 * Math.PI) / numSlices;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < numSlices; i++) {
                const startAngle = wheelAngle + i * sliceAngle;
                const endAngle = startAngle + sliceAngle;

                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, startAngle, endAngle);
                ctx.closePath();
                ctx.fillStyle = colorsPalette[i % colorsPalette.length];
                ctx.fill();
                ctx.lineWidth = 2;
                ctx.strokeStyle = "#ffffff";
                ctx.stroke();

                ctx.save();
                ctx.translate(centerX, centerY);
                ctx.rotate(startAngle + sliceAngle / 2);
                ctx.textAlign = "right";
                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 15px Cairo, sans-serif";
                
                let textLabel = "موضوع " + (i + 1);
                ctx.fillText(textLabel, radius - 20, 5);
                ctx.restore();
            }

            ctx.beginPath();
            ctx.arc(centerX, centerY, 28, 0, 2 * Math.PI);
            ctx.fillStyle = "#ffffff";
            ctx.fill();
            ctx.lineWidth = 5;
            ctx.strokeStyle = "#2c3e50";
            ctx.stroke();
        }

        function startWheelSpin() {
            if (isSpinningWheel) return;
            isSpinningWheel = true;
            const btn = document.getElementById("spinBtn");
            btn.disabled = true;
            document.getElementById("winnerTopicCard").style.display = "none";

            let duration = 4000;
            let startTime = null;
            let initialAngle = wheelAngle;
            let totalSpin = (Math.PI * 2) * (5 + Math.random() * 5);

            function animateSpin(timestamp) {
                if (!startTime) startTime = timestamp;
                let elapsed = timestamp - startTime;
                let progress = Math.min(elapsed / duration, 1);
                
                let easeOut = 1 - Math.pow(1 - progress, 3);
                wheelAngle = initialAngle + totalSpin * easeOut;
                drawWheel();

                if (progress < 1) {
                    requestAnimationFrame(animateSpin);
                } else {
                    isSpinningWheel = false;
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> لفة جديدة | ¡Girar de nuevo!';
                    determineWinner();
                }
            }
            requestAnimationFrame(animateSpin);
        }

        let speakingTimerInterval = null;
        let remainingSeconds = 120;

        function determineWinner() {
            const numSlices = levelTopics.length;
            const sliceAngle = (2 * Math.PI) / numSlices;
            
            let normalizedAngle = wheelAngle % (2 * Math.PI);
            if (normalizedAngle < 0) normalizedAngle += 2 * Math.PI;
            
            let pointerAngle = (3 * Math.PI / 2 - normalizedAngle) % (2 * Math.PI);
            if (pointerAngle < 0) pointerAngle += 2 * Math.PI;

            let winningIndex = Math.floor(pointerAngle / sliceAngle) % numSlices;
            let winningTopic = levelTopics[winningIndex];

            // 1. إخفاء العجلة وزر الدوران
            document.getElementById("wheelSpinSection").style.display = "none";
            document.getElementById("wheelSubtitle").style.display = "none";

            // 2. إظهار الموضوع المختار واستوديو التسجيل مكان العجلة بانيميشن
            document.getElementById("winnerTopicText").innerText = winningTopic;
            document.getElementById("topicAndRecorderSection").style.display = "block";

            // تجهيز العدادات (لا يبدأ التايمر إلا عند الضغط على ابدأ التسجيل)
            remainingSeconds = 120;
            updateSpeakingTimerDisplay(120);
            document.getElementById("speakingTimerEl").classList.remove("running");
            clearInterval(speakingTimerInterval);
            document.getElementById("playbackArea").style.display = "none";
            document.getElementById("startRecordBtn").disabled = false;
            document.getElementById("startRecordBtn").style.display = "inline-flex";
            document.getElementById("stopRecordBtn").disabled = true;
            document.getElementById("stopRecordBtn").style.display = "inline-flex";
            document.getElementById("recStatusText").innerText = "جاهز للتسجيل، اضغط الزر أدناه لبدء التايمر | Listo para grabar";
            document.getElementById("recTimerText").innerText = "00:00";
            document.getElementById("statusDot").classList.remove("active-rec");
        }

        function updateSpeakingTimerDisplay(sec) {
            let m = Math.floor(sec / 60);
            let s = sec % 60;
            document.getElementById("speakingTimerEl").textContent = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
        }

        window.addEventListener("DOMContentLoaded", () => { drawWheel(); });

        let mediaRecorder;
        let audioChunks = [];
        let recInterval;
        let recSeconds = 0;

        async function startRecording() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = event => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    // إيقاف التايمر والعداد فوراً عند الضغط على إيقاف
                    clearInterval(recInterval);
                    clearInterval(speakingTimerInterval);
                    document.getElementById("speakingTimerEl").classList.remove("running");

                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audioPlayback = document.getElementById("audioPlayback");
                    const downloadBtn = document.getElementById("downloadRecordBtn");
                    audioPlayback.src = audioUrl;
                    document.getElementById("playbackArea").style.display = "block";
                    downloadBtn.href = audioUrl;
                    document.getElementById("recStatusText").innerText = "تم حفظ الإجابة وإيقاف العداد | Grabación completada";
                    document.getElementById("statusDot").classList.remove("active-rec");
                    
                    document.getElementById("startRecordBtn").style.display = "none";
                    document.getElementById("stopRecordBtn").style.display = "none";
                };

                mediaRecorder.start();
                
                // بدء عداد التسجيل وتايمر التحدث الآن معاً!
                recSeconds = 0;
                document.getElementById("recTimerText").innerText = "00:00";
                clearInterval(recInterval);
                recInterval = setInterval(() => {
                    recSeconds++;
                    let rm = Math.floor(recSeconds / 60);
                    let rs = recSeconds % 60;
                    document.getElementById("recTimerText").innerText = (rm < 10 ? "0" + rm : rm) + ":" + (rs < 10 ? "0" + rs : rs);
                }, 1000);

                clearInterval(speakingTimerInterval);
                document.getElementById("speakingTimerEl").classList.add("running");
                speakingTimerInterval = setInterval(() => {
                    if (remainingSeconds > 0) {
                        remainingSeconds--;
                        updateSpeakingTimerDisplay(remainingSeconds);
                    } else {
                        clearInterval(speakingTimerInterval);
                        document.getElementById("speakingTimerEl").textContent = "انتهى الوقت!";
                        stopRecording();
                    }
                }, 1000);

                document.getElementById("startRecordBtn").disabled = true;
                document.getElementById("stopRecordBtn").disabled = false;
                document.getElementById("playbackArea").style.display = "none";
                document.getElementById("recStatusText").innerText = "جاري التسجيل والعد التنازلي الآن... | Grabando en curso...";
                document.getElementById("statusDot").classList.add("active-rec");
            } catch (err) {
                alert("يرجى السماح للمتصفح بالوصول للميكروفون لبدء التسجيل الصوتي.");
                console.error("Mic error:", err);
            }
        }

        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state !== "inactive") {
                mediaRecorder.stop();
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
                document.getElementById("startRecordBtn").disabled = false;
                document.getElementById("stopRecordBtn").disabled = true;
            }
        }

        function resetToSpinAgain() {
            if (mediaRecorder && mediaRecorder.state !== "inactive") {
                mediaRecorder.stop();
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
            }
            clearInterval(recInterval);
            clearInterval(speakingTimerInterval);

            document.getElementById("topicAndRecorderSection").style.display = "none";
            document.getElementById("wheelSpinSection").style.display = "block";
            document.getElementById("wheelSubtitle").style.display = "block";
            setTimeout(drawWheel, 20);
        }
    </script>
</body>
</html>
"""

# =====================================================================
# [ لوحة المدرس - TEACHER_DASHBOARD_HTML ]
# =====================================================================
TEACHER_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة المدرس | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Cairo', sans-serif; }
        body { background: #f4f7f6; color: #333; }
        .top-nav { background: #1a1a2e; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .brand { font-size: 20px; font-weight: 900; color: #f39c12; }
        .user-actions a { color: white; text-decoration: none; background: #e74c3c; padding: 8px 15px; border-radius: 8px; font-weight: bold; }
        .main-tabs { display: flex; justify-content: center; gap: 20px; background: white; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 30px; flex-wrap: wrap; }
        .m-tab { background: none; border: none; font-size: 18px; font-weight: bold; color: #555; padding: 10px 20px; cursor: pointer; border-bottom: 3px solid transparent; transition: 0.3s; }
        .m-tab.active { color: #1a1a2e; border-color: #f39c12; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 15px 80px; }
        .level-selector { background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .level-selector select { padding: 10px 20px; font-size: 16px; border: 2px solid #ccc; border-radius: 8px; font-weight: bold; }
        .content-tabs { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; justify-content: center; }
        .c-tab { background: white; border: 1px solid #ddd; padding: 8px 15px; border-radius: 8px; cursor: pointer; font-weight: bold; color: #555; }
        .c-tab.active { background: #f39c12; color: white; border-color: #f39c12; }
        .c-tab.multi-games { background: #8e44ad; color: white; border-color: #8e44ad; }
        .c-tab.multi-games.active { background: #9b59b6; box-shadow: 0 0 10px rgba(142, 68, 173, 0.5); }
        .c-section { display: none; }
        .tab-section { display: none; }
        .tab-section.active { display: block; animation: fadeIn 0.3s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 20px; margin-top: 15px; }
        .course-card { background: white; border-radius: 15px; border: 1px solid #eee; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.03); text-align: center; cursor: pointer; transition: 0.3s; }
        .course-card:hover { transform: translateY(-3px); border-color: #f39c12; }
        .course-card .header { background: #f8f9fa; padding: 15px; font-weight: bold; color: #1a1a2e; border-bottom: 1px solid #eee; }
        .course-card .body { padding: 20px; }
        .course-card a, .action-btn { display: inline-block; width: 100%; padding: 10px; background: #f39c12; color: #1a1a2e; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 10px; border: none; cursor: pointer; }
        .course-card a.multi-btn { background: #8e44ad; color: white; }
        .grading-section { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); min-height: 400px; }
        .badge { padding: 4px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; margin-left: 5px; }
        .badge.pending { background: #ffeaa7; color: #d35400; }
        .back-btn { padding: 8px 15px; background: #95a5a6; color: white; border: none; border-radius: 5px; cursor: pointer; margin-bottom: 15px; font-weight: bold; transition: 0.3s; }
        .back-btn:hover { background: #7f8c8d; }
        .schedule-table { width: 100%; border-collapse: collapse; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        .schedule-table th { background: #1a1a2e; color: white; padding: 15px; text-align: center; font-size: 15px; }
        .schedule-table td { padding: 15px; border-bottom: 1px solid #eee; text-align: center; font-weight: 600; color: #333; }
        .schedule-table tr:hover { background: #f8fafc; }
        @media (max-width: 768px) {
            .top-nav { flex-direction: column; gap: 15px; text-align: center; }
            .main-tabs { flex-direction: column; gap: 10px; }
            .m-tab { width: 100%; text-align: center; }
        }
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="brand"><i class="fa-solid fa-chalkboard-user"></i> لوحة المدرس</div>
        <div class="user-actions">
            <span style="margin-left: 15px;">أهلاً يا <strong>{{ teacher.username }}</strong></span>
            <a href="/logout">خروج</a>
        </div>
    </nav>

    <div class="main-tabs">
        <button class="m-tab active" onclick="switchMainTab('materials', this)"><i class="fa-solid fa-book"></i> المناهج والمواد | Materiales</button>
        <button class="m-tab" onclick="switchMainTab('grading', this); refreshGradingData();"><i class="fa-solid fa-check-double"></i> تصحيح الواجبات | Tareas</button>
        <button class="m-tab" onclick="switchMainTab('leaderboard', this); loadProgressData();"><i class="fa-solid fa-ranking-star"></i> تقدم الطلبة | Progreso</button>
    </div>

    <div class="container">
        <!-- ===== قسم المواد والمناهج ===== -->
        <div id="materials-view" class="tab-section active">
            <div class="level-selector">
                <label style="font-weight: bold; font-size: 18px;">اختر المستوى:</label><br><br>
                <select id="levelSelect" onchange="window.location.href='/teacher_dashboard?level=' + this.value">
                    <option value="">-- اختر المستوى --</option>
                    <option value="demo" {% if current_level == 'demo' %}selected{% endif %}>مستوى تجريبي (Demo)</option>
                    <option value="A1.1" {% if current_level == 'A1.1' %}selected{% endif %}>مستوى A1.1</option>
                    <option value="A1.2" {% if current_level == 'A1.2' %}selected{% endif %}>مستوى A1.2</option>
                    <option value="A1.3" {% if current_level == 'A1.3' %}selected{% endif %}>مستوى A1.3</option>
                    <option value="A2.1" {% if current_level == 'A2.1' %}selected{% endif %}>مستوى A2.1</option>
                    <option value="A2.2" {% if current_level == 'A2.2' %}selected{% endif %}>مستوى A2.2</option>
                    <option value="A2.3" {% if current_level == 'A2.3' %}selected{% endif %}>مستوى A2.3</option>
                    <option value="B1.1" {% if current_level == 'B1.1' %}selected{% endif %}>مستوى B1.1</option>
                    <option value="B1.2" {% if current_level == 'B1.2' %}selected{% endif %}>مستوى B1.2</option>
                    <option value="B1.3" {% if current_level == 'B1.3' %}selected{% endif %}>مستوى B1.3</option>
                    <option value="B2.1" {% if current_level == 'B2.1' %}selected{% endif %}>مستوى B2.1</option>
                    <option value="B2.2" {% if current_level == 'B2.2' %}selected{% endif %}>مستوى B2.2</option>
                    <option value="B2.3" {% if current_level == 'B2.3' %}selected{% endif %}>مستوى B2.3</option>
                </select>
            </div>

            {% if current_level %}
            <div class="content-tabs">
                <button class="c-tab active" onclick="switchContentTab('lectures')">الدروس | Lecciones</button>
                <button class="c-tab" onclick="switchContentTab('exercises')">التمارين | Ejercicios</button>
                <button class="c-tab" onclick="switchContentTab('vocab')">الكلمات | Vocabulario</button>
                <button class="c-tab" onclick="switchContentTab('schedules')">الجداول | Planes</button>
                <button class="c-tab" onclick="switchContentTab('shadowing')">الشادوينج | Shadowing</button>
                <button class="c-tab" onclick="switchContentTab('games')">الألعاب الفردية | Juegos</button>
                <button class="c-tab multi-games" onclick="switchContentTab('multiplayer')"><i class="fa-solid fa-users"></i> ألعاب جماعية | Multijugador</button>
            </div>

            <div id="lectures" class="c-section active" style="display: block;">
                <div class="cards-grid">
                    {% for item in materials.lessons %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الدرس | Abrir Lección</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div id="exercises" class="c-section" style="display: none;">
                <div class="cards-grid">
                    {% for item in materials.exercises %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح التمرين | Abrir Ejercicio</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="vocab" class="c-section" style="display: none;">
                <div class="cards-grid">
                    {% for item in materials.vocab %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الكلمات | Abrir Vocabulario</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="schedules" class="c-section" style="display: none;">
                <div class="cards-grid">
                    {% for item in materials.schedules %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الجدول | Abrir Plan</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="shadowing" class="c-section" style="display: none;">
                <div class="cards-grid">
                    {% for item in materials.shadowing %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الشادوينج | Abrir Shadowing</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="games" class="c-section" style="display: none;">
                <div class="cards-grid">
                    {% for item in materials.games %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح اللعبة | Abrir Juego</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="multiplayer" class="c-section" style="display: none;">
                <div class="cards-grid">
                    {% for item in materials.multi_games %}
                    <div class="course-card" style="border-color: #8e44ad;">
                        <div class="header" style="background: #f4ecf7; color: #8e44ad;">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank" class="multi-btn">تشغيل اللعبة <i class="fa-solid fa-play"></i> | Iniciar</a></div>
                    </div>
                    {% else %}
                    <p style="text-align: center; width: 100%; color: #888;">لا توجد ألعاب جماعية حالياً.</p>
                    {% endfor %}
                </div>
            </div>
            {% else %}
            <p style="text-align: center; color: #777; font-size: 18px;">يرجى اختيار المستوى لعرض المحتوى.</p>
            {% endif %}
        </div>

        <!-- ===== قسم تصحيح الواجبات ===== -->
        <div id="grading-view" class="tab-section grading-section">
            <h2 style="color: #f39c12; margin-bottom: 15px;"><i class="fa-solid fa-file-pen"></i> تصحيح الواجبات لمستوى ({{ current_level or 'الرجاء اختياره من الأعلى' }})</h2>
            
            <div id="studentsListView">
                {% if current_level %}
                <button onclick="refreshGradingData()" style="padding: 8px 15px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer;">🔄 تحديث القائمة</button>
                <div id="studentsListContent" class="cards-grid">جاري التحميل...</div>
                {% else %}
                <p style="text-align: center; color: #777;">اختر المستوى من القائمة العلوية أولاً لتظهر واجبات طلبة هذا المستوى.</p>
                {% endif %}
            </div>

            <div id="studentLessonsView" style="display: none;">
                <button onclick="backToStudentsList()" class="back-btn">⬅️ رجوع لقائمة الطلبة</button>
                <div id="studentLessonsContent"></div>
            </div>
        </div>

        <!-- ===== قسم تقدم الطلبة ===== -->
        <div id="leaderboard-view" class="tab-section grading-section">
            <h2 style="color: #f39c12; margin-bottom: 15px;"><i class="fa-solid fa-ranking-star"></i> تقدم الطلبة (Leaderboard) لمستوى ({{ current_level }})</h2>
            <button onclick="loadProgressData()" style="padding: 8px 15px; background: #e67e22; color: white; border: none; border-radius: 5px; cursor: pointer; margin-bottom: 15px;">🔄 تحديث البيانات</button>
            <div style="overflow-x: auto;">
                <table class="schedule-table">
                    <thead>
                        <tr>
                            <th>الطالب</th>
                            <th>✅ إجابات صحيحة</th>
                            <th>❌ إجابات خاطئة</th>
                            <th>⏳ بانتظار التصحيح</th>
                            <th>🎯 النسبة المئوية</th>
                            <th>🕒 آخر تحديث</th>
                        </tr>
                    </thead>
                    <tbody id="leaderboardContent">
                        <tr><td colspan="6">اضغط على تحديث البيانات لجلب القائمة... ⏳</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // بيانات من الخادم
        const SCRIPT_URL = '{{ script_url }}';
        const CURRENT_LEVEL = '{{ current_level }}';
        const studentsLevelsMap = {{ students_levels_json | safe }};
        const exercisesList = {{ materials.exercises | tojson | safe if materials else '[]' }};

        // بيانات الواجبات المؤقتة
        let allPendingData = [];
        let currentSelectedUsername = "";

        // التحويل بين التبويبات الرئيسية
        function switchMainTab(tab, btn) {
            document.querySelectorAll('.m-tab').forEach(b => b.classList.remove('active'));
            if(btn) btn.classList.add('active');
            document.querySelectorAll('.tab-section').forEach(s => s.classList.remove('active'));
            document.getElementById(tab + '-view').classList.add('active');
        }

        // التحويل بين تبويبات المحتوى
        function switchContentTab(tabId) {
            document.querySelectorAll('.c-tab').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.c-section').forEach(s => s.style.display = 'none');
            if(document.getElementById(tabId)) document.getElementById(tabId).style.display = 'block';
        }

        // ================= جلب بيانات التصحيح =================
        async function refreshGradingData() {
            if (!CURRENT_LEVEL) return;
            const container = document.getElementById('studentsListContent');
            container.innerHTML = '<p>جاري التحميل من الخادم... ⏳</p>';
            try {
                const res = await fetch(SCRIPT_URL + '?action=getPendingReviews&_t=' + Date.now());
                const data = await res.json();
                if (data.status === 'success') {
                    allPendingData = (data.students || []).filter(s => {
                        return studentsLevelsMap[s.username] === CURRENT_LEVEL;
                    });
                    renderStudentsList();
                }
            } catch (err) {
                container.innerHTML = '<p>❌ خطأ في تحميل البيانات</p>';
            }
        }

        // عرض قائمة الطلبة
        function renderStudentsList() {
            const container = document.getElementById('studentsListContent');
            if(allPendingData.length === 0) {
                container.innerHTML = '<p style="color: green; font-weight: bold; font-size: 18px;">✅ ممتاز! لا توجد واجبات بانتظار التصحيح لهذا المستوى.</p>';
                return;
            }

            const grouped = {};
            allPendingData.forEach(s => {
                if(!grouped[s.username]) {
                    grouped[s.username] = { fullName: s.fullName || s.username, lessons: [], totalPending: 0 };
                }
                grouped[s.username].lessons.push(s);
                grouped[s.username].totalPending += s.pendingCount;
            });

            let html = '';
            Object.keys(grouped).forEach(username => {
                const student = grouped[username];
                html += `
                <div class="course-card" onclick="showStudentLessons('${username}')">
                    <div class="header" style="background: #eef2f5;"><i class="fa-solid fa-user-graduate"></i> الطالب: ${student.fullName}</div>
                    <div class="body">
                        <p style="color: #7f8c8d; margin-bottom: 10px;">الدروس المتاحة للتقييم: <strong>${student.lessons.length}</strong></p>
                        <span class="badge pending">⏳ ${student.totalPending} سؤال بانتظار التصحيح</span>
                        <button class="action-btn" style="margin-top: 15px; background: #3498db; color: white;">عرض واجبات الطالب</button>
                    </div>
                </div>`;
            });
            container.innerHTML = html;
        }

        // عرض واجبات طالب معين وفتح الرابط الدقيق بناءً على البيانات
        function showStudentLessons(username) {
            currentSelectedUsername = username;
            document.getElementById('studentsListView').style.display = 'none';
            document.getElementById('studentLessonsView').style.display = 'block';
            
            const container = document.getElementById('studentLessonsContent');
            const studentData = allPendingData.filter(s => s.username === username);
            
            let html = `<h3 style="margin-bottom: 20px; color: var(--secondary);">واجبات الطالب: <span style="color: var(--primary);">${studentData[0].fullName || username}</span></h3>`;
            html += `<div class="cards-grid">`;
            
            studentData.forEach(s => {
                let lessonNum = 1;
                if(s.lessonId && s.lessonId.includes('_L')) {
                    lessonNum = parseInt(s.lessonId.split('_L')[1]) || 1;
                }
                
                // البحث في المصفوفة اللي جاية من بايثون للوصول لاسم الملف الأصلي
                let exerciseFile = `exercise${lessonNum}.html`; 
                if (exercisesList && exercisesList.length >= lessonNum) {
                    exerciseFile = exercisesList[lessonNum - 1].file;
                }
                
                const gradeLink = `/page/${CURRENT_LEVEL}/${exerciseFile}?student=${s.username}&mode=grading`;
                
                html += `
                <div class="course-card">
                    <div class="header" style="background: #fcf3cf;"><i class="fa-solid fa-book"></i> الدرس: ${s.lessonId}</div>
                    <div class="body">
                        <span class="badge pending" style="font-size: 14px;">⏳ ${s.pendingCount} إجابات للتصحيح</span>
                        <a href="${gradeLink}" target="_blank" class="action-btn" style="margin-top: 15px; display: block; text-align: center; text-decoration: none; background: #9b59b6; color: white;" onclick="this.style.background = '#95a5a6'; this.innerHTML = 'تم فتح الصفحة ✔️';">
                            افتح الصفحة وصحح <i class="fa-solid fa-arrow-up-right-from-square"></i>
                        </a>
                    </div>
                </div>`;
            });
            html += `</div>`;
            container.innerHTML = html;
        }

        // العودة لقائمة الطلبة
        function backToStudentsList() {
            document.getElementById('studentLessonsView').style.display = 'none';
            document.getElementById('studentsListView').style.display = 'block';
        }

        // ================= جلب بيانات التقدم (الليدربورد) =================
        async function loadProgressData() {
            if (!CURRENT_LEVEL) return;
            const tbody = document.getElementById('leaderboardContent');
            tbody.innerHTML = '<tr><td colspan="6">جاري تحميل البيانات... ⏳</td></tr>';
            try {
                const res = await fetch(SCRIPT_URL + '?action=getAllStudentsProgress&_t=' + Date.now());
                const data = await res.json();
                
                if (data.status === 'success' && data.students && data.students.length > 0) {
                    const filteredStudents = data.students.filter(s => studentsLevelsMap[s.username] === CURRENT_LEVEL);
                    
                    if(filteredStudents.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6">لا يوجد بيانات تقدم لطلبة هذا المستوى حتى الآن.</td></tr>';
                        return;
                    }

                    let html = '';
                    const sortedStudents = filteredStudents.sort((a, b) => {
                        let valA = parseFloat(a.percentage) || 0;
                        let valB = parseFloat(b.percentage) || 0;
                        return valB - valA;
                    });
                    
                    sortedStudents.forEach(s => {
                        html += `
                        <tr>
                            <td><strong>${s.fullName || s.username}</strong></td>
                            <td style="color: #27ae60; font-weight: bold; font-size: 16px;">${s.totalCorrect || 0}</td>
                            <td style="color: #c0392b; font-weight: bold; font-size: 16px;">${s.totalWrong || 0}</td>
                            <td style="color: #f39c12; font-weight: bold; font-size: 16px;">${s.totalPending || 0}</td>
                            <td><span class="badge" style="background: #eef2f5; color: #2c3e50; font-size: 15px; padding: 6px 12px;">${s.percentage || '0%'}</span></td>
                            <td style="font-size: 12px; color: #7f8c8d;">${s.lastUpdate || '-'}</td>
                        </tr>`;
                    });
                    tbody.innerHTML = html;
                } else {
                    tbody.innerHTML = '<tr><td colspan="6">لا يوجد بيانات للطلبة حتى الآن.</td></tr>';
                }
            } catch (err) {
                tbody.innerHTML = '<tr><td colspan="6">❌ حدث خطأ أثناء الاتصال بخادم التقييمات.</td></tr>';
            }
        }
    </script>
</body>
</html>
"""

# =====================================================================
# [ Routes - الراوتات ]
# =====================================================================

@app.route('/', methods=['GET', 'POST'])
def login_student():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_data(username, password, role='student')
        if user:
            session.permanent = True 
            session['user'] = user
            session['role'] = 'student'
            return redirect(url_for('dashboard'))
        else:
            error = "بيانات الطالب غير صحيحة!"
    return render_template_string(STUDENT_LOGIN_HTML, error=error)

@app.route('/teacher_login', methods=['GET', 'POST'])
def login_teacher():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_data(username, password, role='teacher')
        if user:
            session.permanent = True 
            session['user'] = user
            session['role'] = 'teacher'
            return redirect(url_for('teacher_dashboard'))
        else:
            error = "بيانات المدرس غير صحيحة!"
    return render_template_string(TEACHER_LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session or session.get('role') != 'student':
        return redirect(url_for('login_student'))
    
    student = session['user']
    raw_level = str(student.get('level', '')).strip()
    level = 'demo' if raw_level.lower() == 'demo' else raw_level
    student['level'] = level
    
    student_lessons = LESSONS_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_exercises = EXERCISES_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_vocab = VOCAB_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_schedules = SCHEDULES_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_shadowing = SHADOWING_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_games = GAMES_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_videos = VIDEOS_DATA.get(level, [{"title": "فيديو ترحيبي", "youtube_id": "dQw4w9WgXcQ"}])
    
    random_quote = random.choice(motivation_quotes)
    
    base_level = level.split('.')[0] if '.' in level else level
    student_wheel_topics = WHEEL_TOPICS.get(level, WHEEL_TOPICS.get(base_level, ["تحدث عن مهاراتك."]))
    topics_json = json.dumps(student_wheel_topics, ensure_ascii=False)
    
    return render_template_string(
        DASHBOARD_HTML, 
        student=student, 
        lessons_list=student_lessons, 
        exercises_list=student_exercises,
        vocab_list=student_vocab,
        schedules_list=student_schedules,
        shadowing_list=student_shadowing,
        games_list=student_games,
        quote=random_quote,
        topics_json=topics_json,
        videos_list=student_videos
    )

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect(url_for('login_teacher'))
    
    teacher = session['user']
    selected_level = request.args.get('level', '')
    
    materials = {}
    if selected_level:
        materials = {
            'lessons': LESSONS_DATA.get(selected_level, []),
            'exercises': EXERCISES_DATA.get(selected_level, []),
            'vocab': VOCAB_DATA.get(selected_level, []),
            'schedules': SCHEDULES_DATA.get(selected_level, []),
            'shadowing': SHADOWING_DATA.get(selected_level, []),
            'games': GAMES_DATA.get(selected_level, []),
            'multi_games': MULTIPLAYER_GAMES_DATA.get(selected_level, [])
        }

    students_levels_map = get_all_students_levels()
    students_levels_json = json.dumps(students_levels_map, ensure_ascii=False)

    return render_template_string(
        TEACHER_DASHBOARD_HTML, 
        teacher=teacher, 
        current_level=selected_level, 
        materials=materials,
        script_url=SCRIPT_URL,
        students_levels_json=students_levels_json
    )

@app.route('/page/<level>/<filename>')
def serve_page(level, filename):
    if 'user' not in session:
        return redirect(url_for('login_student'))
    
    role = session.get('role')
    student_username = request.args.get('student')
    
    if role == 'teacher':
        target_user = {'username': student_username or session['user'].get('username', 'المدرس'), 'level': level}
    else:
        target_user = session['user']
        user_level = str(target_user.get('level', '')).strip()
        req_level = str(level).strip()
        
        if user_level.lower() == 'demo':
            allowed_demo_files = [
                'lesson1.html', 'lesson2.html',
                'exercise1.html', 'exercise2.html',
                'vocab1.html', 'vocab2.html',
                'schedule1.html', 'schedule2.html',
                'game1.html', 'game2.html',
                'shadowing1.html', 'shadowing2.html',
                'multi1.html', 'multi2.html'
            ]
            if req_level.lower() not in ['demo', 'a1.1'] or filename not in allowed_demo_files:
                abort(403)
        elif user_level != req_level:
            abort(403)
    
    template_context = {
        'student': target_user,
        'script_url': SCRIPT_URL  
    }
    
    actual_folder = "A1.1" if str(level).strip().lower() == "demo" else level
    
    try:
        return render_template(f"{actual_folder}/{filename}", **template_context)
    except Exception as e:
        print(f"Template error: {e}")
        try:
            return render_template(f"{actual_folder}/{filename}")
        except:
            abort(404)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_student'))

@app.route('/healthz')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
