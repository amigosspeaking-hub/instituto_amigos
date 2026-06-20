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

# حط لينك الـ CSV بتاع تاب المدرسين هنا
TEACHER_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdTMPVAfLN18RG6mLNXwycXhra4STzYPIiy7fvzCpeio0SfksLG4YNw78vA-djsSTG4rNSv2qdoXS8/pub?gid=854861638&single=true&output=csv" 

# رابط السكربت الخاص بحفظ التقييمات
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
    "A1.1": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "A1.2": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "A1.3": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "A2.1": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "gadwal1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "Unidad 02 - Study_Plan.htm"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "gadwal3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "gadwal4.html"}
    ],
    "A2.2": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "A2.3": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "B1.1": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "B1.2": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "B1.3": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "B2.1": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "B2.2": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ],
    "B2.3": [
        {"title": "جدول مذاكرة الدرس الأول", "file": "schedule1.html"},
        {"title": "جدول مذاكرة الدرس الثاني", "file": "schedule2.html"},
        {"title": "جدول مذاكرة الدرس الثالث", "file": "schedule3.html"},
        {"title": "جدول مذاكرة الدرس الرابع", "file": "schedule4.html"}
    ]
}

# =====================================================================
# [ 5. الألعاب - GAMES_DATA ]
# =====================================================================
GAMES_DATA = {
    "A1.1": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "A1.2": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "A1.3": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "A2.1": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "juego-estudiante1.htm"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "Unidad 02 - Juego _Est.htm"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "A2.2": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "A2.3": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "B1.1": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "B1.2": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "B1.3": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "B2.1": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "B2.2": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ],
    "B2.3": [
        {"title": "لعبة تفاعلية للدرس الأول", "file": "game1.html"},
        {"title": "لعبة تفاعلية للدرس الثاني", "file": "game2.html"},
        {"title": "لعبة تفاعلية للدرس الثالث", "file": "game3.html"},
        {"title": "لعبة تفاعلية للدرس الرابع", "file": "game4.html"}
    ]
}

# =====================================================================
# [ 6. الشادوينج - SHADOWING_DATA ]
# =====================================================================
SHADOWING_DATA = {
    "A1.1": [
        {"title": "شادوينج: HOLA, ¿QUÉ TAL?", "file": "shadowing1.html"},
        {"title": "شادوينج: EL ESPAÑOL Y YO", "file": "shadowing2.html"},
        {"title": "شادوينج: TRABAJO AQUÍ", "file": "shadowing3.html"},
        {"title": "شادوينج: ¡ME GUSTAN LAS TAPAS!", "file": "shadowing4.html"}
    ],
    "A1.2": [
        {"title": "شادوينج: EN FAMILIA", "file": "shadowing1.html"},
        {"title": "شادوينج: MI BARRIO", "file": "shadowing2.html"},
        {"title": "شادوينج: MI DÍA A DÍA", "file": "shadowing3.html"},
        {"title": "شادوينج: DE VACACIONES", "file": "shadowing4.html"}
    ],
    "A1.3": [
        {"title": "شادوينج: COMPRAR Y COMER EN ALICANTE", "file": "shadowing1.html"},
        {"title": "شادوينج: ¡BUEN FIN DE SEMANA!", "file": "shadowing2.html"},
        {"title": "شادوينج: INTERCAMBIO DE CASA", "file": "shadowing3.html"},
        {"title": "شادوينج: ESTA ES MI VIDA", "file": "shadowing4.html"}
    ],
    "A2.1": [
        {"title": "شادوينج: NUEVA ETAPA", "file": "shadowing1.html"},
        {"title": "شادوينج: PARA TI Y PARA MÍ", "file": "Unidad 02 - Shadowing.htm"},
        {"title": "شادوينج: UN AÑO ESPECIAL", "file": "shadowing3.html"},
        {"title": "شادوينج: CON TUS MANOS", "file": "shadowing4.html"}
    ],
    "A2.2": [
        {"title": "شادوينج: ¿CÓMO ERA ANTES?", "file": "shadowing1.html"},
        {"title": "شادوينج: ¿Y QUÉ PASÓ?", "file": "shadowing2.html"},
        {"title": "شادوينج: HOY COCINO YO", "file": "shadowing3.html"},
        {"title": "شادوينج: ¡ME SIENTO BIEN!", "file": "shadowing4.html"}
    ],
    "A2.3": [
        {"title": "شادوينج: TE INVITO", "file": "shadowing1.html"},
        {"title": "شادوينج: UNA CIUDAD IDEAL", "file": "shadowing2.html"},
        {"title": "شادوينج: NOSOTROS Y EL TRABAJO", "file": "shadowing3.html"},
        {"title": "شادوينج: ¡ESTAMOS AL DÍA!", "file": "shadowing4.html"}
    ],
    "B1.1": [
        {"title": "شادوينج: SEGUIMOS JUNTOS", "file": "shadowing1.html"},
        {"title": "شادوينج: UN VIAJE INOLVIDABLE", "file": "shadowing2.html"},
        {"title": "شادوينج: UN MUNDO MEJOR", "file": "shadowing3.html"},
        {"title": "شادوينج: HABLANDO DEL FUTURO", "file": "shadowing4.html"}
    ],
    "B1.2": [
        {"title": "شادوينج: ENTRE NOSOTROS", "file": "shadowing1.html"},
        {"title": "شادوينج: NUESTRO PLANETA", "file": "shadowing2.html"},
        {"title": "شادوينج: ¡CÁMARA, ACCIÓN!", "file": "shadowing3.html"},
        {"title": "شادوينج: BUENO Y SANO", "file": "shadowing4.html"}
    ],
    "B1.3": [
        {"title": "شادوينج: MENSAJES CON EFECTO", "file": "shadowing1.html"},
        {"title": "شادوينج: UN PASEO CULTURAL", "file": "shadowing2.html"},
        {"title": "شادوينج: DE AQUÍ PARA ALLÁ", "file": "shadowing3.html"},
        {"title": "شادوينج: UN MUNDO IMPRESIONANTE", "file": "shadowing4.html"}
    ],
    "B2.1": [
        {"title": "شادوينج: ASÍ HABLAMOS, ASÍ SOMOS", "file": "shadowing1.html"},
        {"title": "شادوينج: LA ESCUELA DE LA VIDA", "file": "shadowing2.html"},
        {"title": "شادوينج: NUEVOS MUNDOS LABORALES", "file": "shadowing3.html"},
        {"title": "شادوينج: ¡QUÉ ILUSIÓN!", "file": "shadowing4.html"}
    ],
    "B2.2": [
        {"title": "شادوينج: PEGADOS AL MÓVIL", "file": "shadowing1.html"},
        {"title": "شادوينج: MENTE SANA EN CUERPO SANO", "file": "shadowing2.html"},
        {"title": "شادوينج: ¡HOGAR, DULCE HOGAR!", "file": "shadowing3.html"},
        {"title": "شادوينج: A FLOR DE PIEL", "file": "shadowing4.html"}
    ],
    "B2.3": [
        {"title": "شادوينج: LUGARES ESPECIALES", "file": "shadowing1.html"},
        {"title": "شادوينج: ROMPIENDO ESQUEMAS", "file": "shadowing2.html"},
        {"title": "شادوينج: ¡NO TE QUEJES TANTO!", "file": "shadowing3.html"},
        {"title": "شادوينج: MIRANDO HACIA ADELANTE", "file": "shadowing4.html"}
    ]
}

# =====================================================================
# [ 7. الفيديوهات - VIDEOS_DATA ]
# =====================================================================
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
        {"title": "كيف تتسوق وتطلب الطعام داخل المطعم", "youtube_id": "dQw4w9WgXcQ"}
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

# =====================================================================
# [ الألعاب الجماعية - MULTIPLAYER_GAMES_DATA (خاصة بالمدرس) ]
# =====================================================================
MULTIPLAYER_GAMES_DATA = {
    "A1.1": [{"title": "لعبة تفاعلية للفصل - الدرس الأول", "file": "multi1.html"}],
    "A2.1": [{"title": "مسابقة كلمات جماعية", "file": "multi_a2.html"}],
}

# =====================================================================
# [ 8. عجلة التحدث - WHEEL_TOPICS ]
# =====================================================================
WHEEL_TOPICS = {
    "A1.1": [
        "قدم نفسك بالكامل: اسمك وسنك وبلدك.",
        "تحدث عن الألوان المفضلة لديك ولماذا.",
        "اذكر 5 أشياء تستخدمها كل يوم.",
        "اوصف الطقس النهاردة بالإسباني.",
        "قول أيام الأسبوع وقول بتعمل إيه كل يوم.",
        "اتكلم عن أكلتك المفضلة.",
        "عرّف صاحبك المقرب: اسمه وشكله.",
        "قول الأرقام من 1 لـ 20 وبعدين العد العكسي.",
        "اوصف أوضتك: فيها إيه؟",
        "سلم على حد جديد وعرّفه بنفسك."
    ],
    "A1.2": [
        "صف أفراد عائلتك واحد واحد.",
        "تحدث عن روتينك الصباحي خطوة بخطوة.",
        "ما هو طعامك المفضل وليه؟",
        "اوصف حيك أو شارعك.",
        "اتكلم عن هوايتك المفضلة.",
        "إيه اللي بتعمله يوم الجمعة؟",
        "اوصف صاحبك: شكله وطبعه.",
        "اتكلم عن مدرستك أو شغلك.",
        "قول 5 حاجات بتحبها و5 مبتحبهاش.",
        "خطط لعطلة نهاية الأسبوع الجاية."
    ],
    "A1.3": [
        "تخيل أنك في السوبرماركت وبتشتري أكل.",
        "صف مدينتك: فيها إيه؟",
        "كيف تقضي عطلة نهاية الأسبوع عادةً؟",
        "اوصف بيتك: كام أوضة وشكله عامل إزاي.",
        "اتكلم عن آخر حاجة اشتريتها.",
        "اطلب أكل في مطعم إسباني.",
        "اوصف الطقس في بلدك في الصيف والشتاء.",
        "اتكلم عن رحلة عملتها قبل كده.",
        "إيه الحاجات اللي بتعملها في الأجازة؟",
        "صف يوم مثالي بالنسبالك."
    ],
    "A2.1": [
        "تحدث عن هواية جديدة بدأتها مؤخراً.",
        "صف أعز أصدقائك: شخصيته وهواياته.",
        "تحدث عما فعلته في عطلة الأسبوع الماضي.",
        "اوصف تجربة تعلمك الإسبانية.",
        "اتكلم عن أحلامك وأهدافك.",
        "لو سافرت لإسبانيا هتعمل إيه؟",
        "اوصف عيد ميلادك الأخير.",
        "اتكلم عن فيلم أو مسلسل شفته مؤخراً.",
        "صف شخص بتحبه وبتقدره.",
        "قارن بين حياتك دلوقتي وقبل 5 سنين."
    ],
    "A2.2": [
        "احكِ لنا كيف كانت مرحلة طفولتك.",
        "اشرح وصفة طبخ بسيطة خطوة بخطوة.",
        "ماذا تفعل عندما تشعر بالمرض؟",
        "اتكلم عن ذكرى جميلة من أيام المدرسة.",
        "صف مكان زرته وعجبك أوي.",
        "اتكلم عن عادات كنت بتعملها وأنت صغير.",
        "قارن بين الحياة في المدينة والريف.",
        "اوصف أجمل يوم في حياتك.",
        "اتكلم عن حاجة اتعلمتها من غلطة عملتها.",
        "صف شخصيتك لما كنت طفل."
    ],
    "A2.3": [
        "وجه دعوة لصديقك لحفلة عندك.",
        "صف ملامح مدينتك المثالية.",
        "تحدث عن وظيفة أحلامك.",
        "اقترح خطة لعطلة مع أصحابك.",
        "اتكلم عن مهارة نفسك تتعلمها.",
        "اوصف مطعمك المفضل.",
        "اتكلم عن مشكلة في شغلك وإزاي حليتها.",
        "لو عندك سوبر باور هتختار إيه؟",
        "انصح حد بدأ يتعلم إسباني.",
        "اتكلم عن التكنولوجيا في حياتك اليومية."
    ],
    "B1.1": [
        "احكِ لنا عن رحلة لا تُنسى في حياتك.",
        "ما هي خططك المستقبلية للسنة الجاية؟",
        "تحدث عن فيلم أثر فيك كتير.",
        "اوصف شخصية تاريخية بتعجبك.",
        "لو تقدر تغير حاجة في العالم تغير إيه؟",
        "اتكلم عن تجربة صعبة واتعلمت منها.",
        "قارن بين الدراسة أونلاين والدراسة العادية.",
        "اتكلم عن كتاب قرأته وأثر فيك.",
        "صف أحسن معلم أو أستاذ قابلته في حياتك.",
        "اتكلم عن عادات صحية بتحاول تعملها."
    ],
    "B1.2": [
        "إيجابيات وسلبيات السوشيال ميديا في حياتنا.",
        "ما هو أسلوب الحياة الصحي من وجهة نظرك؟",
        "كيف يمكننا حماية كوكب الأرض؟",
        "اتكلم عن تأثير الموسيقى على المزاج.",
        "لو أنت رئيس بلد يوم واحد تعمل إيه؟",
        "اتكلم عن أهمية الرياضة في حياة الإنسان.",
        "صف مشكلة بيئية وإزاي نحلها.",
        "اتكلم عن تجربة تطوع عملتها أو نفسك تعملها.",
        "قارن بين الأجيال المختلفة في التفكير.",
        "اتكلم عن أهمية السفر والتعرف على ثقافات تانية."
    ],
    "B1.3": [
        "أهمية الفنون والموسيقى في المجتمع.",
        "احكِ عن تجربة شخصية صعبة وإزاي تغلبت عليها.",
        "رأيك في التعليم عن بُعد: مميزاته وعيوبه.",
        "اتكلم عن تأثير الأخبار على حياتنا اليومية.",
        "صف ثقافة بلد تاني بتعجبك وليه.",
        "اتكلم عن أهمية القراءة في العصر الحديث.",
        "لو عندك آلة زمن تروح فين ولأي عصر؟",
        "اتكلم عن موقف غيّر تفكيرك في حاجة.",
        "صف مشروع نفسك تبدأه في المستقبل.",
        "اتكلم عن الفرق بين الحياة في الماضي والحاضر."
    ],
    "B2.1": [
        "كيف تطورت شخصيتك على مدار السنين؟",
        "تحديات الشباب في سوق العمل الحديث.",
        "ما هو مفهوم النجاح الشخصي بالنسبالك؟",
        "ناقش تأثير العولمة على الثقافات المحلية.",
        "اتكلم عن الذكاء الاصطناعي وتأثيره على المستقبل.",
        "لو تقدر تعيش في أي عصر تاني تختار أنهي؟",
        "ناقش أهمية تعلم لغات متعددة في عالم اليوم.",
        "اتكلم عن العلاقة بين المال والسعادة.",
        "صف قدوتك في الحياة وإيه اللي اتعلمته منها.",
        "ناقش مفهوم التوازن بين العمل والحياة الشخصية."
    ],
    "B2.2": [
        "إدمان الهواتف الذكية: مشكلة حقيقية ولا مبالغة؟",
        "أهمية الحفاظ على الصحة النفسية في عصرنا.",
        "احكِ عن موقف حرج وكيف تعاملت معه بذكاء.",
        "ناقش تأثير وسائل التواصل على العلاقات الإنسانية.",
        "اتكلم عن أهمية الخروج من منطقة الراحة.",
        "صف تجربة فشلت فيها وإيه اللي اتعلمته منها.",
        "ناقش ظاهرة العمل عن بُعد: مستقبل ولا موضة؟",
        "اتكلم عن أهمية الوعي البيئي للأجيال الجديدة.",
        "لو تقدر تنصح نفسك من 10 سنين تقول إيه؟",
        "ناقش تأثير الثقافة الشعبية على قيم المجتمع."
    ],
    "B2.3": [
        "مكان استثنائي تمنيت زيارته واوصفه بالتفصيل.",
        "تطلعاتك المهنية على المدى الطويل.",
        "كيف تتعامل مع مشكلات وضغوط العمل؟",
        "ناقش أخلاقيات استخدام التكنولوجيا الحديثة.",
        "اتكلم عن دور الفن في التغيير الاجتماعي.",
        "صف لحظة حسيت فيها بفخر كبير بنفسك.",
        "ناقش العلاقة بين التعليم التقليدي والتعليم الذاتي.",
        "لو هتكتب كتاب عن حياتك عنوانه يبقى إيه؟",
        "اتكلم عن أهمية التنوع الثقافي في بيئة العمل.",
        "ناقش مستقبل اللغات في عالم الترجمة الآلية."
    ]
}

# =====================================================================
# [ 9. الجمل التحفيزية ]
# =====================================================================
motivation_quotes = [
    "عاش يا بطل، الاستمرارية هي سر النجاح في أي لغة.",
    "كل درس بتخلصه بيقربك خطوة لحلمك، كمل وماتوقفش!",
    "المذاكرة النهاردة هي طلاقتك بكرة، شد حيلك!",
    "مافيش حاجة صعبة على واحد بيحاول كل يوم، إحنا واثقين فيك!",
    "خطوة بخطوة هتوصل، المهم تفضل مكمل على نفس الحماس.",
    "تعبك النهاردة هترتاح بيه بكرة، ركز في درسك واعمل اللي عليك.",
    "رحلة الألف ميل بتبدأ بخطوة، وأنت قطعت شوط كبير.. استمر!"
]

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

# =====================================================================
# صفحات تسجيل الدخول
# =====================================================================
STUDENT_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>يالا بينا.. دخول | Instituto Amigos</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Reenie+Beanie&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary-red: #e52421; --primary-gold: #ffd100; }
        body { background: #fcfbf7; font-family: 'Cairo', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin:0; overflow: hidden; position: relative; }
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
        .card { background: white; padding: 40px; border-radius: 15px; box-shadow: 5px 5px 0px rgba(0,0,0,0.05); border: 3px solid #333; text-align: center; width: 400px; position: relative; z-index: 1; }
        .logo-img { width: 110px; height: auto; margin-bottom: 10px; border-radius: 50%; border: 3px solid var(--primary-gold); }
        h1 { color: #333; margin-bottom: 5px; font-size: 24px; font-weight: 900; }
        h1 .es-word { color: var(--primary-red); font-family: 'Reenie Beanie', cursive; font-size: 30px; }
        p.subtitle { color: #666; font-size: 14px; margin-bottom: 25px; }
        .input-group { position: relative; margin: 15px 0; }
        .input-group i.field-icon { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); color: #aaa; font-size: 16px; }
        input { width: 100%; padding: 12px 40px 12px 12px; border: 2px solid #333; border-radius: 8px; text-align: center; box-sizing: border-box; font-size: 15px; font-family: 'Cairo', sans-serif; transition: all 0.2s; }
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
        @media (max-width: 500px) { .card { width: 92%; padding: 25px; } .doodle-container { display: none; } }
    </style>
</head>
<body>
    <span class="float-word fw1">¡Hola!</span><span class="float-word fw2">ازيك!</span><span class="float-word fw3">Amigos</span><span class="float-word fw4">صحاب</span><span class="float-word fw5">Gracias</span><span class="float-word fw6">شكراً</span><span class="float-word fw7">Familia</span><span class="float-word fw8">عيلة</span><span class="float-word fw9">Bonito</span><span class="float-word fw10">جميل</span>
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
                <input type="text" name="username" placeholder="اسم المستخدم بتاعك" required>
            </div>
            <div class="input-group">
                <i class="fa-solid fa-lock field-icon"></i>
                <input type="password" name="password" placeholder="كلمة المرور" required>
            </div>
            <button type="submit"><i class="fa-solid fa-arrow-right-to-bracket"></i> ادخل للمنصة</button>
        </form>
        <a href="/teacher_login" class="teacher-link"><i class="fa-solid fa-chalkboard-user"></i> الدخول كمدرس</a>
        <div class="lang-strip">
            <div class="lang-item"><span class="es">Aprende!</span><br><span class="ar">اتعلم!</span></div>
            <div class="lang-item"><span class="es">Habla!</span><br><span class="ar">اتكلم!</span></div>
            <div class="lang-item"><span class="es">Practica!</span><br><span class="ar">اتمرن!</span></div>
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
# لوحة الطالب (DASHBOARD_HTML)
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
        :root { 
            --primary: #e52421; --primary-dark: #c31e1b; 
            --accent: #ffd100; --secondary: #2c3e50; 
            --bg-body: #f4f7f6; --text-main: #1e293b; --text-muted: #64748b;
            --vocab-color: #8e44ad; --vocab-light: rgba(142, 68, 173, 0.1);
            --shadow-color: #e67e22; --shadow-light: rgba(230, 126, 34, 0.1);
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
        .welcome-section::before {
            content: "¡Hola!  Amigos  Español  ازيك  يلا بينا";
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            font-family: 'Reenie Beanie', cursive; font-size: 60px; color: rgba(255,255,255,0.03);
            display: flex; align-items: center; justify-content: center;
            letter-spacing: 30px; pointer-events: none; overflow: hidden;
        }
        .user-welcome-info { z-index: 1; }
        .user-welcome-info h2 { font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        .user-welcome-info h2 .es-greet { font-family: 'Reenie Beanie', cursive; color: var(--accent); font-size: 38px; }
        .user-welcome-info p { font-size: 16px; color: rgba(255,255,255,0.8); max-width: 500px; }
        .motivation-box {
            background: rgba(255, 209, 0, 0.15); border: 1px solid var(--accent);
            color: var(--accent); padding: 20px; border-radius: 16px; text-align: center;
            width: 300px; backdrop-filter: blur(5px); z-index: 1;
        }
        .tabs-nav { 
            display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 25px; 
            background: white; padding: 12px; border-radius: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        }
        .tab-trigger { 
            background: none; border: 2px solid transparent; font-size: 13px; font-weight: 700; color: var(--text-muted); 
            padding: 10px 16px; cursor: pointer; transition: 0.3s; border-radius: 12px; 
            display: flex; align-items: center; gap: 6px; white-space: nowrap;
        }
        .tab-trigger:hover { background: #f0f3f5; border-color: #e2e8f0; }
        .tab-trigger.active { background: var(--primary); color: white; border-color: var(--primary); }
        .tab-trigger .tab-icon { font-size: 16px; }
        .tab-trigger .tab-es { font-family: 'Reenie Beanie', cursive; font-size: 15px; opacity: 0.7; }
        .tab-content { display: none; animation: fadeIn 0.4s ease; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .section-header {
            display: flex; align-items: center; gap: 15px; margin-bottom: 20px;
            padding: 15px 20px; background: white; border-radius: 16px;
            border-right: 5px solid var(--primary);
        }
        .section-header.vocab-header { border-right-color: var(--vocab-color); }
        .section-header.schedule-header { border-right-color: var(--secondary); }
        .section-header.games-header { border-right-color: #2ecc71; }
        .section-header.shadow-header { border-right-color: var(--shadow-color); }
        .section-header .sec-icon { font-size: 28px; }
        .section-header .sec-title { font-size: 20px; font-weight: 800; color: var(--secondary); }
        .section-header .sec-subtitle { font-size: 13px; color: var(--text-muted); }
        .section-header .sec-es { font-family: 'Reenie Beanie', cursive; font-size: 22px; color: var(--primary); margin-right: auto; }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }
        .course-card { 
            background: white; border-radius: 20px; overflow: hidden; 
            border: 1px solid #f0f3f5; transition: 0.3s; display: flex; flex-direction: column;
        }
        .course-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .course-card .card-accent { height: 4px; width: 100%; }
        .card-accent-red { background: linear-gradient(90deg, var(--primary), #ff6b6b); }
        .card-accent-gold { background: linear-gradient(90deg, var(--accent), #ffeb3b); }
        .card-accent-blue { background: linear-gradient(90deg, var(--secondary), #3498db); }
        .card-accent-green { background: linear-gradient(90deg, #2ecc71, #27ae60); }
        .card-accent-purple { background: linear-gradient(90deg, var(--vocab-color), #9b59b6); }
        .card-accent-orange { background: linear-gradient(90deg, var(--shadow-color), #f39c12); }
        .card-header { padding: 18px 20px; background: #fafbfc; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center;}
        .lesson-number { font-size: 12px; font-weight: 800; padding: 5px 12px; border-radius: 50px; }
        .ln-red { color: var(--primary); background: rgba(229, 36, 33, 0.1); }
        .ln-gold { color: #b8860b; background: rgba(255, 209, 0, 0.2); }
        .ln-blue { color: var(--secondary); background: rgba(0,140,186,0.1); }
        .ln-green { color: #2ecc71; background: rgba(46,204,113,0.1); }
        .ln-purple { color: var(--vocab-color); background: var(--vocab-light); }
        .ln-orange { color: var(--shadow-color); background: var(--shadow-light); }
        .card-body { padding: 25px 20px; text-align: center; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .card-body h4 { font-size: 16px; font-weight: 800; color: var(--secondary); margin-bottom: 8px; }
        .card-body .card-es-hint { font-family: 'Reenie Beanie', cursive; font-size: 18px; color: #bbb; margin-bottom: 15px; }
        .card-action-btn { 
            display: inline-flex; align-items: center; justify-content: center; gap: 8px;
            width: 100%; padding: 13px; text-decoration: none; border-radius: 12px; 
            font-weight: 700; font-size: 14px; transition: 0.2s; box-sizing: border-box; 
        }
        .card-action-btn:hover { filter: brightness(1.1); transform: translateY(-1px); }
        .btn-lecture { background: var(--primary); color: white; }
        .btn-exercise { background: var(--accent); color: var(--secondary); }
        .btn-schedule { background: var(--secondary); color: white; }
        .btn-game { background: #2ecc71; color: white; }
        .btn-vocab { background: var(--vocab-color); color: white; }
        .btn-shadow { background: var(--shadow-color); color: white; }
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
            font-family: 'Cairo', sans-serif;
        }
        .spin-btn:hover { background: var(--primary-dark); transform: translateY(-3px); }
        .spin-btn:disabled { background: #ccc; cursor: not-allowed; transform: none; box-shadow: none;}
        .spinning { animation: shake 0.1s infinite; color: var(--primary); }
        @keyframes shake { 0% { transform: translateX(0); } 25% { transform: translateX(-2px); } 50% { transform: translateX(2px); } 100% { transform: translateX(0); } }
        .timer-display { font-size: 30px; font-weight: 900; color: var(--primary); margin-top: 20px; display: none;}
        @media (max-width: 768px) {
            .welcome-section { flex-direction: column; gap: 20px; padding: 25px; }
            .motivation-box { width: 100%; }
            .tabs-nav { gap: 5px; padding: 8px; }
            .tab-trigger { padding: 8px 10px; font-size: 11px; }
            .tab-trigger .tab-es { display: none; }
            .cards-grid { grid-template-columns: 1fr; }
            .top-nav { flex-direction: column; gap: 10px; padding: 10px; }
            .top-right-container { flex-wrap: wrap; justify-content: center; }
            .section-header .sec-es { display: none; }
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
            <div class="v-divider"></div>
            <div class="social-icons">
                <a href="https://www.facebook.com/institutoamigos1" target="_blank"><i class="fab fa-facebook-f"></i></a>
                <a href="https://www.instagram.com/instituto_amigos1/" target="_blank"><i class="fab fa-instagram"></i></a>
                <a href="https://www.tiktok.com/@espanolconamigos" target="_blank"><i class="fab fa-tiktok"></i></a>
                <a href="https://wa.me/+201108425280" target="_blank"><i class="fab fa-whatsapp"></i></a>
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
                <h2><span class="es-greet">¡!</span> أهلاً بيك يا {{ student.username }}! 👋</h2>
                <p>جاهز لدرس النهاردة؟ كمل في طريقك وإحنا في ضهرك دايماً!</p>
            </div>
            <div class="motivation-box">
                <i class="fa-solid fa-lightbulb" style="font-size: 22px; margin-bottom: 8px;"></i>
                <p style="font-size: 15px;">{{ quote }}</p>
            </div>
        </header>

        <nav class="tabs-nav">
            <button class="tab-trigger active" onclick="switchTab(event, 'lectures-tab')">
                <i class="fa-solid fa-video tab-icon"></i> الدروس <span class="tab-es">Lecciones</span>
            </button>
            <button class="tab-trigger" onclick="switchTab(event, 'exercises-tab')">
                <i class="fa-solid fa-pen-ruler tab-icon"></i> التمارين <span class="tab-es">Ejercicios</span>
            </button>
            <button class="tab-trigger" onclick="switchTab(event, 'vocab-tab')">
                <i class="fa-solid fa-spell-check tab-icon"></i> الكلمات <span class="tab-es">Vocabulario</span>
            </button>
            <button class="tab-trigger" onclick="switchTab(event, 'schedule-tab')">
                <i class="fa-solid fa-calendar-days tab-icon"></i> الجداول <span class="tab-es">Horarios</span>
            </button>
            <button class="tab-trigger" onclick="switchTab(event, 'shadowing-tab')">
                <i class="fa-solid fa-headphones tab-icon"></i> الشادوينج <span class="tab-es">Shadowing</span>
            </button>
            <button class="tab-trigger" onclick="switchTab(event, 'games-tab')">
                <i class="fa-solid fa-gamepad tab-icon"></i> الألعاب <span class="tab-es">Juegos</span>
            </button>
            <button class="tab-trigger" onclick="switchTab(event, 'videos-tab')">
                <i class="fa-brands fa-youtube tab-icon"></i> فيديوهات <span class="tab-es">Vídeos</span>
            </button>
            <button class="tab-trigger" onclick="switchTab(event, 'wheel-tab')">
                <i class="fa-solid fa-dharmachakra tab-icon"></i> العجلة <span class="tab-es">Ruleta</span>
            </button>
        </nav>

        <div id="lectures-tab" class="tab-content active">
            <div class="section-header">
                <i class="fa-solid fa-book-open sec-icon" style="color: var(--primary);"></i>
                <div>
                    <div class="sec-title">الدروس والشرح</div>
                    <div class="sec-subtitle">شروحات مفصلة لكل درس في مستوى {{ student.level }}</div>
                </div>
                <span class="sec-es">Las Lecciones</span>
            </div>
            <div class="cards-grid">
                {% for lesson in lessons_list %}
                <div class="course-card">
                    <div class="card-accent card-accent-red"></div>
                    <div class="card-header">
                        <span class="lesson-number ln-red">Unidad {{ loop.index }}</span>
                        <i class="fa-solid fa-book-open" style="color: #ccc;"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ lesson.title }}</h4>
                        <div class="card-es-hint">Lección {{ loop.index }}</div>
                        <a href="/page/{{ student.level }}/{{ lesson.file }}" class="card-action-btn btn-lecture" target="_blank"><i class="fa-solid fa-play-circle"></i> ابدأ الشرح</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="exercises-tab" class="tab-content">
            <div class="section-header">
                <i class="fa-solid fa-pen-ruler sec-icon" style="color: #b8860b;"></i>
                <div>
                    <div class="sec-title">التمارين والتقييم</div>
                    <div class="sec-subtitle">اختبر نفسك وقيس مستواك بعد كل درس</div>
                </div>
                <span class="sec-es">Los Ejercicios</span>
            </div>
            <div class="cards-grid">
                {% for exercise in exercises_list %}
                <div class="course-card">
                    <div class="card-accent card-accent-gold"></div>
                    <div class="card-header">
                        <span class="lesson-number ln-gold">Ejercicio {{ loop.index }}</span>
                        <i class="fa-solid fa-star" style="color: var(--accent);"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ exercise.title }}</h4>
                        <div class="card-es-hint">Práctica {{ loop.index }}</div>
                        <a href="/page/{{ student.level }}/{{ exercise.file }}" class="card-action-btn btn-exercise" target="_blank"><i class="fa-solid fa-pencil"></i> ابدأ التمرين</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="vocab-tab" class="tab-content">
            <div class="section-header vocab-header">
                <i class="fa-solid fa-language sec-icon" style="color: var(--vocab-color);"></i>
                <div>
                    <div class="sec-title">📖 الكلمات - Vocabulario</div>
                    <div class="sec-subtitle">كلمات كل درس بالإسباني والمصري عشان تحفظها كويس</div>
                </div>
                <span class="sec-es" style="color: var(--vocab-color);">Palabras Nuevas</span>
            </div>
            <div class="cards-grid">
                {% for vocab in vocab_list %}
                <div class="course-card">
                    <div class="card-accent card-accent-purple"></div>
                    <div class="card-header" style="background: #faf5ff;">
                        <span class="lesson-number ln-purple"><i class="fa-solid fa-spell-check"></i> الدرس {{ loop.index }}</span>
                        <i class="fa-solid fa-language" style="color: var(--vocab-color);"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ vocab.title }}</h4>
                        <div class="card-es-hint" style="color: var(--vocab-color); opacity: 0.6;">Vocabulario {{ loop.index }}</div>
                        <a href="/page/{{ student.level }}/{{ vocab.file }}" class="card-action-btn btn-vocab" target="_blank"><i class="fa-solid fa-book-bookmark"></i> افتح الكلمات</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="schedule-tab" class="tab-content">
            <div class="section-header schedule-header">
                <i class="fa-solid fa-calendar-check sec-icon" style="color: var(--secondary);"></i>
                <div>
                    <div class="sec-title">جداول المذاكرة</div>
                    <div class="sec-subtitle">نظم وقتك وذاكر صح مع الجدول المخصص لكل درس</div>
                </div>
                <span class="sec-es">Los Horarios</span>
            </div>
            <div class="cards-grid">
                {% for schedule in schedules_list %}
                <div class="course-card">
                    <div class="card-accent card-accent-blue"></div>
                    <div class="card-header" style="background: #f8fafc;">
                        <span class="lesson-number ln-blue">الجدول {{ loop.index }}</span>
                        <i class="fa-solid fa-calendar-days" style="color: var(--secondary);"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ schedule.title }}</h4>
                        <div class="card-es-hint">Horario {{ loop.index }}</div>
                        <a href="/page/{{ student.level }}/{{ schedule.file }}" target="_blank" class="card-action-btn btn-schedule"><i class="fa-solid fa-external-link-alt"></i> افتح الجدول</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="shadowing-tab" class="tab-content">
            <div class="section-header shadow-header">
                <i class="fa-solid fa-headphones sec-icon" style="color: var(--shadow-color);"></i>
                <div>
                    <div class="sec-title">🎧 الشادوينج - Shadowing</div>
                    <div class="sec-subtitle">اسمع وردد وراهم عشان نطقك يبقى زي الإسبان بالظبط</div>
                </div>
                <span class="sec-es" style="color: var(--shadow-color);">Repetir y Mejorar</span>
            </div>
            <div class="cards-grid">
                {% for shadow in shadowing_list %}
                <div class="course-card">
                    <div class="card-accent card-accent-orange"></div>
                    <div class="card-header" style="background: #fff8f0;">
                        <span class="lesson-number ln-orange"><i class="fa-solid fa-headphones"></i> الدرس {{ loop.index }}</span>
                        <i class="fa-solid fa-microphone" style="color: var(--shadow-color);"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ shadow.title }}</h4>
                        <div class="card-es-hint" style="color: var(--shadow-color); opacity: 0.6;">Shadowing {{ loop.index }}</div>
                        <a href="/page/{{ student.level }}/{{ shadow.file }}" class="card-action-btn btn-shadow" target="_blank"><i class="fa-solid fa-headphones"></i> ابدأ الشادوينج</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="games-tab" class="tab-content">
            <div class="section-header games-header">
                <i class="fa-solid fa-puzzle-piece sec-icon" style="color: #2ecc71;"></i>
                <div>
                    <div class="sec-title">الألعاب التفاعلية</div>
                    <div class="sec-subtitle">اتعلم وانت بتلعب.. طريقة ممتعة لتثبيت المعلومة</div>
                </div>
                <span class="sec-es" style="color: #2ecc71;">¡A Jugar!</span>
            </div>
            <div class="cards-grid">
                {% for game in games_list %}
                <div class="course-card">
                    <div class="card-accent card-accent-green"></div>
                    <div class="card-header" style="background: #f0fff4;">
                        <span class="lesson-number ln-green"><i class="fa-solid fa-gamepad"></i> لعبة {{ loop.index }}</span>
                        <i class="fa-solid fa-trophy" style="color: #f39c12;"></i>
                    </div>
                    <div class="card-body">
                        <h4>{{ game.title }}</h4>
                        <div class="card-es-hint" style="color: #2ecc71;">Juego {{ loop.index }}</div>
                        <a href="/page/{{ student.level }}/{{ game.file }}" target="_blank" class="card-action-btn btn-game"><i class="fa-solid fa-play"></i> ادخل العب</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="videos-tab" class="tab-content">
            <div class="section-header">
                <i class="fa-brands fa-youtube sec-icon" style="color: #ff0000;"></i>
                <div>
                    <div class="sec-title">مكتبة الفيديوهات</div>
                    <div class="sec-subtitle">شروحات مرئية لمستوى {{ student.level }}</div>
                </div>
                <span class="sec-es" style="color: #ff0000;">Los Vídeos</span>
            </div>
            <div class="cards-grid">
                {% for video in videos_list %}
                <div class="course-card" style="padding: 15px;">
                    <div class="card-accent card-accent-red"></div>
                    <div class="video-container">
                        <iframe src="https://www.youtube.com/embed/{{ video.youtube_id }}" title="{{ video.title }}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                    <h4 style="margin-top: 15px; font-size: 15px; padding: 0 10px;">{{ video.title }}</h4>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="wheel-tab" class="tab-content">
            <div class="wheel-box">
                <h3 style="color: var(--secondary); margin-bottom: 10px;">
                    <i class="fa-solid fa-microphone-lines"></i> عجلة التحدث والطلاقة - 
                    <span style="font-family: 'Reenie Beanie', cursive; color: var(--primary); font-size: 28px;">La Ruleta</span>
                </h3>
                <p style="color: var(--text-muted);">اضغط على الزر ليتم اختيار موضوع عشوائي مناسب لمستواك ({{ student.level }}). تحدث عنه لمدة دقيقتين بدون توقف!</p>
                <div id="topicDisplay" class="wheel-display">اضغط على "لف العجلة" لبدء التحدي! 🎯</div>
                <button id="spinBtn" class="spin-btn" onclick="spinWheel()"><i class="fa-solid fa-rotate"></i> لف العجلة</button>
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
                    display.innerHTML = '<span style="color: var(--primary); font-size: 26px;">🎯 ' + finalTopic + '</span>';
                    btn.innerHTML = '<i class="fa-solid fa-rotate"></i> جرب موضوع تاني';
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

# =====================================================================
# لوحة المدرس (TEACHER_DASHBOARD_HTML)
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
        
        .main-tabs { display: flex; justify-content: center; gap: 20px; background: white; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 30px; }
        .m-tab { background: none; border: none; font-size: 18px; font-weight: bold; color: #555; padding: 10px 20px; cursor: pointer; border-bottom: 3px solid transparent; transition: 0.3s; }
        .m-tab.active { color: #1a1a2e; border-color: #f39c12; }

        .container { max-width: 1200px; margin: 0 auto; padding: 0 15px 50px; }
        
        .level-selector { background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .level-selector select { padding: 10px 20px; font-size: 16px; font-family: 'Cairo'; border: 2px solid #ccc; border-radius: 8px; font-weight: bold; }
        
        .content-tabs { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; justify-content: center; }
        .c-tab { background: white; border: 1px solid #ddd; padding: 8px 15px; border-radius: 8px; cursor: pointer; font-weight: bold; color: #555; }
        .c-tab.active { background: #f39c12; color: white; border-color: #f39c12; }
        .c-tab.multi-games { background: #8e44ad; color: white; border-color: #8e44ad; }
        .c-tab.multi-games.active { background: #9b59b6; box-shadow: 0 0 10px rgba(142, 68, 173, 0.5); }
        
        .tab-section { display: none; }
        .tab-section.active { display: block; animation: fadeIn 0.3s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .course-card { background: white; border-radius: 15px; border: 1px solid #eee; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.03); text-align: center; }
        .course-card .header { background: #f8f9fa; padding: 15px; font-weight: bold; color: #1a1a2e; border-bottom: 1px solid #eee; }
        .course-card .body { padding: 20px; }
        .course-card a { display: inline-block; width: 100%; padding: 10px; background: #f39c12; color: #1a1a2e; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 10px; }
        .course-card a.multi-btn { background: #8e44ad; color: white; }

        .grading-section { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .students-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; margin-top: 20px; }
        .student-list-card { background: #f8f9fa; border: 1px solid #ddd; border-radius: 10px; padding: 15px; cursor: pointer; transition: 0.3s; }
        .student-list-card:hover { border-color: #f39c12; transform: translateY(-2px); }
        .badge { padding: 4px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; margin-left: 5px; }
        .badge.pending { background: #ffeaa7; color: #d35400; }
        .badge.correct { background: #d4efdf; color: #27ae60; }
        .badge.wrong { background: #fadbd8; color: #c0392b; }
        
        .student-detail { background: #fff; border: 2px solid #f39c12; border-radius: 15px; padding: 20px; margin-top: 20px; }
        .pq-box { background: #fdfefe; border: 1px solid #eee; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-right: 4px solid #f39c12; }
        .pq-ans { background: #f4f6f7; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 16px; margin: 10px 0; direction: ltr; text-align: left;}
        .v-btn { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-left: 5px; }
        .v-btn.correct { background: #e9f7ef; color: #27ae60; border: 1px solid #27ae60; }
        .v-btn.correct.active { background: #27ae60; color: white; }
        .v-btn.wrong { background: #fdedec; color: #c0392b; border: 1px solid #c0392b; }
        .v-btn.wrong.active { background: #c0392b; color: white; }
        .f-input { padding: 8px; border: 1px solid #ccc; border-radius: 5px; width: 250px; font-family: 'Cairo'; }
        .submit-btn { background: #27ae60; color: white; padding: 12px 25px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; margin-top: 15px; }
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="brand"><i class="fa-solid fa-chalkboard-user"></i> لوحة المدرس</div>
        <div class="user-actions">
            <span style="margin-left: 15px;">أهلاً يا أستاذ/ة <strong>{{ teacher.fullName if teacher.fullName else teacher.username }}</strong></span>
            <a href="/logout">خروج <i class="fa-solid fa-arrow-right-from-bracket"></i></a>
        </div>
    </nav>

    <div class="main-tabs">
        <button class="m-tab active" onclick="switchMainTab('materials')"><i class="fa-solid fa-book"></i> المناهج والمواد</button>
        <button class="m-tab" onclick="switchMainTab('grading'); refreshGradingData();"><i class="fa-solid fa-check-double"></i> تصحيح الواجبات</button>
    </div>

    <div class="container">
        <div id="materials-view">
            <div class="level-selector">
                <label style="font-weight:bold; font-size:18px;">اختر المستوى لعرض محتواه:</label><br><br>
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
                <button class="c-tab" onclick="switchContentTab('vocab')">الكلمات</button>
                <button class="c-tab" onclick="switchContentTab('schedules')">الجداول</button>
                <button class="c-tab" onclick="switchContentTab('shadowing')">الشادوينج</button>
                <button class="c-tab" onclick="switchContentTab('games')">الألعاب الفردية</button>
                <button class="c-tab multi-games" onclick="switchContentTab('multiplayer')"><i class="fa-solid fa-users"></i> ألعاب جماعية</button>
            </div>

            <div id="lectures" class="tab-section active">
                <div class="cards-grid">
                    {% for item in materials.lessons %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الدرس</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div id="exercises" class="tab-section">
                <div class="cards-grid">
                    {% for item in materials.exercises %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح التمرين</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="vocab" class="tab-section">
                <div class="cards-grid">
                    {% for item in materials.vocab %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الكلمات</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="schedules" class="tab-section">
                <div class="cards-grid">
                    {% for item in materials.schedules %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الجدول</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="shadowing" class="tab-section">
                <div class="cards-grid">
                    {% for item in materials.shadowing %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح الشادوينج</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="games" class="tab-section">
                <div class="cards-grid">
                    {% for item in materials.games %}
                    <div class="course-card">
                        <div class="header">{{ item.title }}</div>
                        <div class="body"><a href="/page/{{ current_level }}/{{ item.file }}" target="_blank">افتح اللعبة</a></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="multiplayer" class="tab-section">
                <div class="cards-grid">
                    {% for item in materials.multi_games %}
                    <div class="course-card" style="border-color: #8e44ad;">
                        <div class="header" style="background: #f4ecf7; color: #8e44ad;">{{ item.title }}</div>
                        <div class="body">
                            <p style="font-size: 13px; color: #666; margin-bottom: 10px;">خاصة بالعرض داخل الفصل</p>
                            <a href="/page/{{ current_level }}/{{ item.file }}" target="_blank" class="multi-btn">تشغيل اللعبة <i class="fa-solid fa-play"></i></a>
                        </div>
                    </div>
                    {% else %}
                    <p style="text-align:center; width:100%; color:#888;">لا توجد ألعاب جماعية لهذا المستوى حالياً.</p>
                    {% endfor %}
                </div>
            </div>
            
            {% else %}
            <p style="text-align:center; color:#777; font-size:18px; margin-top:50px;">يرجى اختيار المستوى من القائمة بالأعلى لعرض المحتوى.</p>
            {% endif %}
        </div>

        <div id="grading-view" style="display:none;" class="grading-section">
            <h2 style="color: #f39c12; margin-bottom: 15px;"><i class="fa-solid fa-file-pen"></i> تصحيح واجبات الطلبة</h2>
            
            <div id="studentsListView">
                <button onclick="refreshGradingData()" style="padding:8px 15px; background:#3498db; color:white; border:none; border-radius:5px; cursor:pointer;">🔄 تحديث القائمة</button>
                <div id="studentsListContent" class="students-list">جاري التحميل...</div>
            </div>

            <div id="studentDetailView" style="display:none;">
                <button onclick="backToGradingList()" style="padding:8px 15px; background:#95a5a6; color:white; border:none; border-radius:5px; cursor:pointer; margin-bottom:15px;">⬅️ رجوع للقائمة</button>
                <div id="studentDetailContent" class="student-detail"></div>
            </div>
        </div>

    </div>

    <script>
        function switchMainTab(tab) {
            document.querySelectorAll('.m-tab').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById('materials-view').style.display = tab === 'materials' ? 'block' : 'none';
            document.getElementById('grading-view').style.display = tab === 'grading' ? 'block' : 'none';
        }

        function switchContentTab(tabId) {
            document.querySelectorAll('.c-tab').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.tab-section').forEach(s => s.classList.remove('active'));
            if(document.getElementById(tabId)) document.getElementById(tabId).classList.add('active');
        }

        const SCRIPT_URL = '{{ script_url }}';
        const TEACHER_USER = '{{ teacher.username }}';
        let currentReviews = {};
        let currentStudent = null;

        async function refreshGradingData() {
            const container = document.getElementById('studentsListContent');
            container.innerHTML = 'جاري التحميل... ⏳';
            try {
                const res = await fetch(SCRIPT_URL + '?action=getPendingReviews&_t=' + Date.now());
                const data = await res.json();
                if (data.status === 'success') {
                    if(!data.students || data.students.length === 0) {
                        container.innerHTML = '<p style="color:green; font-weight:bold;">✅ كل الإجابات تم تصحيحها!</p>';
                        return;
                    }
                    let html = '';
                    data.students.forEach(s => {
                        html += `
                        <div class="student-list-card" onclick="openStudentGrading('${s.username}', '${s.lessonId}')">
                            <h3 style="color:#2c3e50;">👤 ${s.fullName || s.username}</h3>
                            <p style="color:#7f8c8d; font-size:14px; margin-bottom:10px;">الدرس: ${s.lessonId}</p>
                            <div>
                                <span class="badge pending">⏳ ${s.pendingCount} بانتظار</span>
                            </div>
                        </div>`;
                    });
                    container.innerHTML = html;
                }
            } catch (err) {
                container.innerHTML = '❌ خطأ في تحميل البيانات';
            }
        }

        async function openStudentGrading(username, lessonId) {
            document.getElementById('studentsListView').style.display = 'none';
            document.getElementById('studentDetailView').style.display = 'block';
            const container = document.getElementById('studentDetailContent');
            container.innerHTML = 'جاري تحميل إجابات الطالب... ⏳';
            currentReviews = {};

            try {
                const res = await fetch(SCRIPT_URL + '?action=getStudentDetails&username=' + username + '&lessonId=' + lessonId);
                const data = await res.json();
                if (data.status === 'success') {
                    currentStudent = data.student;
                    renderStudentDetails(container);
                }
            } catch (err) {
                container.innerHTML = '❌ خطأ في التحميل';
            }
        }

        function renderStudentDetails(container) {
            const pending = currentStudent.pendingAnswers;
            let html = `<h3>التصحيح للطالب: <span style="color:#e52421;">${currentStudent.fullName || currentStudent.username}</span></h3>`;
            
            Object.keys(pending).forEach(qId => {
                const ans = pending[qId];
                html += `
                <div class="pq-box">
                    <p><strong>السؤال:</strong> ${ans.questionText || qId}</p>
                    <div class="pq-ans">${ans.value}</div>
                    ${ans.expectedAnswer ? `<p style="color:green; font-size:14px;">الإجابة النموذجية: ${ans.expectedAnswer}</p>` : ''}
                    <div style="margin-top:10px;">
                        <button class="v-btn correct" onclick="setVerdict('${qId}', 'correct', this)">✅ صح</button>
                        <button class="v-btn wrong" onclick="setVerdict('${qId}', 'wrong', this)">❌ خطأ</button>
                        <input type="text" class="f-input" placeholder="ملاحظة (اختياري)" data-qid="${qId}">
                    </div>
                </div>`;
            });
            html += `<button class="submit-btn" onclick="submitReviews()">حفظ التصحيح</button>`;
            container.innerHTML = html;
        }

        function setVerdict(qId, verdict, btn) {
            currentReviews[qId] = { verdict: verdict };
            btn.parentElement.querySelectorAll('.v-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }

        function backToGradingList() {
            document.getElementById('studentDetailView').style.display = 'none';
            document.getElementById('studentsListView').style.display = 'block';
            refreshGradingData();
        }

        async function submitReviews() {
            if (Object.keys(currentReviews).length === 0) return alert('لم تقم بتصحيح أي سؤال!');
            
            Object.keys(currentReviews).forEach(qId => {
                const inp = document.querySelector(`.f-input[data-qid="${qId}"]`);
                if(inp) currentReviews[qId].feedback = inp.value;
            });

            const payload = {
                action: 'submitReview',
                username: currentStudent.username,
                lessonId: currentStudent.lessonId,
                teacher: TEACHER_USER,
                reviews: JSON.stringify(currentReviews)
            };

            const url = SCRIPT_URL + '?action=submitReview&data=' + encodeURIComponent(JSON.stringify(payload));
            await fetch(url, { mode: 'no-cors' });
            alert('تم الحفظ بنجاح!');
            backToGradingList();
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
    
    student_lessons = LESSONS_DATA.get(level, [{"title": "درس غير متوفر", "file": "error.html"}])
    student_exercises = EXERCISES_DATA.get(level, [{"title": "تمرين غير متوفر", "file": "error.html"}])
    student_vocab = VOCAB_DATA.get(level, [{"title": "كلمات غير متوفرة", "file": "error.html"}])
    student_schedules = SCHEDULES_DATA.get(level, [{"title": "جدول غير متوفر", "file": "error.html"}])
    student_shadowing = SHADOWING_DATA.get(level, [{"title": "شادوينج غير متوفر", "file": "error.html"}])
    student_games = GAMES_DATA.get(level, [{"title": "لعبة غير متوفرة", "file": "error.html"}])
    student_videos = VIDEOS_DATA.get(level, [{"title": "فيديو ترحيبي", "youtube_id": "dQw4w9WgXcQ"}])
    
    random_quote = random.choice(motivation_quotes)
    
    student_wheel_topics = WHEEL_TOPICS.get(level, ["تحدث عن مهاراتك."])
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

    return render_template_string(
        TEACHER_DASHBOARD_HTML, 
        teacher=teacher, 
        current_level=selected_level, 
        materials=materials,
        script_url=SCRIPT_URL
    )

@app.route('/page/<path:filename>')
def serve_page(filename):
    if 'user' not in session:
        return redirect(url_for('login_student'))
    
    user = session['user']
    role = session.get('role')
    
    # لو مدرس، يقدر يفتح أي ملف، لو طالب يفتح ملفات مستواه بس
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
