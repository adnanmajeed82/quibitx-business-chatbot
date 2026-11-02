
from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# ==========================================
# QUIBITX BUSINESS INFORMATION
# ==========================================

BUSINESS = {
    "name": "QuibitX",

    "tagline": "Build • Automate • Scale",

    "services": [
        "AI Chatbots",
        "Web Application Development",
        "Business Automation",
        "Python Development",
        "Django Development",
        "FastAPI Development",
        "REST API Development",
        "API Integration",
    ],

    "hours": "Monday to Saturday, 9 AM to 6 PM",

    "location": "Lahore, Pakistan",

    "whatsapp": "923209422680",

    "website": "https://adnanmajeed82.github.io",
}


# ==========================================
# CHATBOT FREQUENTLY ASKED QUESTIONS
# ==========================================

FAQS = [

    # GREETINGS
    {
        "keywords": [
            "hello", "hi", "hey", "salam",
            "assalam", "good morning", "good evening"
        ],
        "answer": (
            "Hello! Welcome to QuibitX. "
            "We help businesses build, automate, and scale "
            "with practical software solutions. "
            "How can we help you today?"
        ),
    },

    # SERVICES
    {
        "keywords": [
            "service", "services", "offer",
            "provide", "what do you do"
        ],
        "answer": (
            "QuibitX offers the following services:\n\n"
            "1. AI Chatbots\n"
            "2. Web Application Development\n"
            "3. Business Process Automation\n"
            "4. Python Development\n"
            "5. Django and FastAPI Development\n"
            "6. REST API Development and Integration\n\n"
            "Which service are you interested in?"
        ),
    },

    # PRICING
    {
        "keywords": [
            "price", "pricing", "cost", "charges",
            "rate", "budget", "quotation"
        ],
        "answer": (
            "Our pricing depends on your project requirements, "
            "features, and complexity.\n\n"
            "Please tell us about your project. "
            "Our team will discuss a suitable quotation "
            "with you."
        ),
    },

    # WORKING HOURS
    {
        "keywords": [
            "hours", "timing", "open",
            "working", "schedule"
        ],
        "answer": (
            f"Our working hours are {BUSINESS['hours']}."
            "\n\nYou can also send us a WhatsApp message."
        ),
    },

    # LOCATION
    {
        "keywords": [
            "location", "address", "where",
            "located", "office"
        ],
        "answer": (
            f"QuibitX is based in {BUSINESS['location']}."
            "\n\nContact us to discuss your software project."
        ),
    },

    # CONTACT
    {
        "keywords": [
            "contact", "phone", "whatsapp",
            "call", "number", "reach"
        ],
        "answer": (
            "You can contact QuibitX through WhatsApp:\n\n"
            f"https://wa.me/{BUSINESS['whatsapp']}\n\n"
            "We would be happy to discuss your project!"
        ),
    },

    # WEBSITE
    {
        "keywords": [
            "website", "web", "link",
            "portfolio", "online"
        ],
        "answer": (
            "Visit the QuibitX website and portfolio:\n\n"
            f"{BUSINESS['website']}\n\n"
            "Contact us for your custom software solution."
        ),
    },

    # AI CHATBOT
    {
        "keywords": [
            "chatbot", "chatbots", "bot",
            "bots", "ai chatbot", "customer support"
        ],
        "answer": (
            "Yes! QuibitX develops AI chatbots for businesses.\n\n"
            "Our chatbot solutions can help with:\n"
            "- Customer enquiries\n"
            "- Automated responses\n"
            "- Frequently asked questions\n"
            "- Customer support\n"
            "- Business communication\n\n"
            "Would you like a chatbot for your business?"
        ),
    },

    # WEB DEVELOPMENT
    {
        "keywords": [
            "website development", "web development",
            "websites", "web application",
            "django", "frontend", "backend"
        ],
        "answer": (
            "Yes! QuibitX develops custom websites "
            "and web applications.\n\n"
            "Our technologies include:\n"
            "- Python\n"
            "- Django\n"
            "- FastAPI\n"
            "- HTML, CSS and JavaScript\n"
            "- REST APIs\n\n"
            "Tell us about your website requirements."
        ),
    },

    # BUSINESS AUTOMATION
    {
        "keywords": [
            "automate", "automation", "automating",
            "business automation", "workflow",
            "repetitive", "automatic"
        ],
        "answer": (
            "QuibitX helps businesses automate repetitive tasks "
            "and improve their daily operations.\n\n"
            "Examples include:\n"
            "- Automated customer replies\n"
            "- Data processing\n"
            "- Business workflow automation\n"
            "- Report generation\n"
            "- API integrations\n\n"
            "Tell us which business process you want to automate."
        ),
    },

    # PYTHON DEVELOPMENT
    {
        "keywords": [
            "python", "python development",
            "software development", "programming"
        ],
        "answer": (
            "QuibitX provides Python software development "
            "services, including automation, backend systems, "
            "web applications, and API development.\n\n"
            "Tell us about your Python project."
        ),
    },

    # API DEVELOPMENT
    {
        "keywords": [
            "api", "apis", "rest api",
            "integration", "fastapi"
        ],
        "answer": (
            "QuibitX develops REST APIs and backend services "
            "using Python, Django REST Framework, and FastAPI.\n\n"
            "We can help with API development, integration, "
            "and backend application development."
        ),
    },

    # PROJECT DISCUSSION
    {
        "keywords": [
            "project", "idea", "requirement",
            "development", "need software"
        ],
        "answer": (
            "We would love to discuss your project!\n\n"
            "Please share:\n"
            "1. What type of software do you need?\n"
            "2. What features do you require?\n"
            "3. What is your expected timeline?\n\n"
            "Our team will discuss the next steps with you."
        ),
    },

    # THANK YOU
    {
        "keywords": [
            "thanks", "thank", "thankyou",
            "great", "excellent"
        ],
        "answer": (
            "You're welcome! Thank you for considering QuibitX.\n\n"
            "We look forward to working with you."
        ),
    },
]


# ==========================================
# TEXT NORMALIZATION
# ==========================================

def normalize(text):
    """
    Convert text to lowercase words.
    Remove unnecessary punctuation.
    """

    return re.findall(r"[a-z0-9]+", text.lower())


# ==========================================
# CHATBOT RESPONSE ENGINE
# ==========================================

def get_response(message):

    words = set(normalize(message))

    if not words:
        return "Please type a question so I can help you."

    best_match = None
    best_score = 0

    for faq in FAQS:

        keywords = faq["keywords"]

        score = 0

        for keyword in keywords:

            keyword_words = set(normalize(keyword))

            if keyword_words and keyword_words.issubset(words):
                score += len(keyword_words)

        if score > best_score:

            best_score = score
            best_match = faq

    if best_match:
        return best_match["answer"]

    return (
        "Thank you for contacting QuibitX!\n\n"
        "I can help you with:\n"
        "- AI Chatbots\n"
        "- Web Development\n"
        "- Business Automation\n"
        "- Python Development\n"
        "- API Development\n\n"
        "Please tell me more about your software requirements."
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        business=BUSINESS
    )


# ==========================================
# CHAT API
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "")

    if not isinstance(message, str):

        return jsonify({
            "error": "Invalid message."
        }), 400

    message = message.strip()

    if not message:

        return jsonify({
            "error": "Please enter a message."
        }), 400

    if len(message) > 1000:

        return jsonify({
            "error": "Message is too long."
        }), 400

    reply = get_response(message)

    return jsonify({
        "reply": reply
    })


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "business": BUSINESS["name"],
        "message": "QuibitX chatbot is running successfully."
    })


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
