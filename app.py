import os
import pandas as pd
import random
import json
from datetime import timedelta
from flask import Flask, render_template_string, request, redirect, url_for, session, abort, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'instituto_amigos_ultra_secure_2026')

# إغلاق الجلسة أوتوماتيكياً بعد ساعتين لزيادة الأمان
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# =====================================================================
# [ روابط جوجل شيت ]
# =====================================================================
# رابط شيت الطلبة
STUDENT_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdTMPVAfLN18RG6mLNXwycXhra4STzYPIiy7fvzCpeio0SfksLG4YNw78vA-djsSTG4rNSv2qdoXS8/pub?output=csv"

# رابط شيت المدرسين (تم التحديث بالرابط الخاص بك)
TEACHER_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8XNmds7FrrXWcDd8mwrD0AGc7e1tU_-ACrJ-vVF7UYsL36COnRtxiEoaMq9VhauxPyUGJqfEGak8X/pub?gid=854861638&single=true&output=csv" 

# رابط السكربت الخاص بحفظ التقييمات وجلب تقدم الطلبة
SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbychpxvHbr8JbOBoha0qTegQUtsVd8l0aPnt1V_7CyJniWSjGGbk1djI2Tzk3HrPa8x/exec'

# =====================================================================
# [ 1. المحاضرات - LESSONS_DATA ]
# =====================================================================
LESSONS_DATA = {
    "A1.1": [
        {"title": "HOLA, ¿QUÉ TAL?", "file": "lesson1.html"},
        {"title": "EL ESPAÑOL Y YO", "file": "lesson2.html"},
        {"title": "TRABAJO AQUÍ", "file": "lesson3.html"},
        {"title": "¡ME GUSTAN LAS TAPAS!", "file": "lesson4.html"}
    ],
    "A1.2": [
        {"title": "EN FAMILIA", "file": "lesson1.html"},
        {"title": "MI BARRIO", "file": "lesson2.html"},
        {"title": "MI DÍA A DÍA", "file": "lesson3.html"},
        {"title": "DE VACACIONES", "file": "lesson4.html"}
    ],
    "A1.3": [
        {"title": "COMPRAR Y COMER EN ALICANTE", "file": "lesson1.html"},
        {"title": "¡BUEN FIN DE SEMANA!", "file": "lesson2.html"},
        {"title": "INTERCAMBIO DE CASA", "file": "lesson3.html"},
        {"title": "ESTA ES MI VIDA", "file": "lesson4.html"}
    ],
    "A2.1": [
        {"title": "NUEVA ETAPA", "file": "lesson1.html"},
        {"title": "PARA TI Y PARA MÍ", "file": "Unidad 02.htm"},
        {"title": "UN AÑO ESPECIAL", "file": "lesson3.html"},
        {"title": "CON TUS MANOS", "file": "lesson4.html"}
    ],
    "A2.2": [
        {"title": "¿CÓMO ERA ANTES?", "file": "lesson1.html"},
        {"title": "¿Y QUÉ PASÓ?", "file": "lesson2.html"},
        {"title": "HOY COCINO YO", "file": "lesson3.html"},
        {"title": "¡ME SIENTO BIEN!", "file": "lesson4.html"}
    ],
    "A2.3": [
        {"title": "TE INVITO", "file": "lesson1.html"},
        {"title": "UNA CIUDAD IDEAL", "file": "lesson2.html"},
        {"title": "NOSOTROS Y EL TRABAJO", "file": "lesson3.html"},
        {"title": "¡ESTAMOS AL DÍA!", "file": "lesson4.html"}
    ],
    "B1.1": [
        {"title": "SEGUIMOS JUNTOS", "file": "lesson1.html"},
        {"title": "UN VIAJE INOLVIDABLE", "file": "lesson2.html"},
        {"title": "UN MUNDO MEJOR", "file": "lesson3.html"},
        {"title": "HABLANDO DEL FUTURO", "file": "lesson4.html"}
    ],
    "B1.2": [
        {"title": "ENTRE NOSOTROS", "file": "lesson1.html"},
        {"title": "NUESTRO PLANETA", "file": "lesson2.html"},
        {"title": "¡CÁMARA, ACCIÓN!", "file": "lesson3.html"},
        {"title": "BUENO Y SANO", "file": "lesson4.html"}
    ],
    "B1.3": [
        {"title": "MENSAJES CON EFECTO", "file": "lesson1.html"},
        {"title": "UN PASEO CULTURAL", "file": "lesson2.html"},
        {"title": "DE AQUÍ PARA ALLÁ", "file": "lesson3.html"},
        {"title": "UN MUNDO IMPRESIONANTE", "file": "lesson4.html"}
    ],
    "B2.1": [
        {"title": "ASÍ HABLAMOS, ASÍ SOMOS", "file": "lesson1.html"},
        {"title": "LA ESCUELA DE LA VIDA", "file": "lesson2.html"},
        {"title": "NUEVOS MUNDOS LABORALES", "file": "lesson3.html"},
        {"title": "¡QUÉ ILUSIÓN!", "file": "lesson4.html"}
    ],
    "B2.2": [
        {"title": "PEGADOS AL MÓVIL", "file": "lesson1.html"},
        {"title": "MENTE SANA EN CUERPO SANO", "file": "lesson2.html"},
        {"title": "¡HOGAR, DULCE HOGAR!", "file": "lesson3.html"},
        {"title": "A FLOR DE PIEL", "file": "lesson4.html"}
    ],
    "B2.3": [
        {"title": "LUGARES ESPECIALES", "file": "lesson1.html"},
        {"title": "ROMPIENDO ESQUEMAS", "file": "lesson2.html"},
        {"title": "¡NO TE QUEJES TANTO!", "file": "lesson3.html"},
        {"title": "MIRANDO HACIA ADELANTE", "file": "lesson4.html"}
    ]
}

# =====================================================================
# [ 2. التمارين - EXERCISES_DATA ]
# =====================================================================
EXERCISES_DATA = {
    "A1.1": [
        {"title": "تمرين: HOLA, ¿QUÉ TAL?", "file": "exercise1.html"},
        {"title": "تمرين: EL ESPAÑOL Y YO", "file": "exercise2.html"},
        {"title": "تمرين: TRABAJO AQUÍ", "file": "exercise3.html"},
        {"title": "تمرين: ¡ME GUSTAN LAS TAPAS!", "file": "exercise4.html"}
    ],
    "A1.2": [
        {"title": "تمرين: EN FAMILIA", "file": "exercise1.html"},
        {"title": "تمرين: MI BARRIO", "file": "exercise2.html"},
        {"title": "تمرين: MI DÍA A DÍA", "file": "exercise3.html"},
        {"title": "تمرين: DE VACACIONES", "file": "exercise4.html"}
    ],
    "A1.3": [
        {"title": "تمرين: COMPRAR Y COMER EN ALICANTE", "file": "exercise1.html"},
        {"title": "تمرين: ¡BUEN FIN DE SEMANA!", "file": "exercise2.html"},
        {"title": "تمرين: INTERCAMBIO DE CASA", "file": "exercise3.html"},
        {"title": "تمرين: ESTA ES MI VIDA", "file": "exercise4.html"}
    ],
    "A2.1": [
        {"title": "تمرين: NUEVA ETAPA", "file": "exercise1.html"},
        {"title": "تمرين: PARA TI Y PARA MÍ", "file": "exercise2.htm"},
        {"title": "تمرين: UN AÑO ESPECIAL", "file": "exercise3.html"},
        {"title": "تمرين: CON TUS MANOS", "file": "exercise4.html"}
    ],
    "A2.2": [
        {"title": "تمرين: ¿CÓMO ERA ANTES?", "file": "exercise1.html"},
        {"title": "تمرين: ¿Y QUÉ PASÓ?", "file": "exercise2.html"},
        {"title": "تمرين: HOY COCINO YO", "file": "exercise3.html"},
        {"title": "تمرين: ¡ME SIENTO BIEN!", "file": "exercise4.html"}
    ],
    "A2.3": [
        {"title": "تمرين: TE INVITO", "file": "exercise1.html"},
        {"title": "تمرين: UNA CIUDAD IDEAL", "file": "exercise2.html"},
        {"title": "تمرين: NOSOTROS Y EL TRABAJO", "file": "exercise3.html"},
        {"title": "تمرين: ¡ESTAMOS AL DÍA!", "file": "exercise4.html"}
    ],
    "B1.1": [
        {"title": "تمرين: SEGUIMOS JUNTOS", "file": "exercise1.html"},
        {"title": "تمرين: UN VIAJE INOLVIDABLE", "file": "exercise2.html"},
        {"title": "تمرين: UN MUNDO MEJOR", "file": "exercise3.html"},
        {"title": "تمرين: HABLANDO DEL FUTURO", "file": "exercise4.html"}
    ],
    "B1.2": [
        {"title": "تمرين: ENTRE NOSOTROS", "file": "exercise1.html"},
        {"title": "تمرين: NUESTRO PLANETA", "file": "exercise2.html"},
        {"title": "تمرين: ¡CÁMARA, ACCIÓN!", "file": "exercise3.html"},
        {"title": "تمرين: BUENO Y SANO", "file": "exercise4.html"}
    ],
    "B1.3": [
        {"title": "تمرين: MENSAJES CON EFECTO", "file": "exercise1.html"},
        {"title": "تمرين: UN PASEO CULTURAL", "file": "exercise2.html"},
        {"title": "تمرين: DE AQUÍ PARA ALLÁ", "file": "exercise3.html"},
        {"title": "تمرين: UN MUNDO IMPRESIONANTE", "file": "exercise4.html"}
    ],
    "B2.1": [
        {"title": "تمرين: ASÍ HABLAMOS, ASÍ SOMOS", "file": "exercise1.html"},
        {"title": "تمرين: LA ESCUELA DE LA VIDA", "file": "exercise2.html"},
        {"title": "تمرين: NUEVOS MUNDOS LABORALES", "file": "exercise3.html"},
        {"title": "تمرين: ¡QUÉ ILUSIÓN!", "file": "exercise4.html"}
    ],
    "B2.2": [
        {"title": "تمرين: PEGADOS AL MÓVIL", "file": "exercise1.html"},
        {"title": "تمرين: MENTE SANA EN CUERPO SANO", "file": "exercise2.html"},
        {"title": "تمرين: ¡HOGAR, DULCE HOGAR!", "file": "exercise3.html"},
        {"title": "تمرين: A FLOR DE PIEL", "file": "exercise4.html"}
    ],
    "B2.3": [
        {"title": "تمرين: LUGARES ESPECIALES", "file": "exercise1.html"},
        {"title": "تمرين: ROMPIENDO ESQUEMAS", "file": "exercise2.html"},
        {"title": "تمرين: ¡NO TE QUEJES TANTO!", "file": "exercise3.html"},
        {"title": "تمرين: MIRANDO HACIA ADELANTE", "file": "exercise4.html"}
    ]
}

# =====================================================================
# [ 3. الكلمات - VOCAB_DATA ]
# =====================================================================
VOCAB_DATA = {
    "A1.1": [
        {"title": "كلمات: HOLA, ¿QUÉ TAL?", "file": "vocab1.html"},
        {"title": "كلمات: EL ESPAÑOL Y YO", "file": "vocab2.html"},
        {"title": "كلمات: TRABAJO AQUÍ", "file": "vocab3.html"},
        {"title": "كلمات: ¡ME GUSTAN LAS TAPAS!", "file": "vocab4.html"}
    ],
    "A1.2": [
        {"title": "كلمات: EN FAMILIA", "file": "vocab1.html"},
        {"title": "كلمات: MI BARRIO", "file": "vocab2.html"},
        {"title": "كلمات: MI DÍA A DÍA", "file": "vocab3.html"},
        {"title": "كلمات: DE VACACIONES", "file": "vocab4.html"}
    ],
    "A1.3": [
        {"title": "كلمات: COMPRAR Y COMER EN ALICANTE", "file": "vocab1.html"},
        {"title": "كلمات: ¡BUEN FIN DE SEMANA!", "file": "vocab2.html"},
        {"title": "كلمات: INTERCAMBIO DE CASA", "file": "vocab3.html"},
        {"title": "كلمات: ESTA ES MI VIDA", "file": "vocab4.html"}
    ],
    "A2.1": [
        {"title": "كلمات: NUEVA ETAPA", "file": "vocab1.html"},
        {"title": "كلمات: PARA TI Y PARA MÍ", "file": "Unidad 02 - Palabras.htm"},
        {"title": "كلمات: UN AÑO ESPECIAL", "file": "vocab3.html"},
        {"title": "كلمات: CON TUS MANOS", "file": "vocab4.html"}
    ],
    "A2.2": [
        {"title": "كلمات: ¿CÓMO ERA ANTES?", "file": "vocab1.html"},
        {"title": "كلمات: ¿Y QUÉ PASÓ?", "file": "vocab2.html"},
        {"title": "كلمات: HOY COCINO YO", "file": "vocab3.html"},
        {"title": "كلمات: ¡ME SIENTO BIEN!", "file": "vocab4.html"}
    ],
    "A2.3": [
        {"title": "كلمات: TE INVITO", "file": "vocab1.html"},
        {"title": "كلمات: UNA CIUDAD IDEAL", "file": "vocab2.html"},
        {"title": "كلمات: NOSOTROS Y EL TRABAJO", "file": "vocab3.html"},
        {"title": "كلمات: ¡ESTAMOS AL DÍA!", "file": "vocab4.html"}
    ],
    "B1.1": [
        {"title": "كلمات: SEGUIMOS JUNTOS", "file": "vocab1.html"},
        {"title": "كلمات: UN VIAJE INOLVIDABLE", "file": "vocab2.html"},
        {"title": "كلمات: UN MUNDO MEJOR", "file": "vocab3.html"},
        {"title": "كلمات: HABLANDO DEL FUTURO", "file": "vocab4.html"}
    ],
    "B1.2": [
        {"title": "كلمات: ENTRE NOSOTROS", "file": "vocab1.html"},
        {"title": "كلمات: NUESTRO PLANETA", "file": "vocab2.html"},
        {"title": "كلمات: ¡CÁMARA, ACCIÓN!", "file": "vocab3.html"},
        {"title": "كلمات: BUENO Y SANO", "file": "vocab4.html"}
    ],
    "B1.3": [
        {"title": "كلمات: MENSAJES CON EFECTO", "file": "vocab1.html"},
        {"title": "كلمات: UN PASEO CULTURAL", "file": "vocab2.html"},
        {"title": "كلمات: DE AQUÍ PARA ALLÁ", "file": "vocab3.html"},
        {"title": "كلمات: UN MUNDO IMPRESIONANTE", "file": "vocab4.html"}
    ],
    "B2.1": [
        {"title": "كلمات: ASÍ HABLAMOS, ASÍ SOMOS", "file": "vocab1.html"},
        {"title": "كلمات: LA ESCUELA DE LA VIDA", "file": "vocab2.html"},
        {"title": "كلمات: NUEVOS MUNDOS LABORALES", "file": "vocab3.html"},
        {"title": "كلمات: ¡QUÉ ILUSIÓN!", "file": "vocab4.html"}
    ],
    "B2.2": [
        {"title": "كلمات: PEGADOS AL MÓVIL", "file": "vocab1.html"},
        {"title": "كلمات: MENTE SANA EN CUERPO SANO", "file": "vocab2.html"},
        {"title": "كلمات: ¡HOGAR, DULCE HOGAR!", "file": "vocab3.html"},
        {"title": "كلمات: A FLOR DE PIEL", "file": "vocab4.html"}
    ],
    "B2.3": [
        {"title": "كلمات: LUGARES ESPECIALES", "file": "vocab1.html"},
        {"title": "كلمات: ROMPIENDO ESQUEMAS", "file": "vocab2.html"},
        {"title": "كلمات: ¡NO TE QUEJES TANTO!", "file": "vocab3.html"},
        {"title": "كلمات: MIRANDO HACIA ADELANTE", "file": "vocab4.html"}
    ]
}

# =====================================================================
# [ 4. جداول المذاكرة - SCHEDULES_DATA ]
# =====================================================================
SCHEDULES_DATA = {
    "A1.1": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "A1.2": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "A1.3": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "A2.1": [{"title": "جدول مذاكرة الدرس الأول", "file": "gadwal1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "Unidad 02 - Study_Plan.htm"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "gadwal3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "gadwal4.html"}],
    "A2.2": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "A2.3": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "B1.1": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "B1.2": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "B1.3": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "B2.1": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "B2.2": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}],
    "B2.3": [{"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"}, {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"}, {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"}, {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}]
}

# =====================================================================
# [ 5. الألعاب الفردية - GAMES_DATA ]
# =====================================================================
GAMES_DATA = {
    "A1.1": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "A1.2": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "A1.3": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "A2.1": [{"title": "لعبة تفاعلية للدرس الأول", "file": "juego-estudiante1.htm"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "Unidad 02 - Juego _Est.htm"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "A2.2": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "A2.3": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "B1.1": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "B1.2": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "B1.3": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "B2.1": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "B2.2": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}],
    "B2.3": [{"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"}, {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"}, {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"}, {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}]
}

# =====================================================================
# [ 6. الشادوينج - SHADOWING_DATA ]
# =====================================================================
SHADOWING_DATA = {
    "A1.1": [{"title": "شادوينج: HOLA, ¿QUÉ TAL?", "file": "shadowing1.html"}, {"title": "شادوينج: EL ESPAÑOL Y YO", "file": "shadowing2.html"}, {"title": "شادوينج: TRABAJO AQUÍ", "file": "shadowing3.html"}, {"title": "شادوينج: ¡ME GUSTAN LAS TAPAS!", "file": "shadowing4.html"}],
    "A1.2": [{"title": "شادوينج: EN FAMILIA", "file": "shadowing1.html"}, {"title": "شادوينج: MI BARRIO", "file": "shadowing2.html"}, {"title": "شادوينج: MI DÍA A DÍA", "file": "shadowing3.html"}, {"title": "شادوينج: DE VACACIONES", "file": "shadowing4.html"}],
    "A1.3": [{"title": "شادوينج: COMPRAR Y COMER EN ALICANTE", "file": "shadowing1.html"}, {"title": "شادوينج: ¡BUEN FIN DE SEMANA!", "file": "shadowing2.html"}, {"title": "شادوينج: INTERCAMBIO DE CASA", "file": "shadowing3.html"}, {"title": "شادوينج: ESTA ES MI VIDA", "file": "shadowing4.html"}],
    "A2.1": [{"title": "شادوينج: NUEVA ETAPA", "file": "shadowing1.html"}, {"title": "شادوينج: PARA TI Y PARA MÍ", "file": "Unidad 02 - Shadowing.htm"}, {"title": "شادوينج: UN AÑO ESPECIAL", "file": "shadowing3.html"}, {"title": "شادوينج: CON TUS MANOS", "file": "shadowing4.html"}],
    "A2.2": [{"title": "شادوينج: ¿CÓMO ERA ANTES?", "file": "shadowing1.html"}, {"title": "شادوينج: ¿Y QUÉ PASÓ?", "file": "shadowing2.html"}, {"title": "شادوينج: HOY COCINO YO", "file": "shadowing3.html"}, {"title": "شادوينج: ¡ME SIENTO BIEN!", "file": "shadowing4.html"}],
    "A2.3": [{"title": "شادوينج: TE INVITO", "file": "shadowing1.html"}, {"title": "شادوينج: UNA CIUDAD IDEAL", "file": "shadowing2.html"}, {"title": "شادوينج: NOSOTROS Y EL TRABAJO", "file": "shadowing3.html"}, {"title": "شادوينج: ¡ESTAMOS AL DÍA!", "file": "shadowing4.html"}],
    "B1.1": [{"title": "شادوينج: SEGUIMOS JUNTOS", "file": "shadowing1.html"}, {"title": "شادوينج: UN VIAJE INOLVIDABLE", "file": "shadowing2.html"}, {"title": "شادوينج: UN MUNDO MEJOR", "file": "shadowing3.html"}, {"title": "شادوينج: HABLANDO DEL FUTURO", "file": "shadowing4.html"}],
    "B1.2": [{"title": "شادوينج: ENTRE NOSOTROS", "file": "shadowing1.html"}, {"title": "شادوينج: NUESTRO PLANETA", "file": "shadowing2.html"}, {"title": "شادوينج: ¡CÁMARA, ACCIÓN!", "file": "shadowing3.html"}, {"title": "شادوينج: BUENO Y SANO", "file": "shadowing4.html"}],
    "B1.3": [{"title": "شادوينج: MENSAJES CON EFECTO", "file": "shadowing1.html"}, {"title": "شادوينج: UN PASEO CULTURAL", "file": "shadowing2.html"}, {"title": "شادوينج: DE AQUÍ PARA ALLÁ", "file": "shadowing3.html"}, {"title": "شادوينج: UN MUNDO IMPRESIONANTE", "file": "shadowing4.html"}],
    "B2.1": [{"title": "شادوينج: ASÍ HABLAMOS, ASÍ SOMOS", "file": "shadowing1.html"}, {"title": "شادوينج: LA ESCUELA DE LA VIDA", "file": "shadowing2.html"}, {"title": "شادوينج: NUEVOS MUNDOS LABORALES", "file": "shadowing3.html"}, {"title": "شادوينج: ¡QUÉ ILUSIÓN!", "file": "shadowing4.html"}],
    "B2.2": [{"title": "شادوينج: PEGADOS AL MÓVIL", "file": "shadowing1.html"}, {"title": "شادوينج: MENTE SANA EN CUERPO SANO", "file": "shadowing2.html"}, {"title": "شادوينج: ¡HOGAR, DULCE HOGAR!", "file": "shadowing3.html"}, {"title": "شادوينج: A FLOR DE PIEL", "file": "shadowing4.html"}],
    "B2.3": [{"title": "شادوينج: LUGARES ESPECIALES", "file": "shadowing1.html"}, {"title": "شادوينج: ROMPIENDO ESQUEMAS", "file": "shadowing2.html"}, {"title": "شادوينج: ¡NO TE QUEJES TANTO!", "file": "shadowing3.html"}, {"title": "شادوينج: MIRANDO HACIA ADELANTE", "file": "shadowing4.html"}]
}

# =====================================================================
# [ 7. الفيديوهات - VIDEOS_DATA ]
# =====================================================================
VIDEOS_DATA = {
    "A1.1": [{"title": "مراجعة قواعد النطق الأساسية والأبجدية", "youtube_id": "dQw4w9WgXcQ"}, {"title": "أدوات التعريف والتنكير في الإسبانية", "youtube_id": "dQw4w9WgXcQ"}],
    "A1.2": [{"title": "شرح مفردات العائلة والأقارب بالتفصيل", "youtube_id": "dQw4w9WgXcQ"}, {"title": "الأفعال الروتينية اليومية وتصريفها", "youtube_id": "dQw4w9WgXcQ"}],
    "A1.3": [{"title": "كيف تتسوق وتطلب الطعام داخل المطعم", "youtube_id": "dQw4w9WgXcQ"}],
    "A2.1": [{"title": "Un día muy especial", "youtube_id": "7dgZvDijGP0"}, {"title": "Soy un manitas", "youtube_id": "fnC6LeUHcq0"}],
    "A2.2": [{"title": "استخدامات زمن الماضي المستمر لوصف الطفولة", "youtube_id": "dQw4w9WgXcQ"}],
    "A2.3": [{"title": "صيغ الأمر والطلب بطريقة مهذبة", "youtube_id": "dQw4w9WgXcQ"}],
    "B1.1": [{"title": "قواعد التعبير عن المستقبل والخطط البعيدة", "youtube_id": "dQw4w9WgXcQ"}],
    "B1.2": [{"title": "تعبيرات النقاش وإبداء الرأي الشخصي بحرية", "youtube_id": "dQw4w9WgXcQ"}],
    "B1.3": [{"title": "روابط الجمل المتقدمة وكتابة المقالات", "youtube_id": "dQw4w9WgXcQ"}],
    "B2.1": [{"title": "التعمق في صيغ الشك والاحتمالية الصعبة", "youtube_id": "dQw4w9WgXcQ"}],
    "B2.2": [{"title": "مصطلحات تقنية متقدمة لإدارة حوار عملي", "youtube_id": "dQw4w9WgXcQ"}],
    "B2.3": [{"title": "مراجعة شاملة لإتقان المحادثة السريعة والطلاقة", "youtube_id": "dQw4w9WgXcQ"}]
}

# =====================================================================
# [ 8. الألعاب الجماعية - MULTIPLAYER_GAMES_DATA ]
# =====================================================================
MULTIPLAYER_GAMES_DATA = {
    "A1.1": [{"title": "لعبة كاهوت جماعية 1", "file": "multi1.html"}, {"title": "لعبة تفاعلية للفصل", "file": "multi2.html"}],
    "A2.1": [{"title": "مسابقة كلمات جماعية", "file": "multi_a2.html"}]
}

# =====================================================================
# [ 9. عجلة التحدث - WHEEL_TOPICS ]
# =====================================================================
WHEEL_TOPICS = {
    "A1.1": ["قدم نفسك بالكامل: اسمك وسنك وبلدك.", "تحدث عن الألوان المفضلة لديك ولماذا.", "اذكر 5 أشياء تستخدمها كل يوم.", "اوصف الطقس النهاردة بالإسباني.", "قول أيام الأسبوع وقول بتعمل إيه كل يوم.", "اتكلم عن أكلتك المفضلة.", "عرّف صاحبك المقرب: اسمه وشكله.", "قول الأرقام من 1 لـ 20 وبعدين العد العكسي.", "اوصف أوضتك: فيها إيه؟", "سلم على حد جديد وعرّفه بنفسك."],
    "A1.2": ["صف أفراد عائلتك واحد واحد.", "تحدث عن روتينك الصباحي خطوة بخطوة.", "ما هو طعامك المفضل وليه؟", "اوصف حيك أو شارعك.", "اتكلم عن هوايتك المفضلة.", "إيه اللي بتعمله يوم الجمعة؟", "اوصف صاحبك: شكله وطبعه.", "اتكلم عن مدرستك أو شغلك.", "قول 5 حاجات بتحبها و5 مبتحبهاش.", "خطط لعطلة نهاية الأسبوع الجاية."],
    "A1.3": ["تخيل أنك في السوبرماركت وبتشتري أكل.", "صف مدينتك: فيها إيه؟", "كيف تقضي عطلة نهاية الأسبوع عادةً؟", "اوصف بيتك: كام أوضة وشكله عامل إزاي.", "اتكلم عن آخر حاجة اشتريتها.", "اطلب أكل في مطعم إسباني.", "اوصف الطقس في بلدك في الصيف والشتاء.", "اتكلم عن رحلة عملتها قبل كده.", "إيه الحاجات اللي بتعملها في الأجازة؟", "صف يوم مثالي بالنسبالك."],
    "A2.1": ["تحدث عن هواية جديدة بدأتها مؤخراً.", "صف أعز أصدقائك: شخصيته وهواياته.", "تحدث عما فعلته في عطلة الأسبوع الماضي.", "اوصف تجربة تعلمك الإسبانية.", "اتكلم عن أحلامك وأهدافك.", "لو سافرت لإسبانيا هتعمل إيه؟", "اوصف عيد ميلادك الأخير.", "اتكلم عن فيلم أو مسلسل شفته مؤخراً.", "صف شخص بتحبه وبتقدره.", "قارن بين حياتك دلوقتي وقبل 5 سنين."],
    "A2.2": ["احكِ لنا كيف كانت مرحلة طفولتك.", "اشرح وصفة طبخ بسيطة خطوة بخطوة.", "ماذا تفعل عندما تشعر بالمرض؟", "اتكلم عن ذكرى جميلة من أيام المدرسة.", "صف مكان زرته وعجبك أوي.", "اتكلم عن عادات كنت بتعملها وأنت صغير.", "قارن بين الحياة في المدينة والريف.", "اوصف أجمل يوم في حياتك.", "اتكلم عن حاجة اتعلمتها من غلطة عملتها.", "صف شخصيتك لما كنت طفل."],
    "A2.3": ["وجه دعوة لصديقك لحفلة عندك.", "صف ملامح مدينتك المثالية.", "تحدث عن وظيفة أحلامك.", "اقترح خطة لعطلة مع أصحابك.", "اتكلم عن مهارة نفسك تتعلمها.", "اوصف مطعمك المفضل.", "اتكلم عن مشكلة في شغلك وإزاي حليتها.", "لو عندك سوبر باور هتختار إيه؟", "انصح حد بدأ يتعلم إسباني.", "اتكلم عن التكنولوجيا في حياتك اليومية."],
    "B1.1": ["احكِ لنا عن رحلة لا تُنسى في حياتك.", "ما هي خططك المستقبلية للسنة الجاية؟", "تحدث عن فيلم أثر فيك كتير.", "اوصف شخصية تاريخية بتعجبك.", "لو تقدر تغير حاجة في العالم تغير إيه؟", "اتكلم عن تجربة صعبة واتعلمت منها.", "قارن بين الدراسة أونلاين والدراسة العادية.", "اتكلم عن كتاب قرأته وأثر فيك.", "صف أحسن معلم أو أستاذ قابلته في حياتك.", "اتكلم عن عادات صحية بتحاول تعملها."],
    "B1.2": ["إيجابيات وسلبيات السوشيال ميديا في حياتنا.", "ما هو أسلوب الحياة الصحي من وجهة نظرك؟", "كيف يمكننا حماية كوكب الأرض؟", "اتكلم عن تأثير الموسيقى على المزاج.", "لو أنت رئيس بلد يوم واحد تعمل إيه؟", "اتكلم عن أهمية الرياضة في حياة الإنسان.", "صف مشكلة بيئية وإزاي نحلها.", "اتكلم عن تجربة تطوع عملتها أو نفسك تعملها.", "قارن بين الأجيال المختلفة في التفكير.", "اتكلم عن أهمية السفر والتعرف على ثقافات تانية."],
    "B1.3": ["أهمية الفنون والموسيقى في المجتمع.", "احكِ عن تجربة شخصية صعبة وإزاي تغلبت عليها.", "رأيك في التعليم عن بُعد: مميزاته وعيوبه.", "اتكلم عن تأثير الأخبار على حياتنا اليومية.", "صف ثقافة بلد تاني بتعجبك وليه.", "اتكلم عن أهمية القراءة في العصر الحديث.", "لو عندك آلة زمن تروح فين ولأي عصر؟", "اتكلم عن موقف غيّر تفكيرك في حاجة.", "صف مشروع نفسك تبدأه في المستقبل.", "اتكلم عن الفرق بين الحياة في الماضي والحاضر."],
    "B2.1": ["كيف تطورت شخصيتك على مدار السنين؟", "تحديات الشباب في سوق العمل الحديث.", "ما هو مفهوم النجاح الشخصي بالنسبالك؟", "ناقش تأثير العولمة على الثقافات المحلية.", "اتكلم عن الذكاء الاصطناعي وتأثيره على المستقبل.", "لو تقدر تعيش في أي عصر تاني تختار أنهي؟", "ناقش أهمية تعلم لغات متعددة في عالم اليوم.", "اتكلم عن العلاقة بين المال والسعادة.", "صف قدوتك في الحياة وإيه اللي اتعلمته منها.", "ناقش مفهوم التوازن بين العمل والحياة الشخصية."],
    "B2.2": ["إدمان الهواتف الذكية: مشكلة حقيقية ولا مبالغة؟", "أهمية الحفاظ على الصحة النفسية في عصرنا.", "احكِ عن موقف حرج وكيف تعاملت معه بذكاء.", "ناقش تأثير وسائل التواصل على العلاقات الإنسانية.", "اتكلم عن أهمية الخروج من منطقة الراحة.", "صف تجربة فشلت فيها وإيه اللي اتعلمته منها.", "ناقش ظاهرة العمل عن بُعد: مستقبل ولا موضة؟", "اتكلم عن أهمية الوعي البيئي للأجيال الجديدة.", "لو تقدر تنصح نفسك من 10 سنين تقول إيه؟", "ناقش تأثير الثقافة الشعبية على قيم المجتمع."],
    "B2.3": ["مكان استثنائي تمنيت زيارته واوصفه بالتفصيل.", "تطلعاتك المهنية على المدى الطويل.", "كيف تتعامل مع مشكلات وضغوط العمل؟", "ناقش أخلاقيات استخدام التكنولوجيا الحديثة.", "اتكلم عن دور الفن في التغيير الاجتماعي.", "صف لحظة حسيت فيها بفخر كبير بنفسك.", "ناقش العلاقة بين التعليم التقليدي والتعليم الذاتي.", "لو هتكتب كتاب عن حياتك عنوانه يبقى إيه؟", "اتكلم عن أهمية التنوع الثقافي في بيئة العمل.", "ناقش مستقبل اللغات في عالم الترجمة الآلية."]
}

# الجمل التحفيزية للطلبة
motivation_quotes = [
    "عاش يا بطل، الاستمرارية هي سر النجاح في أي لغة.",
    "كل درس بتخلصه بيقربك خطوة لحلمك، كمل وماتوقفش!"
]

# =====================================================================
# [ دوال قراءة البيانات ]
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
            return user_row.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error checking Google Sheet ({role}): {e}")
        return None

def get_all_students_levels():
    """ استدعاء جميع مستويات الطلبة لاستخدامها في فلترة الواجبات للمدرس """
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
# [ صفحات الدخول ]
# =====================================================================
STUDENT_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>دخول الطلبة | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #fcfbf7; font-family: 'Cairo', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin:0; }
        .card { background: white; padding: 40px; border-radius: 15px; box-shadow: 5px 5px 0px rgba(0,0,0,0.05); border: 3px solid #333; text-align: center; width: 400px; }
        .logo-img { width: 110px; border-radius: 50%; border: 3px solid #ffd100; margin-bottom: 10px; }
        h1 { color: #333; font-size: 24px; font-weight: 900; margin-bottom: 5px; }
        .input-group { margin: 15px 0; }
        input { width: 100%; padding: 12px; border: 2px solid #333; border-radius: 8px; text-align: center; font-family: 'Cairo'; }
        button { width: 100%; padding: 12px; background: #e52421; color: white; border: 2px solid #333; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 10px; }
        .teacher-link { display: inline-block; margin-top: 20px; color: #555; text-decoration: none; font-weight: bold; font-size: 14px; border-bottom: 2px dashed #ccc; padding-bottom: 2px; transition: 0.3s; }
        .teacher-link:hover { color: #e52421; border-color: #e52421; }
        .error { color: #e52421; margin-bottom: 15px; font-weight: bold; background: #ffebeb; padding: 8px; border-radius: 5px; border: 1px solid #e52421; }
    </style>
</head>
<body>
    <div class="card">
        <img src="/static/assets/logo.png" class="logo-img" onerror="this.src='https://ui-avatars.com/api/?name=IA&background=ffd100&color=e52421'">
        <h1>بوابتك لـ Español 👋</h1>
        <p style="color: #666; margin-bottom: 25px;">دخول الطلبة للمنصة التعليمية</p>
        {% if error %} <div class="error">{{ error }}</div> {% endif %}
        <form method="POST">
            <div class="input-group"><input type="text" name="username" placeholder="اسم المستخدم" required></div>
            <div class="input-group"><input type="password" name="password" placeholder="كلمة المرور" required></div>
            <button type="submit">ادخل للمنصة</button>
        </form>
        <a href="/teacher_login" class="teacher-link"><i class="fa-solid fa-chalkboard-user"></i> الدخول كمدرس</a>
    </div>
</body>
</html>
"""

TEACHER_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>دخول المدرسين | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #1a1a2e; color: white; font-family: 'Cairo', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin:0; }
        .card { background: #16213e; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 2px solid #0f3460; text-align: center; width: 400px; }
        h1 { color: #f39c12; font-size: 26px; font-weight: 900; margin-bottom: 5px; }
        .input-group { margin: 15px 0; }
        input { width: 100%; padding: 12px; border: 2px solid #0f3460; background: #1a1a2e; color: white; border-radius: 8px; text-align: center; font-family: 'Cairo'; }
        button { width: 100%; padding: 12px; background: #e67e22; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 10px; }
        .student-link { display: inline-block; margin-top: 20px; color: #aaa; text-decoration: none; font-size: 14px; transition: 0.3s; }
        .student-link:hover { color: #fff; }
        .error { color: #fff; margin-bottom: 15px; font-weight: bold; background: #e74c3c; padding: 8px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="card">
        <i class="fa-solid fa-chalkboard-user" style="font-size: 50px; color: #f39c12; margin-bottom: 15px;"></i>
        <h1>بوابة المدرسين 👨‍🏫</h1>
        <p style="color: #aaa; margin-bottom: 25px;">أدخل بياناتك للوصول للوحة التحكم</p>
        {% if error %} <div class="error">{{ error }}</div> {% endif %}
        <form method="POST">
            <div class="input-group"><input type="text" name="username" placeholder="اسم المستخدم" required></div>
            <div class="input-group"><input type="password" name="password" placeholder="كلمة المرور" required></div>
            <button type="submit">تسجيل الدخول</button>
        </form>
        <a href="/" class="student-link"><i class="fa-solid fa-arrow-right"></i> رجوع لصفحة الطلبة</a>
    </div>
</body>
</html>
"""

# =====================================================================
# [ لوحة الطالب ]
# =====================================================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
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
        .welcome-section { background: linear-gradient(135deg, var(--secondary) 0%, #1a2530 100%); color: white; padding: 40px; border-radius: 24px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
        .user-welcome-info h2 { font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        .tabs-nav { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 25px; background: white; padding: 12px; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); }
        .tab-trigger { background: none; border: 2px solid transparent; font-size: 13px; font-weight: 700; color: var(--text-muted); padding: 10px 16px; cursor: pointer; border-radius: 12px; }
        .tab-trigger.active { background: var(--primary); color: white; border-color: var(--primary); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }
        .course-card { background: white; border-radius: 20px; overflow: hidden; border: 1px solid #f0f3f5; text-align: center; }
        .card-header { padding: 18px 20px; background: #fafbfc; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center;}
        .lesson-number { font-size: 12px; font-weight: 800; padding: 5px 12px; border-radius: 50px; background: rgba(0,0,0,0.05); color: #333; }
        .card-body { padding: 25px 20px; }
        .card-body h4 { font-size: 16px; font-weight: 800; color: var(--secondary); margin-bottom: 15px; }
        .card-action-btn { display: inline-block; width: 100%; padding: 13px; background: var(--primary); color: white; text-decoration: none; border-radius: 12px; font-weight: 700; font-size: 14px; }
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="top-right-container">
            <div class="user-buttons">
                <a href="/logout" class="logout-btn">خروج</a>
                <span class="level-badge">مستواك: {{ student.level }}</span>
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
            </div>
        </header>

        <nav class="tabs-nav">
            <button class="tab-trigger active" onclick="switchTab(event, 'lectures-tab')">الدروس</button>
            <button class="tab-trigger" onclick="switchTab(event, 'exercises-tab')">التمارين</button>
            <button class="tab-trigger" onclick="switchTab(event, 'vocab-tab')">الكلمات</button>
            <button class="tab-trigger" onclick="switchTab(event, 'schedule-tab')">الجداول</button>
            <button class="tab-trigger" onclick="switchTab(event, 'shadowing-tab')">الشادوينج</button>
            <button class="tab-trigger" onclick="switchTab(event, 'games-tab')">الألعاب</button>
        </nav>

        <div id="lectures-tab" class="tab-content active">
            <div class="cards-grid">
                {% for item in lessons_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number">الدرس {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn" target="_blank">ابدأ الدرس</a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="exercises-tab" class="tab-content">
            <div class="cards-grid">
                {% for item in exercises_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number">تمرين {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn" target="_blank" style="background:#f39c12;">ابدأ التمرين</a></div>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div id="vocab-tab" class="tab-content">
            <div class="cards-grid">
                {% for item in vocab_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number">كلمات {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn" target="_blank" style="background:#8e44ad;">افتح الكلمات</a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="schedule-tab" class="tab-content">
            <div class="cards-grid">
                {% for item in schedules_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number">جدول {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn" target="_blank" style="background:#2c3e50;">افتح الجدول</a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="shadowing-tab" class="tab-content">
            <div class="cards-grid">
                {% for item in shadowing_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number">شادوينج {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn" target="_blank" style="background:#e67e22;">ابدأ الشادوينج</a></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="games-tab" class="tab-content">
            <div class="cards-grid">
                {% for item in games_list %}
                <div class="course-card">
                    <div class="card-header"><span class="lesson-number">لعبة {{ loop.index }}</span></div>
                    <div class="card-body"><h4>{{ item.title }}</h4><a href="/page/{{ student.level }}/{{ item.file }}" class="card-action-btn" target="_blank" style="background:#2ecc71;">العب الآن</a></div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    <script>
        function switchTab(evt, tabId) {
            document.querySelectorAll(".tab-content").forEach(el => el.classList.remove("active"));
            document.querySelectorAll(".tab-trigger").forEach(el => el.classList.remove("active"));
            document.getElementById(tabId).classList.add("active");
            evt.currentTarget.classList.add("active");
        }
    </script>
</body>
</html>
"""

# =====================================================================
# [ لوحة المدرس الشاملة (بها التقسيم الهرمي والليدربورد) ]
# =====================================================================
TEACHER_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>لوحة المدرس | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Cairo', sans-serif; }
        body { background: #f4f7f6; color: #333; }
        .top-nav { background: #1a1a2e; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .brand { font-size: 20px; font-weight: 900; color: #f39c12; }
        .user-actions a { color: white; text-decoration: none; background: #e74c3c; padding: 8px 15px; border-radius: 8px; font-weight: bold; }
        .main-tabs { display: flex; justify-content: center; gap: 20px; background: white; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 30px; flex-wrap: wrap;}
        .m-tab { background: none; border: none; font-size: 18px; font-weight: bold; color: #555; padding: 10px 20px; cursor: pointer; border-bottom: 3px solid transparent; transition: 0.3s; }
        .m-tab.active { color: #1a1a2e; border-color: #f39c12; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 15px 50px; }
        .level-selector { background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .level-selector select { padding: 10px 20px; font-size: 16px; border: 2px solid #ccc; border-radius: 8px; font-weight: bold; }
        .content-tabs { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; justify-content: center; }
        .c-tab { background: white; border: 1px solid #ddd; padding: 8px 15px; border-radius: 8px; cursor: pointer; font-weight: bold; color: #555; }
        .c-tab.active { background: #f39c12; color: white; border-color: #f39c12; }
        .c-tab.multi-games { background: #8e44ad; color: white; border-color: #8e44ad; }
        .c-tab.multi-games.active { background: #9b59b6; }
        .tab-section { display: none; }
        .tab-section.active { display: block; }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top:15px; }
        .course-card { background: white; border-radius: 15px; border: 1px solid #eee; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.03); text-align: center; cursor: pointer; transition: 0.3s; }
        .course-card:hover { transform: translateY(-3px); border-color:#f39c12; }
        .course-card .header { background: #f8f9fa; padding: 15px; font-weight: bold; color: #1a1a2e; border-bottom: 1px solid #eee; }
        .course-card .body { padding: 20px; }
        .course-card a, .action-btn { display: inline-block; width: 100%; padding: 10px; background: #f39c12; color: #1a1a2e; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 10px; border:none; cursor:pointer;}
        .course-card a.multi-btn { background: #8e44ad; color: white; }
        .grading-section { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); min-height: 400px;}
        .badge { padding: 4px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; margin-left: 5px; }
        .badge.pending { background: #ffeaa7; color: #d35400; }
        .student-detail { background: #fff; border: 2px solid #f39c12; border-radius: 15px; padding: 20px; margin-top: 20px; }
        .pq-box { background: #fdfefe; border: 1px solid #eee; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-right: 4px solid #f39c12; text-align:right;}
        .pq-ans { background: #f4f6f7; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 16px; margin: 10px 0; direction: ltr; text-align: left;}
        .v-btn { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-left: 5px; }
        .v-btn.correct { background: #e9f7ef; color: #27ae60; border: 1px solid #27ae60; }
        .v-btn.correct.active { background: #27ae60; color: white; }
        .v-btn.wrong { background: #fdedec; color: #c0392b; border: 1px solid #c0392b; }
        .v-btn.wrong.active { background: #c0392b; color: white; }
        .f-input { padding: 8px; border: 1px solid #ccc; border-radius: 5px; width: 250px; font-family: 'Cairo'; }
        .submit-btn { background: #27ae60; color: white; padding: 12px 25px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; margin-top: 15px; }
        .back-btn { padding:8px 15px; background:#95a5a6; color:white; border:none; border-radius:5px; cursor:pointer; margin-bottom:15px; font-weight:bold; transition:0.3s; }
        .back-btn:hover { background: #7f8c8d; }
        
        /* ستايل جدول تقدم الطلبة (الترتيب) */
        .schedule-table { width: 100%; border-collapse: collapse; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        .schedule-table th { background: #1a1a2e; color: white; padding: 15px; text-align: center; font-size: 15px; }
        .schedule-table td { padding: 15px; border-bottom: 1px solid #eee; text-align: center; font-weight: 600; color: #333;}
        .schedule-table tr:hover { background: #f8fafc; }
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
        <button class="m-tab active" onclick="switchMainTab('materials', this)"><i class="fa-solid fa-book"></i> المناهج والمواد</button>
        <button class="m-tab" onclick="switchMainTab('grading', this); refreshGradingData();"><i class="fa-solid fa-check-double"></i> تصحيح الواجبات</button>
        <button class="m-tab" onclick="switchMainTab('leaderboard', this); loadProgressData();"><i class="fa-solid fa-ranking-star"></i> تقدم الطلبة</button>
    </div>

    <div class="container">
        <div id="materials-view" class="tab-section active">
            <div class="level-selector">
                <label style="font-weight:bold; font-size:18px;">اختر المستوى:</label><br><br>
                <select id="levelSelect" onchange="window.location.href='/teacher_dashboard?level=' + this.value">
                    <option value="">-- اختر المستوى --</option>
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
                <button class="c-tab active" onclick="switchContentTab('lectures')">الدروس</button>
                <button class="c-tab" onclick="switchContentTab('exercises')">التمارين</button>
                <button class="c-tab multi-games" onclick="switchContentTab('multiplayer')"><i class="fa-solid fa-users"></i> ألعاب جماعية</button>
            </div>

            <div id="lectures" class="c-section active" style="display:block;">
                <div class="cards-grid">
                    {% for item in materials.lessons %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الدرس</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div id="exercises" class="c-section" style="display:none;">
                <div class="cards-grid">
                    {% for item in materials.exercises %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح التمرين</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="multiplayer" class="c-section" style="display:none;">
                <div class="cards-grid">
                    {% for item in materials.multi_games %}
                    <div class="course-card" style="border-color: #8e44ad;">
                        <div class="header" style="background: #f4ecf7; color: #8e44ad;">{{ item.title }}</div>
                        <div class="body">
                            <a href="/page/{{ current_level }}/{{ item.file }}" target="_blank" class="multi-btn">تشغيل اللعبة <i class="fa-solid fa-play"></i></a>
                        </div>
                    </div>
                    {% else %}
                    <p style="text-align:center; width:100%; color:#888;">لا توجد ألعاب جماعية حالياً.</p>
                    {% endfor %}
                </div>
            </div>
            {% else %}
            <p style="text-align:center; color:#777; font-size:18px;">يرجى اختيار المستوى لعرض المحتوى.</p>
            {% endif %}
        </div>

        <div id="grading-view" class="tab-section grading-section">
            <h2 style="color: #f39c12; margin-bottom: 15px;"><i class="fa-solid fa-file-pen"></i> تصحيح الواجبات لمستوى ({{ current_level or 'الرجاء اختياره من الأعلى' }})</h2>
            
            <div id="studentsListView">
                {% if current_level %}
                <button onclick="refreshGradingData()" style="padding:8px 15px; background:#3498db; color:white; border:none; border-radius:5px; cursor:pointer;">🔄 تحديث القائمة</button>
                <div id="studentsListContent" class="cards-grid">جاري التحميل...</div>
                {% else %}
                <p style="text-align:center; color:#777;">اختر المستوى من القائمة العلوية أولاً لتظهر واجبات طلبة هذا المستوى.</p>
                {% endif %}
            </div>

            <div id="studentLessonsView" style="display:none;">
                <button onclick="backToStudentsList()" class="back-btn">⬅️ رجوع لقائمة الطلبة</button>
                <div id="studentLessonsContent"></div>
            </div>

            <div id="studentDetailView" style="display:none;">
                <button onclick="backToStudentLessons()" class="back-btn">⬅️ رجوع لدروس الطالب</button>
                <div id="studentDetailContent" class="student-detail"></div>
            </div>
        </div>

        <div id="leaderboard-view" class="tab-section grading-section">
            <h2 style="color: #f39c12; margin-bottom: 15px;"><i class="fa-solid fa-ranking-star"></i> تقدم الطلبة (Leaderboard)</h2>
            <button onclick="loadProgressData()" style="padding:8px 15px; background:#e67e22; color:white; border:none; border-radius:5px; cursor:pointer; margin-bottom:15px;">🔄 تحديث البيانات</button>
            <div style="overflow-x:auto;">
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
        // التبديل بين الأقسام الرئيسية (المواد، التصحيح، الترتيب)
        function switchMainTab(tab, btn) {
            document.querySelectorAll('.m-tab').forEach(b => b.classList.remove('active'));
            if(btn) btn.classList.add('active');
            document.querySelectorAll('.tab-section').forEach(s => s.classList.remove('active'));
            document.getElementById(tab + '-view').classList.add('active');
        }

        // التبديل بين محتويات المادة التعليمية
        function switchContentTab(tabId) {
            document.querySelectorAll('.c-tab').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.c-section').forEach(s => s.style.display = 'none');
            if(document.getElementById(tabId)) document.getElementById(tabId).style.display = 'block';
        }

        // ================= المتغيرات العامة =================
        const SCRIPT_URL = '{{ script_url }}';
        const TEACHER_USER = '{{ teacher.username }}';
        const CURRENT_LEVEL = '{{ current_level }}';
        const studentsLevelsMap = {{ students_levels_json | safe }};
        
        // ================= نظام التصحيح الهرمي =================
        let allPendingData = [];
        let currentSelectedUsername = "";
        let currentReviews = {};
        let currentStudentDetails = null;

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

        function renderStudentsList() {
            const container = document.getElementById('studentsListContent');
            if(allPendingData.length === 0) {
                container.innerHTML = '<p style="color:green; font-weight:bold;">✅ لا يوجد واجبات بانتظار التصحيح لطلبة هذا المستوى!</p>';
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
                    <div class="header" style="background:#eef2f5;"><i class="fa-solid fa-user-graduate"></i> الطالب: ${student.fullName}</div>
                    <div class="body">
                        <p style="color:#7f8c8d; margin-bottom:10px;">عدد الدروس للتقييم: <strong>${student.lessons.length}</strong></p>
                        <span class="badge pending">⏳ ${student.totalPending} سؤال بانتظار التصحيح</span>
                        <button class="action-btn" style="margin-top:15px; background:#3498db; color:white;">عرض دروس الطالب</button>
                    </div>
                </div>`;
            });
            container.innerHTML = html;
        }

        function showStudentLessons(username) {
            currentSelectedUsername = username;
            document.getElementById('studentsListView').style.display = 'none';
            document.getElementById('studentLessonsView').style.display = 'block';
            
            const container = document.getElementById('studentLessonsContent');
            const studentData = allPendingData.filter(s => s.username === username);
            
            let html = `<h3 style="margin-bottom: 20px; color: var(--secondary);">واجبات الطالب: <span style="color:var(--primary);">${studentData[0].fullName || username}</span></h3>`;
            html += `<div class="cards-grid">`;
            
            studentData.forEach(s => {
                html += `
                <div class="course-card" onclick="openStudentGrading('${s.username}', '${s.lessonId}')">
                    <div class="header" style="background:#fcf3cf;"><i class="fa-solid fa-book"></i> الدرس: ${s.lessonId}</div>
                    <div class="body">
                        <span class="badge pending" style="font-size:14px;">⏳ ${s.pendingCount} إجابات للتصحيح</span>
                        <button class="action-btn" style="margin-top:15px;">صحح الآن <i class="fa-solid fa-pen-clip"></i></button>
                    </div>
                </div>`;
            });
            html += `</div>`;
            container.innerHTML = html;
        }

        function backToStudentsList() {
            document.getElementById('studentLessonsView').style.display = 'none';
            document.getElementById('studentDetailView').style.display = 'none';
            document.getElementById('studentsListView').style.display = 'block';
        }

        function backToStudentLessons() {
            document.getElementById('studentDetailView').style.display = 'none';
            document.getElementById('studentLessonsView').style.display = 'block';
        }

        async function openStudentGrading(username, lessonId) {
            document.getElementById('studentLessonsView').style.display = 'none';
            document.getElementById('studentDetailView').style.display = 'block';
            
            const container = document.getElementById('studentDetailContent');
            container.innerHTML = '<p>جاري تحميل إجابات الدرس... ⏳</p>';
            currentReviews = {};

            try {
                const res = await fetch(SCRIPT_URL + '?action=getStudentDetails&username=' + username + '&lessonId=' + lessonId);
                const data = await res.json();
                if (data.status === 'success') {
                    currentStudentDetails = data.student;
                    renderStudentDetails(container);
                }
            } catch (err) {
                container.innerHTML = '<p>❌ خطأ في التحميل</p>';
            }
        }
        
        function renderStudentDetails(container) {
            const pending = currentStudentDetails.pendingAnswers;
            let html = `<h3 style="margin-bottom:20px;">تصحيح لدرس <span style="color:#e52421;">${currentStudentDetails.lessonId}</span></h3>`;
            
            Object.keys(pending).forEach(qId => {
                const ans = pending[qId];
                html += `
                <div class="pq-box">
                    <p><strong>السؤال:</strong> ${ans.questionText || qId}</p>
                    <div class="pq-ans">${ans.value}</div>
                    ${ans.expectedAnswer ? `<p style="color:green; font-size:14px;">الإجابة النموذجية: ${ans.expectedAnswer}</p>` : ''}
                    <div style="margin-top:15px; display:flex; gap:10px; align-items:center;">
                        <button class="v-btn correct" onclick="setVerdict('${qId}', 'correct', this)">✅ إجابة صحيحة</button>
                        <button class="v-btn wrong" onclick="setVerdict('${qId}', 'wrong', this)">❌ إجابة خاطئة</button>
                        <input type="text" class="f-input" placeholder="ملاحظة للطالب (اختياري)" data-qid="${qId}">
                    </div>
                </div>`;
            });
            html += `<button class="submit-btn" onclick="submitReviews()">حفظ التصحيح المعتمد <i class="fa-solid fa-save"></i></button>`;
            container.innerHTML = html;
        }

        function setVerdict(qId, verdict, btn) {
            currentReviews[qId] = { verdict: verdict };
            btn.parentElement.querySelectorAll('.v-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }

        async function submitReviews() {
            if (Object.keys(currentReviews).length === 0) return alert('برجاء تصحيح سؤال واحد على الأقل قبل الحفظ!');
            
            Object.keys(currentReviews).forEach(qId => {
                const inp = document.querySelector(`.f-input[data-qid="${qId}"]`);
                if(inp) currentReviews[qId].feedback = inp.value;
            });

            const payload = {
                action: 'submitReview',
                username: currentStudentDetails.username,
                lessonId: currentStudentDetails.lessonId,
                teacher: TEACHER_USER,
                reviews: JSON.stringify(currentReviews)
            };

            const url = SCRIPT_URL + '?action=submitReview&data=' + encodeURIComponent(JSON.stringify(payload));
            await fetch(url, { mode: 'no-cors' }); 
            alert('✅ تم حفظ التصحيح بنجاح وإرساله للطالب!');
            refreshGradingData();
            backToStudentsList();
        }

        // ================= نظام تقدم الطلبة (الترتيب) =================
        async function loadProgressData() {
            const tbody = document.getElementById('leaderboardContent');
            tbody.innerHTML = '<tr><td colspan="6">جاري تحميل البيانات... ⏳</td></tr>';
            try {
                // نطلب البيانات من الـ SCRIPT
                const res = await fetch(SCRIPT_URL + '?action=getStudentsProgress&_t=' + Date.now());
                const data = await res.json();
                
                if (data.status === 'success' && data.students && data.students.length > 0) {
                    let html = '';
                    
                    // ترتيب الطلبة من الأعلى نسبة إلى الأقل
                    const sortedStudents = data.students.sort((a, b) => {
                        let valA = parseFloat(a.percentage) || 0;
                        let valB = parseFloat(b.percentage) || 0;
                        return valB - valA;
                    });
                    
                    sortedStudents.forEach(s => {
                        html += `
                        <tr>
                            <td><strong>${s.fullName || s.username}</strong></td>
                            <td style="color:#27ae60; font-weight:bold;">${s.totalCorrect || 0}</td>
                            <td style="color:#c0392b; font-weight:bold;">${s.totalWrong || 0}</td>
                            <td style="color:#f39c12; font-weight:bold;">${s.totalPending || 0}</td>
                            <td><span class="badge" style="background:#eef2f5; color:#2c3e50; font-size:14px; padding:6px 12px;">${s.percentage || '0%'}</span></td>
                            <td style="font-size:12px; color:#7f8c8d;">${s.lastUpdate || '-'}</td>
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
# [ الراوتات (Routes) ]
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
    level = student['level']
    
    student_lessons = LESSONS_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_exercises = EXERCISES_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_vocab = VOCAB_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_schedules = SCHEDULES_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_shadowing = SHADOWING_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    student_games = GAMES_DATA.get(level, [{"title": "قريباً", "file": "error.html"}])
    
    return render_template_string(
        DASHBOARD_HTML, 
        student=student, 
        lessons_list=student_lessons, 
        exercises_list=student_exercises,
        vocab_list=student_vocab,
        schedules_list=student_schedules,
        shadowing_list=student_shadowing,
        games_list=student_games
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

@app.route('/page/<path:filename>')
def serve_page(filename):
    if 'user' not in session:
        return redirect(url_for('login_student'))
    
    role = session.get('role')
    user = session['user']
    
    if role == 'student':
        if not filename.startswith(user['level'] + "/"):
            abort(403)
            
    try:
        return render_template(filename, student=user)
    except Exception as e:
        print(f"Template load error: {e}")
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
