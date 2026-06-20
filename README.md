# Varahi Automotives – Website

A full-featured business website for Varahi Automotives built with HTML/CSS + Python Flask.

## Features
- Homepage with hero, category grid, featured products, brands strip
- Products page with search & category filter
- About Us page (mission, vision, services, brands)
- Contact page with inquiry form + Google Maps embed
- WhatsApp floating button on all pages
- **Admin Panel** to manage products & view customer inquiries

---

## Setup Instructions

### 1. Install Python (if not installed)
Download from: https://python.org/downloads (Python 3.9+)

### 2. Install Flask
```
pip install flask
```

### 3. Run the Website
```
cd varahi
python app.py
```

### 4. Open in Browser
Go to: **http://localhost:5000**

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
├── app.py               ← Main Flask application
├── requirements.txt     ← Dependencies
├── varahi.db            ← SQLite database (auto-created on first run)
├── static/
│   ├── css/style.css    ← All styles
│   └── js/main.js       ← JavaScript
└── templates/
    ├── base.html         ← Navbar & footer
    ├── index.html        ← Homepage
    ├── products.html     ← Products catalog
    ├── about.html        ← About page
    ├── contact.html      ← Contact + inquiry form
    └── admin/
        ├── login.html
        ├── dashboard.html
        ├── products.html
        ├── product_form.html
        └── inquiries.html
```

## To Deploy Online (Free)
Options: **PythonAnywhere** (free tier), **Railway**, or **Render.com**
- Upload all files
- Set start command: `python app.py`
- Site will be live at a public URL
