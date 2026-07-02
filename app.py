import streamlit as st
import tempfile
import base64
import os
import subprocess
import random
import googletrans
from googletrans import Translator

st.set_page_config(page_title="Let's Learn Accounting with Gesner", layout="wide")

# ---------- Style (Light Purple Theme) ----------
def set_light_purple_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f3e5ff, #d9b3ff, #f3e5ff); }
        .main-header { background: linear-gradient(135deg, #b380ff, #d9b3ff, #b380ff); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #f0e6ff; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, pre, code, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: #1a0b2e !important; }
        .stText { color: #1a0b2e !important; font-size: 1rem; background: transparent !important; }
        .stTabs [role="tab"] { color: #1a0b2e !important; background: rgba(179, 128, 255, 0.2); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: rgba(179, 128, 255, 0.5); color: #1a0b2e !important; }
        .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: #1a0b2e !important; }
        .stButton button { background-color: #b380ff; color: white; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #d9b3ff; color: #1a0b2e; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #f3e5ff, #d9b3ff); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: #1a0b2e !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: #1a0b2e !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #ffffff; border: 1px solid #b380ff; border-radius: 10px; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div { color: #1a0b2e !important; }
        section[data-testid="stSidebar"] .stSelectbox svg { fill: #1a0b2e; }
        section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span { color: #1a0b2e !important; }
        div[data-baseweb="popover"] ul { background-color: #ffffff; border: 1px solid #b380ff; }
        div[data-baseweb="popover"] li { color: #1a0b2e !important; background-color: #ffffff; }
        div[data-baseweb="popover"] li:hover { background-color: #d9b3ff; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#b380ff" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#b380ff"/>
                    <stop offset="50%" stop-color="#d9b3ff"/>
                    <stop offset="100%" stop-color="#b380ff"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📊</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ---------- Language dictionary (UI texts) ----------
LANGUAGES = {
    "English": {
        "code": "en",
        "voice": "en-US-GuyNeural",
        "ui": {
            "title": "📊 Let's Learn Accounting with Gesner",
            "subtitle": "Book 1 – 20 interactive lessons | Cash flow | Budgeting | Market pricing | Saving | Spending wisely",
            "login_title": "🔐 Access Required",
            "login_sub": "Book 1 – Lessons 1 to 20",
            "login_password": "Enter password to access",
            "login_btn": "Login",
            "login_error": "Incorrect password. Access denied.",
            "sidebar_progress": "Your progress",
            "sidebar_completed": "of 20",
            "sidebar_founder": "Founder & Developer:",
            "sidebar_price_label": "Price",
            "sidebar_price": "$299 USD (full book – 20 lessons, source code included)",
            "sidebar_logout": "Logout",
            "lesson_prefix": "Lesson",
            "tabs": ["📚 Symbols & Tables", "🎯 Demonstrations", "✏️ Exercises", "❓ Quiz"],
            "symbols_title": "📊 Key Accounting Terms",
            "table_title": "📋 Reference Table",
            "demo_title": "🎯 Watch and Learn",
            "demo_instruction": "Click the 'Explain & Solve' button for each demonstration. The AI will explain the situation and show the answer.",
            "demo_button": "Explain & Solve",
            "demo_explanation": "💡 Explanation:",
            "demo_solution": "✅ Solution:",
            "exercise_title": "✏️ Practice Exercises",
            "exercise_instruction": "Type your answer in the box and click 'Check Answer'.",
            "exercise_check": "Check",
            "exercise_correct": "Yes, that's correct!",
            "exercise_hint": "Not quite. Try again! Hint: The correct answer is",
            "quiz_title": "📝 Final Quiz",
            "quiz_instruction": "Answer one question from each lesson to test your knowledge.",
            "quiz_check": "Check Lesson",
            "quiz_correct": "Yes, that's correct!",
            "quiz_incorrect": "Incorrect. The correct answer is",
            "quiz_results": "Show Quiz Results",
            "quiz_results_text": "You have answered {correct} out of 20 quiz questions correctly.",
            "congrats": "🎓 Congratulations! You have completed Book 1.",
            "contact": "To continue with Book 2, contact us:",
            "footer_caption": "📊 Let's Learn Accounting with Gesner – Book 1",
            "built_by": "This software accounting Book was built by Gesner Deslandes"
        }
    },
    "French": {
        "code": "fr",
        "voice": "fr-FR-HenriNeural",
        "ui": {
            "title": "📊 Apprenons la comptabilité avec Gesner",
            "subtitle": "Livre 1 – 20 leçons interactives | Flux de trésorerie | Budget | Prix du marché | Épargne | Dépenses intelligentes",
            "login_title": "🔐 Accès requis",
            "login_sub": "Livre 1 – Leçons 1 à 20",
            "login_password": "Entrez le mot de passe pour accéder",
            "login_btn": "Se connecter",
            "login_error": "Mot de passe incorrect. Accès refusé.",
            "sidebar_progress": "Votre progression",
            "sidebar_completed": "sur 20",
            "sidebar_founder": "Fondateur et développeur :",
            "sidebar_price_label": "Prix",
            "sidebar_price": "299 $ USD (livre complet – 20 leçons, code source inclus)",
            "sidebar_logout": "Déconnexion",
            "lesson_prefix": "Leçon",
            "tabs": ["📚 Symboles et tableaux", "🎯 Démonstrations", "✏️ Exercices", "❓ Quiz"],
            "symbols_title": "📊 Termes comptables clés",
            "table_title": "📋 Tableau de référence",
            "demo_title": "🎯 Regardez et apprenez",
            "demo_instruction": "Cliquez sur le bouton « Expliquer et résoudre » pour chaque démonstration. L'IA expliquera la situation et montrera la réponse.",
            "demo_button": "Expliquer et résoudre",
            "demo_explanation": "💡 Explication :",
            "demo_solution": "✅ Solution :",
            "exercise_title": "✏️ Exercices pratiques",
            "exercise_instruction": "Tapez votre réponse dans la case et cliquez sur « Vérifier la réponse ».",
            "exercise_check": "Vérifier",
            "exercise_correct": "Oui, c'est correct !",
            "exercise_hint": "Pas tout à fait. Réessayez ! Indice : la bonne réponse est",
            "quiz_title": "📝 Quiz final",
            "quiz_instruction": "Répondez à une question de chaque leçon pour tester vos connaissances.",
            "quiz_check": "Vérifier la leçon",
            "quiz_correct": "Oui, c'est correct !",
            "quiz_incorrect": "Incorrect. La bonne réponse est",
            "quiz_results": "Afficher les résultats du quiz",
            "quiz_results_text": "Vous avez répondu correctement à {correct} questions sur 20.",
            "congrats": "🎓 Félicitations ! Vous avez terminé le livre 1.",
            "contact": "Pour continuer avec le livre 2, contactez-nous :",
            "footer_caption": "📊 Apprenons la comptabilité avec Gesner – Livre 1",
            "built_by": "Ce logiciel de comptabilité a été construit par Gesner Deslandes"
        }
    },
    "Spanish": {
        "code": "es",
        "voice": "es-ES-AlvaroNeural",
        "ui": {
            "title": "📊 Aprendamos contabilidad con Gesner",
            "subtitle": "Libro 1 – 20 lecciones interactivas | Flujo de efectivo | Presupuesto | Precios de mercado | Ahorro | Gasto inteligente",
            "login_title": "🔐 Acceso requerido",
            "login_sub": "Libro 1 – Lecciones 1 a 20",
            "login_password": "Ingrese la contraseña para acceder",
            "login_btn": "Iniciar sesión",
            "login_error": "Contraseña incorrecta. Acceso denegado.",
            "sidebar_progress": "Tu progreso",
            "sidebar_completed": "de 20",
            "sidebar_founder": "Fundador y desarrollador:",
            "sidebar_price_label": "Precio",
            "sidebar_price": "$299 USD (libro completo – 20 lecciones, código fuente incluido)",
            "sidebar_logout": "Cerrar sesión",
            "lesson_prefix": "Lección",
            "tabs": ["📚 Símbolos y tablas", "🎯 Demostraciones", "✏️ Ejercicios", "❓ Cuestionario"],
            "symbols_title": "📊 Términos contables clave",
            "table_title": "📋 Tabla de referencia",
            "demo_title": "🎯 Mira y aprende",
            "demo_instruction": "Haz clic en el botón « Explicar y resolver » para cada demostración. La IA explicará la situación y mostrará la respuesta.",
            "demo_button": "Explicar y resolver",
            "demo_explanation": "💡 Explicación:",
            "demo_solution": "✅ Solución:",
            "exercise_title": "✏️ Ejercicios prácticos",
            "exercise_instruction": "Escribe tu respuesta en el cuadro y haz clic en « Verificar respuesta ».",
            "exercise_check": "Verificar",
            "exercise_correct": "¡Sí, es correcto!",
            "exercise_hint": "No es correcto. ¡Inténtalo de nuevo! Pista: la respuesta correcta es",
            "quiz_title": "📝 Cuestionario final",
            "quiz_instruction": "Responde una pregunta de cada lección para evaluar tus conocimientos.",
            "quiz_check": "Verificar lección",
            "quiz_correct": "¡Sí, es correcto!",
            "quiz_incorrect": "Incorrecto. La respuesta correcta es",
            "quiz_results": "Mostrar resultados del cuestionario",
            "quiz_results_text": "Has respondido correctamente a {correct} de 20 preguntas.",
            "congrats": "🎓 ¡Felicitaciones! Has completado el libro 1.",
            "contact": "Para continuar con el libro 2, contáctanos:",
            "footer_caption": "📊 Aprendamos contabilidad con Gesner – Libro 1",
            "built_by": "Este software de contabilidad fue construido por Gesner Deslandes"
        }
    }
}

# ---------- Translation helper ----------
translator = Translator()

def translate_lesson_content(lesson_dict, dest_lang, lesson_num):
    """
    Translate a lesson dictionary (title, symbols, table, demos, interactive)
    from English to the destination language.
    Caches results in session_state to avoid repeated translations.
    """
    if "translations" not in st.session_state:
        st.session_state.translations = {}

    cache_key = f"lesson_{lesson_num}_{dest_lang}"
    if cache_key in st.session_state.translations:
        return st.session_state.translations[cache_key]

    # If language is English, return original without translation
    if dest_lang == "en":
        st.session_state.translations[cache_key] = lesson_dict
        return lesson_dict

    translated = {}
    # Translate title
    translated["title"] = translator.translate(lesson_dict["title"], dest=dest_lang).text if lesson_dict.get("title") else ""
    # Translate symbols
    translated["symbols"] = translator.translate(lesson_dict["symbols"], dest=dest_lang).text if lesson_dict.get("symbols") else ""
    # Translate table
    translated["table"] = translator.translate(lesson_dict["table"], dest=dest_lang).text if lesson_dict.get("table") else ""

    # Translate demos
    demos = lesson_dict.get("demos", [])
    translated_demos = []
    for d in demos:
        question = translator.translate(d["question"], dest=dest_lang).text if d.get("question") else ""
        explanation = translator.translate(d["explanation"], dest=dest_lang).text if d.get("explanation") else ""
        answer = d["answer"]  # keep answer as is (numbers, short text)
        translated_demos.append({"question": question, "explanation": explanation, "answer": answer})
    translated["demos"] = translated_demos

    # Translate interactive
    interactive = lesson_dict.get("interactive", [])
    translated_interactive = []
    for item in interactive:
        q = translator.translate(item["question"], dest=dest_lang).text if item.get("question") else ""
        ans = item["answer"]
        translated_interactive.append({"question": q, "answer": ans})
    translated["interactive"] = translated_interactive

    # Cache and return
    st.session_state.translations[cache_key] = translated
    return translated

# ---------- Accounting Lesson Content ----------
def get_lesson_data(lesson_num, lang_code):
    # Original English lessons
    lessons_en = {
        1: {
            "title": "What is Accounting? Cash In and Cash Out",
            "symbols": "💰 Cash In (Revenue) | 💸 Cash Out (Expenses) | 📈 Profit = Cash In - Cash Out",
            "table": "Simple cash flow example:\nCash In: $500 (allowance)\nCash Out: $200 (snacks, games)\nProfit: $300",
            "demos": [
                {"question": "You earn $100 from chores and spend $30 on a book. How much do you save?", "explanation": "Cash In = $100, Cash Out = $30, Savings = $100 - $30 = $70.", "answer": 70},
                {"question": "Your business sells 10 cupcakes at $3 each. What is the total Cash In?", "explanation": "10 × $3 = $30 Cash In.", "answer": 30},
                {"question": "You spend $15 on pizza and $10 on a movie ticket. Total Cash Out?", "explanation": "$15 + $10 = $25 Cash Out.", "answer": 25}
            ],
            "interactive": [
                {"question": "You earn $50 and spend $20. How much do you save?", "answer": 30},
                {"question": "You sell 8 lemonades at $2 each. Cash In?", "answer": 16},
                {"question": "You buy a book for $12 and a pen for $3. Total Cash Out?", "answer": 15}
            ]
        },
        2: {
            "title": "Sources of Income (Cash In)",
            "symbols": "💵 Wage | 💼 Business | 🏦 Interest | 🎁 Gifts",
            "table": "Common income sources:\nWage: $15/hr, 40 hrs/week → $600/week\nBusiness: selling handmade items\nInterest: bank savings",
            "demos": [
                {"question": "You work 5 hours at $10/hour. How much do you earn?", "explanation": "5 × $10 = $50 Cash In.", "answer": 50},
                {"question": "You sell 20 cookies at $2 each. Total Cash In?", "explanation": "20 × $2 = $40 Cash In.", "answer": 40},
                {"question": "You receive $25 as a birthday gift. Cash In?", "explanation": "Gift = $25 Cash In.", "answer": 25}
            ],
            "interactive": [
                {"question": "Work 8 hours at $12/hour. Earnings?", "answer": 96},
                {"question": "Sell 15 bracelets at $4 each. Cash In?", "answer": 60},
                {"question": "Receive $50 as a graduation gift. Cash In?", "answer": 50}
            ]
        },
        3: {
            "title": "Types of Expenses (Cash Out)",
            "symbols": "🏠 Rent | 🍔 Food | 🚗 Transport | 🎮 Entertainment | 📚 Education",
            "table": "Monthly expense example:\nRent: $500\nFood: $200\nTransport: $100\nEntertainment: $50\nTotal: $850",
            "demos": [
                {"question": "You pay $300 for rent and $120 for groceries. Total Cash Out?", "explanation": "$300 + $120 = $420.", "answer": 420},
                {"question": "You spend $15 on lunch and $5 on coffee. Total Cash Out?", "explanation": "$15 + $5 = $20.", "answer": 20},
                {"question": "You buy a $30 video game and a $10 snack. Total Cash Out?", "explanation": "$30 + $10 = $40.", "answer": 40}
            ],
            "interactive": [
                {"question": "Rent $450, Food $180, Transport $70. Total?", "answer": 700},
                {"question": "Lunch $12, Coffee $4, Snack $3. Total?", "answer": 19},
                {"question": "Book $25, Stationery $15. Total?", "answer": 40}
            ]
        },
        4: {
            "title": "Budgeting Basics",
            "symbols": "📋 Budget = Planned Cash In and Cash Out",
            "table": "Sample monthly budget:\nIncome: $1000\nRent: $300\nFood: $200\nEntertainment: $100\nSavings: $400",
            "demos": [
                {"question": "You earn $800 and plan to spend $300 on rent and $200 on food. How much can you save?", "explanation": "$800 - $300 - $200 = $300 savings.", "answer": 300},
                {"question": "Your budget: Income $1200, Expenses: Rent $400, Transport $150, Food $250. What's left?", "explanation": "$1200 - $400 - $150 - $250 = $400 left.", "answer": 400},
                {"question": "You want to save $200 from a $600 income. How much can you spend?", "explanation": "Spending = $600 - $200 = $400.", "answer": 400}
            ],
            "interactive": [
                {"question": "Income $900, Expenses: Rent $350, Food $200, Entertainment $80. Left?", "answer": 270},
                {"question": "Budget: Income $1000, Expenses $700. Savings?", "answer": 300},
                {"question": "Want to save $150 from $500 income. Spending?", "answer": 350}
            ]
        },
        5: {
            "title": "Saving Money – Why and How",
            "symbols": "🏦 Save for goals | 📈 Compound interest | 🎯 Emergency fund",
            "table": "Saving example:\nGoal: buy a bike for $200\nSave $20 per week → 10 weeks",
            "demos": [
                {"question": "You save $15 per week. How much in 4 weeks?", "explanation": "$15 × 4 = $60 saved.", "answer": 60},
                {"question": "You need $120 for a new game. Save $10 per week. How many weeks?", "explanation": "$120 ÷ $10 = 12 weeks.", "answer": 12},
                {"question": "You have $100 saved and add $20 each month. How much after 3 months?", "explanation": "$100 + ($20×3) = $160.", "answer": 160}
            ],
            "interactive": [
                {"question": "Save $8 per week for 5 weeks. Total?", "answer": 40},
                {"question": "Need $80, save $5 per week. Weeks?", "answer": 16},
                {"question": "Start with $50, add $25 monthly for 4 months. Total?", "answer": 150}
            ]
        },
        6: {
            "title": "Market Pricing – How Prices Are Set",
            "symbols": "📈 Supply | 📉 Demand | 💲 Equilibrium price",
            "table": "Price example:\nIf supply is high and demand low → price falls\nIf supply low and demand high → price rises",
            "demos": [
                {"question": "A toy is popular, demand is high, supply is limited. Will the price go up or down?", "explanation": "High demand + low supply → price goes up.", "answer": "up"},
                {"question": "A farmer has too many apples, demand is normal. What happens to price?", "explanation": "High supply + normal demand → price goes down.", "answer": "down"},
                {"question": "If a new phone is released and many people want it, what happens to price?", "explanation": "High demand → price tends to rise.", "answer": "rises"}
            ],
            "interactive": [
                {"question": "If supply of masks is low and demand is high, price goes up or down?", "answer": "up"},
                {"question": "If supply of gas is high and demand is low, price goes up or down?", "answer": "down"},
                {"question": "If a new game has huge demand and limited copies, price likely?", "answer": "rises"}
            ]
        },
        7: {
            "title": "Needs vs. Wants",
            "symbols": "✅ Needs (essential) | ❌ Wants (optional)",
            "table": "Needs: food, water, shelter, clothing\nWants: video games, designer shoes, vacations",
            "demos": [
                {"question": "Is buying a new smartphone a need or a want?", "explanation": "A smartphone is often a want, unless your old one is broken for work.", "answer": "want"},
                {"question": "Is buying groceries a need or a want?", "explanation": "Groceries are a need – you must eat to survive.", "answer": "need"},
                {"question": "Is a monthly gym membership a need or a want?", "explanation": "Gym is a want – you can exercise for free outside.", "answer": "want"}
            ],
            "interactive": [
                {"question": "Water bill – need or want?", "answer": "need"},
                {"question": "Brand new sneakers – need or want?", "answer": "want"},
                {"question": "Rent – need or want?", "answer": "need"}
            ]
        },
        8: {
            "title": "Opportunity Cost – The Cost of Choices",
            "symbols": "⚖️ Opportunity cost = value of next best alternative",
            "table": "Example: If you spend $20 on a movie, you cannot buy a book. The opportunity cost is the book.",
            "demos": [
                {"question": "You have $30. You can buy a pizza or a book. If you choose the book, what is the opportunity cost?", "explanation": "The opportunity cost is the pizza you gave up.", "answer": "pizza"},
                {"question": "You can work 5 hours and earn $50, or go to a concert. If you work, what is the opportunity cost?", "explanation": "The opportunity cost is the concert you missed.", "answer": "concert"},
                {"question": "You have one hour. You can study or play video games. If you choose to study, what is the opportunity cost?", "explanation": "The opportunity cost is the gaming time you gave up.", "answer": "gaming time"}
            ],
            "interactive": [
                {"question": "You can buy a jacket or a backpack. Choose backpack – opportunity cost?", "answer": "jacket"},
                {"question": "You can go to a friend's party or work overtime. Work overtime – opportunity cost?", "answer": "party"},
                {"question": "You have 30 minutes. Exercise or read. Exercise – opportunity cost?", "answer": "reading"}
            ]
        },
        9: {
            "title": "Tracking Expenses – Keeping Records",
            "symbols": "📝 Expense log | 🧾 Receipts | 📊 Monthly summary",
            "table": "Track every small expense to see where money goes.",
            "demos": [
                {"question": "You log: Mon: $5 coffee, Tue: $10 lunch, Wed: $3 snack. Total for 3 days?", "explanation": "$5+$10+$3 = $18.", "answer": 18},
                {"question": "You spend $15 on gas, $20 on groceries, $8 on snacks. Total?", "explanation": "$15+$20+$8 = $43.", "answer": 43},
                {"question": "You track $4 on bus fare, $6 on breakfast, $2 on water. Total?", "explanation": "$4+$6+$2 = $12.", "answer": 12}
            ],
            "interactive": [
                {"question": "Coffee $6, Lunch $12, Snack $4. Total?", "answer": 22},
                {"question": "Bus $3, Breakfast $7, Magazine $5. Total?", "answer": 15},
                {"question": "Groceries $28, Cleaning supplies $12. Total?", "answer": 40}
            ]
        },
        10: {
            "title": "Emergency Fund – Be Prepared",
            "symbols": "🆘 Emergency = unexpected expenses | 🏦 Save 3-6 months of expenses",
            "table": "If your monthly expenses are $500, aim for $1500 - $3000 in emergency fund.",
            "demos": [
                {"question": "Monthly expenses $600. How much for 3 months?", "explanation": "$600 × 3 = $1800.", "answer": 1800},
                {"question": "You have $1000 saved. Is that enough for 2 months of $400 expenses?", "explanation": "2 × $400 = $800, so yes, $1000 is enough.", "answer": "yes"},
                {"question": "You save $50 each month for emergency. After 12 months, how much?", "explanation": "$50 × 12 = $600.", "answer": 600}
            ],
            "interactive": [
                {"question": "Monthly expenses $300. 6 months emergency fund?", "answer": 1800},
                {"question": "Have $1200, monthly expenses $450. Enough for 2 months?", "answer": "yes"},
                {"question": "Save $30/month for 10 months. Total?", "answer": 300}
            ]
        },
        11: {
            "title": "Introduction to Investing",
            "symbols": "📈 Stocks | 💰 Dividends | 📊 Risk & Return",
            "table": "Investing grows money over time. Higher risk may bring higher returns.",
            "demos": [
                {"question": "You invest $100 at 10% annual return. After 1 year, how much?", "explanation": "$100 + 10% of $100 = $110.", "answer": 110},
                {"question": "If you invest $200 at 5% return, after 1 year?", "explanation": "$200 + 5% of $200 = $210.", "answer": 210},
                {"question": "You invest $50 each month for 6 months. Total invested?", "explanation": "$50 × 6 = $300.", "answer": 300}
            ],
            "interactive": [
                {"question": "Invest $150 at 8% return. After 1 year?", "answer": 162},
                {"question": "Invest $80 at 6% return. After 1 year?", "answer": 84.8},
                {"question": "Invest $40 monthly for 5 months. Total?", "answer": 200}
            ]
        },
        12: {
            "title": "Understanding Debt",
            "symbols": "💳 Credit card debt | 🏦 Loan | 💸 Interest",
            "table": "Borrowing money costs interest. Pay back as soon as possible.",
            "demos": [
                {"question": "You borrow $500 at 10% interest per year. How much interest after one year?", "explanation": "10% of $500 = $50 interest.", "answer": 50},
                {"question": "You owe $200 on a credit card with 20% annual interest. Interest for one year?", "explanation": "20% of $200 = $40.", "answer": 40},
                {"question": "If you borrow $1000 at 5% interest, what is total to repay after one year?", "explanation": "$1000 + $50 = $1050.", "answer": 1050}
            ],
            "interactive": [
                {"question": "Borrow $300 at 8% interest. Annual interest?", "answer": 24},
                {"question": "Owe $150 at 12% interest. Annual interest?", "answer": 18},
                {"question": "Borrow $600 at 4% interest. Total after one year?", "answer": 624}
            ]
        },
        13: {
            "title": "Credit vs. Debit",
            "symbols": "💳 Credit = borrow now, pay later | 🏦 Debit = use your own money",
            "table": "Credit cards can build credit history but may incur interest.\nDebit cards spend money you already have.",
            "demos": [
                {"question": "You buy a $50 item with a credit card. Do you pay immediately?", "explanation": "No, you'll pay later in the billing cycle.", "answer": "no"},
                {"question": "You use a debit card to buy $30 groceries. Where does money come from?", "explanation": "From your bank account (your own money).", "answer": "bank account"},
                {"question": "If you don't pay credit card bill on time, what happens?", "explanation": "You may be charged interest or late fees.", "answer": "interest/fees"}
            ],
            "interactive": [
                {"question": "Using a credit card means you are borrowing money. True or False?", "answer": "true"},
                {"question": "Debit cards spend money you have saved. True or False?", "answer": "true"},
                {"question": "Credit cards are free to use with no downside. True or False?", "answer": "false"}
            ]
        },
        14: {
            "title": "Cash Flow Statement",
            "symbols": "📊 Cash In - Cash Out = Net Cash Flow",
            "table": "Example:\nCash In: $1500\nCash Out: $1200\nNet Cash Flow: +$300",
            "demos": [
                {"question": "Cash In: $2000, Cash Out: $1800. Net Cash Flow?", "explanation": "$2000 - $1800 = +$200.", "answer": 200},
                {"question": "Cash In: $500, Cash Out: $700. Net Cash Flow?", "explanation": "$500 - $700 = -$200 (negative).", "answer": -200},
                {"question": "Cash In: $3000, Cash Out: $2500. Net Cash Flow?", "explanation": "$3000 - $2500 = +$500.", "answer": 500}
            ],
            "interactive": [
                {"question": "Cash In: $1200, Cash Out: $900. Net?", "answer": 300},
                {"question": "Cash In: $800, Cash Out: $950. Net?", "answer": -150},
                {"question": "Cash In: $2500, Cash Out: $2000. Net?", "answer": 500}
            ]
        },
        15: {
            "title": "Income Statement (Profit & Loss)",
            "symbols": "📈 Revenue - Expenses = Net Income",
            "table": "Revenue: $5000\nExpenses: $3000\nNet Income: $2000",
            "demos": [
                {"question": "Revenue $4000, Expenses $2500. Net Income?", "explanation": "$4000 - $2500 = $1500 profit.", "answer": 1500},
                {"question": "Revenue $1000, Expenses $1200. Net Income?", "explanation": "$1000 - $1200 = -$200 (loss).", "answer": -200},
                {"question": "Revenue $8000, Expenses $6000. Net Income?", "explanation": "$8000 - $6000 = $2000.", "answer": 2000}
            ],
            "interactive": [
                {"question": "Revenue $3000, Expenses $2800. Net Income?", "answer": 200},
                {"question": "Revenue $900, Expenses $1100. Net Income?", "answer": -200},
                {"question": "Revenue $5000, Expenses $4000. Net Income?", "answer": 1000}
            ]
        },
        16: {
            "title": "Simplified Balance Sheet",
            "symbols": "📊 Assets = Liabilities + Equity",
            "table": "Assets: Cash $500, Car $1000\nLiabilities: Loan $300\nEquity = Assets - Liabilities = $1200",
            "demos": [
                {"question": "Assets: $2000, Liabilities: $800. Equity?", "explanation": "$2000 - $800 = $1200.", "answer": 1200},
                {"question": "Assets: $1500, Liabilities: $500. Equity?", "explanation": "$1500 - $500 = $1000.", "answer": 1000},
                {"question": "Assets: $3000, Liabilities: $1200. Equity?", "explanation": "$3000 - $1200 = $1800.", "answer": 1800}
            ],
            "interactive": [
                {"question": "Assets $2500, Liabilities $900. Equity?", "answer": 1600},
                {"question": "Assets $1800, Liabilities $600. Equity?", "answer": 1200},
                {"question": "Assets $4000, Liabilities $1500. Equity?", "answer": 2500}
            ]
        },
        17: {
            "title": "Setting Financial Goals",
            "symbols": "🎯 Short-term (<1 year) | 🎯 Medium-term (1-5 years) | 🎯 Long-term (>5 years)",
            "table": "Example: Save $500 for a vacation (short-term), $3000 for a car (medium), $10000 for education (long).",
            "demos": [
                {"question": "Saving for a laptop in 6 months. Short, medium, or long term?", "explanation": "6 months is short-term.", "answer": "short"},
                {"question": "Saving for a house down payment in 3 years. Short, medium, or long term?", "explanation": "3 years is medium-term.", "answer": "medium"},
                {"question": "Saving for retirement in 20 years. Short, medium, or long term?", "explanation": "20 years is long-term.", "answer": "long"}
            ],
            "interactive": [
                {"question": "Saving for a new phone in 4 months?", "answer": "short"},
                {"question": "Saving for a car in 2 years?", "answer": "medium"},
                {"question": "Saving for a child's college in 15 years?", "answer": "long"}
            ]
        },
        18: {
            "title": "Spending Plans (Budgets)",
            "symbols": "📋 50/30/20 rule: 50% Needs, 30% Wants, 20% Savings",
            "table": "Income: $1000\nNeeds: $500\nWants: $300\nSavings: $200",
            "demos": [
                {"question": "You earn $600. According to 50/30/20, how much for needs?", "explanation": "50% of $600 = $300.", "answer": 300},
                {"question": "Income $800. How much for wants (30%)?", "explanation": "30% of $800 = $240.", "answer": 240},
                {"question": "Income $1200. How much for savings (20%)?", "explanation": "20% of $1200 = $240.", "answer": 240}
            ],
            "interactive": [
                {"question": "Income $400. Needs (50%)?", "answer": 200},
                {"question": "Income $750. Wants (30%)?", "answer": 225},
                {"question": "Income $900. Savings (20%)?", "answer": 180}
            ]
        },
        19: {
            "title": "Evaluating Purchases – Important vs. Less Important",
            "symbols": "✔️ Important: essentials | ❌ Less important: luxuries",
            "table": "Important: rent, groceries, medicine\nLess important: designer clothes, latest gadgets",
            "demos": [
                {"question": "Is a new TV an important purchase or less important?", "explanation": "A new TV is less important unless your current one is broken.", "answer": "less important"},
                {"question": "Is prescription medication important or less important?", "explanation": "Medication is important.", "answer": "important"},
                {"question": "Is dining out every day important or less important?", "explanation": "Dining out daily is less important; cooking at home is cheaper.", "answer": "less important"}
            ],
            "interactive": [
                {"question": "Textbooks for school – important or less important?", "answer": "important"},
                {"question": "A new gaming console – important or less important?", "answer": "less important"},
                {"question": "Heating bill in winter – important or less important?", "answer": "important"}
            ]
        },
        20: {
            "title": "Review – Putting It All Together",
            "symbols": "All key concepts: cash flow, budgeting, saving, investing, debt, goals",
            "table": "Remember: track your money, spend wisely, save for the future.",
            "demos": [
                {"question": "You earn $2000, spend $1500, save $300, and invest $200. What is your net cash flow?", "explanation": "Net cash flow = earnings - total spending = $2000 - ($1500+$300+$200) = $2000 - $2000 = $0.", "answer": 0},
                {"question": "If you have $500 in savings and add $100 each month, how much after 6 months?", "explanation": "$500 + ($100×6) = $1100.", "answer": 1100},
                {"question": "What is the 50/30/20 rule?", "explanation": "50% needs, 30% wants, 20% savings.", "answer": "50/30/20"}
            ],
            "interactive": [
                {"question": "You earn $1500, spend $1200 on needs, $200 on wants, and save $100. How much left?", "answer": 0},
                {"question": "You save $200 per month. How much in 1 year?", "answer": 2400},
                {"question": "What percentage of income should go to savings according to 50/30/20?", "answer": 20}
            ]
        }
    }

    # If language is English, return original
    if lang_code == "en" or lang_code == "English":
        return lessons_en.get(lesson_num, lessons_en[1])

    # Otherwise translate the lesson
    # Map language code to destination language for googletrans
    dest = "fr" if lang_code == "fr" else "es" if lang_code == "es" else "en"
    lesson_en = lessons_en.get(lesson_num, lessons_en[1])
    return translate_lesson_content(lesson_en, dest, lesson_num)

# ---------- Authentication ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "lang" not in st.session_state:
    st.session_state.lang = "English"

def set_language():
    pass

# Sidebar for language (visible before login)
with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=60)
    st.selectbox("🌐 Language", options=list(LANGUAGES.keys()), key="lang", on_change=set_language)

if not st.session_state.authenticated:
    lang = st.session_state.lang
    ui = LANGUAGES[lang]["ui"]
    set_light_purple_style()
    st.title(ui["login_title"])
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown(f"<h2 style='text-align: center;'>Let's Learn Accounting with Gesner</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #1a0b2e;'>{ui['login_sub']}</p>", unsafe_allow_html=True)
        password_input = st.text_input(ui["login_password"], type="password")
        if st.button(ui["login_btn"]):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(ui["login_error"])
    st.stop()

# ---------- Main app after login ----------
set_light_purple_style()
lang = st.session_state.lang
ui = LANGUAGES[lang]["ui"]
tts_voice = LANGUAGES[lang]["voice"]

st.markdown(f"""
<div class="main-header">
    <h1>{ui['title']}</h1>
    <p>{ui['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://github.com/Deslandes1/Let-s-Learn-Mathematics-with-Gesner/blob/main/Gesner%20Deslandes.png?raw=true", width=150)
    st.markdown("<h3 style='text-align: center; color: #1a0b2e;'>Gesner Deslandes</h3>", unsafe_allow_html=True)
    st.markdown("---")

    show_logo()
    st.markdown(f"## 🎯 {ui['lesson_prefix']}")
    lesson_number = st.selectbox("", list(range(1, 21)), index=0, label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"### 📚 {ui['sidebar_progress']}")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ {ui['lesson_prefix']} {lesson_number} {ui['sidebar_completed']}")
    st.markdown("---")
    st.markdown(f"**{ui['sidebar_founder']}**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown(f"### 💰 {ui['sidebar_price_label']}")
    st.markdown(ui['sidebar_price'])
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    st.markdown(ui['built_by'])  # Added built-by text
    st.markdown("---")
    if st.button(f"🚪 {ui['sidebar_logout']}", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ---------- Audio function ----------
def generate_audio(text, output_path):
    cmd = ["edge-tts", "--voice", tts_voice, "--text", text, "--write-media", output_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
    except Exception as e:
        st.error(f"Audio error: {e}")

def play_audio(text, key):
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            generate_audio(text, tmp.name)
            with open(tmp.name, "rb") as f:
                audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            os.unlink(tmp.name)

# ---------- Load lesson data (translated) ----------
# Get language code for translation: "en", "fr", "es"
lang_code = LANGUAGES[lang]["code"]  # e.g., "fr", "es", "en"
lesson_data = get_lesson_data(lesson_number, lang_code)
st.markdown(f"## 📖 {ui['lesson_prefix']} {lesson_number}: {lesson_data['title']}")

tab1, tab2, tab3, tab4 = st.tabs(ui['tabs'])

# Tab 1: Symbols & Tables
with tab1:
    st.subheader(ui['symbols_title'])
    st.markdown(lesson_data["symbols"])
    play_audio(lesson_data["symbols"], "symbols")
    st.subheader(ui['table_title'])
    st.markdown(lesson_data["table"])
    play_audio(lesson_data["table"], "table")

# Tab 2: Demonstrations
with tab2:
    st.subheader(ui['demo_title'])
    st.markdown(ui['demo_instruction'])
    for i, demo in enumerate(lesson_data["demos"], 1):
        st.markdown(f"**{ui['demo_button']} {i}:** {demo['question']}")
        if st.button(f"{ui['demo_button']} {i}", key=f"demo_{lesson_number}_{i}"):
            st.info(f"{ui['demo_explanation']} {demo['explanation']}")
            st.success(f"{ui['demo_solution']} {demo['question']} = {demo['answer']}")
            # Play audio of explanation + solution – now in the target language
            audio_text = f"Problem: {demo['question']}. {demo['explanation']} The answer is {demo['answer']}."
            play_audio(audio_text, f"demo_audio_{lesson_number}_{i}")
        st.markdown("---")

# Tab 3: Interactive Exercises
with tab3:
    st.subheader(ui['exercise_title'])
    st.markdown(ui['exercise_instruction'])
    if f"ex_answers_{lesson_number}" not in st.session_state:
        st.session_state[f"ex_answers_{lesson_number}"] = {}
    for i, ex in enumerate(lesson_data["interactive"], 1):
        st.markdown(f"**{ui['exercise_check']} {i}:** {ex['question']}")
        # For numeric answers, use number_input; for text, use text_input.
        # Detect if answer is numeric (int or float) else use text.
        if isinstance(ex["answer"], (int, float)):
            user_ans = st.number_input(f" ", key=f"ex_{lesson_number}_{i}", step=1, format="%d", label_visibility="collapsed")
        else:
            user_ans = st.text_input(f" ", key=f"ex_{lesson_number}_{i}", label_visibility="collapsed")
        if st.button(f"{ui['exercise_check']} {i}", key=f"check_{lesson_number}_{i}"):
            if str(user_ans).lower() == str(ex["answer"]).lower():
                st.success(f"{ui['exercise_correct']} {ex['question']} = {ex['answer']}")
                st.session_state[f"ex_answers_{lesson_number}"][i] = True
                # Play audio of correct message – translated via UI strings
                play_audio(f"{ui['exercise_correct']} {ex['question']} equals {ex['answer']}. Well done!", f"success_{lesson_number}_{i}")
            else:
                st.error(f"{ui['exercise_hint']} {ex['answer']}.")
        st.markdown("---")

# Tab 4: Quiz (20 questions, one from each lesson)
with tab4:
    st.subheader(ui['quiz_title'])
    st.markdown(ui['quiz_instruction'])
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    # Generate quiz questions – we need to fetch each lesson's interactive questions in the current language
    quiz_questions = []
    for l in range(1, 21):
        # Fetch lesson in current language
        lesson_l = get_lesson_data(l, lang_code)
        if lesson_l["interactive"]:
            q = random.choice(lesson_l["interactive"])
            quiz_questions.append({"lesson": l, "question": q["question"], "answer": q["answer"]})
        else:
            quiz_questions.append({"lesson": l, "question": "Sample", "answer": 0})
    for q in quiz_questions:
        st.markdown(f"**{ui['lesson_prefix']} {q['lesson']}:** {q['question']}")
        if isinstance(q["answer"], (int, float)):
            user_ans = st.number_input(f" ", key=f"quiz_{q['lesson']}", step=1, format="%d", label_visibility="collapsed")
        else:
            user_ans = st.text_input(f" ", key=f"quiz_{q['lesson']}", label_visibility="collapsed")
        if st.button(f"{ui['quiz_check']} {q['lesson']}", key=f"quiz_check_{q['lesson']}"):
            if str(user_ans).lower() == str(q["answer"]).lower():
                st.success(ui['quiz_correct'])
                st.session_state.quiz_answers[q['lesson']] = True
            else:
                st.error(f"{ui['quiz_incorrect']} {q['answer']}.")
        st.markdown("---")
    if st.button(ui['quiz_results']):
        correct = sum(1 for l in range(1,21) if st.session_state.quiz_answers.get(l, False))
        st.info(ui['quiz_results_text'].format(correct=correct))

if lesson_number == 20:
    st.markdown("---")
    st.markdown(f"## {ui['congrats']}")
    st.markdown(f"""
    ### 📞 {ui['contact']}
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Book 2 will cover more advanced topics like financial statements, tax, and business finance.
    """)

st.markdown("---")
st.caption(ui['footer_caption'])
