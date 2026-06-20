# Varahi Automotives – Website

A premium, responsive business website for Varahi Automotives built with Python (Flask) + HTML, CSS, and Vanilla JavaScript.

## New Premium Features

- **Clickable Brand Logos**: Brand logos (Hero, Honda, Bajaj, TVS) and pills on the homepage and about page are fully clickable.
- **Dedicated Brand Pages**: Navigates to `/brand/<name>` displaying company background details, logos, and a custom parts catalogue.
- **Dual Category & Brand Filtering**: The products catalog page supports cross-filtering (filter by categories like Lubricants/Spare Parts and brands like Hero/Castrol/Exide at the same time).
- **Vector category illustrations**: Product cards display sharp, high-end inline SVG visual headers customized for each product category (Lubricants, Batteries, Tyres, Spare Parts, Electrical, Accessories).
- **Animated FAQ Accordion**: Interactive accordion on the homepage with smooth slide-down and chevron rotation animations.
- **Modernized Visual Design**: Brand colors updated to a premium **electric racing red**, sleek **charcoal slate grey**, off-white pages, crisp silver borders, and cubic-bezier card hover lifts.
- **Polished Contact Form**: Clean glassmorphism inquiry container, formatted phone/address lists, and maps frame.

---

## Setup & Run Instructions

### 1. Install Python (if not installed)
Download from: https://python.org/downloads (Python 3.9+)

### 2. Install Flask
```bash
pip install flask
```

### 3. Run the Website
Navigate to the project directory:
```bash
cd varahi
python app.py
```
By default, the server will start on: **http://localhost:5000**

---

## Admin Panel
URL: **http://localhost:5000/admin**

Default credentials:
- **Username:** admin
- **Password:** varahi@2024

> Change these in `app.py` → `init_db()` function after first run.

---

## Project Structure
```
varahi/
├── app.py               ← Main Flask application (routes & database init)
├── requirements.txt     ← Dependencies
├── varahi.db            ← SQLite database (auto-created with 26 parts)
├── static/
│   ├── css/style.css    ← Premium colors, shadows, and animations
│   ├── js/main.js       ← Mobile navbar toggle script
│   └── images/          ← Brand logo image assets
└── templates/
    ├── base.html        ← Responsive navbar & footer layout
    ├── index.html       ← Homepage + brand grid + FAQ accordion
    ├── products.html    ← Products catalog + dual cross-filters + category SVGs
    ├── about.html       ← About page + clickable partner logos
    ├── contact.html     ← Polished inquiry form + Google Maps
    ├── brand_detail.html ← Brand detail layouts + brand parts grid
    └── admin/
        ├── login.html
        ├── dashboard.html
        ├── products.html
        ├── product_form.html
        └── inquiries.html
```

## Deployment
Recommended free options for hosting Python/Flask applications: **Render.com**, **PythonAnywhere** or **Railway**. 
- Link your GitHub repository (`https://github.com/vedhavihith/Varahi`).
- Set startup command: `python app.py` or specify WSGI path.
