from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
import uuid
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'varahi_automotives_secret_2024'

DB_PATH = 'varahi.db'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB Max upload limit

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BRANDS_INFO = {
    'hero': {
        'name': 'Hero MotoCorp',
        'type': 'Vehicle Manufacturer',
        'logo': 'hero-logo.png',
        'desc': "India's largest manufacturer of motorcycles and scooters, world-renowned for reliable and fuel-efficient rides.",
        'details': "Hero MotoCorp is the world's largest manufacturer of two-wheelers. Known for legendary, fuel-efficient commuter models like the Splendor, Passion, HF Deluxe, Glamour, and Pleasure scooters, Hero parts are designed for maximum longevity and everyday utility. We stock genuine Hero parts, wires, and cables to keep your commuter running smoothly.",
        'is_vehicle': True
    },
    'honda': {
        'name': 'Honda 2-Wheelers',
        'type': 'Vehicle Manufacturer',
        'logo': 'honda-logo.png',
        'desc': "A world leader in two-wheeler technology, famous for ultra-reliable engines and India's favorite Activa scooter.",
        'details': "Honda Motorcycle & Scooter India (HMSI) is synonymous with smooth performance and reliability. From India's undisputed scooter king, the Honda Activa, to premium commuter bikes like the Honda Shine and Unicorn, Honda vehicles demand precision engineering. We offer authentic Honda spares, brake cables, and filters to maintain that smooth, factory-new feel.",
        'is_vehicle': True
    },
    'bajaj': {
        'name': 'Bajaj Auto',
        'type': 'Vehicle Manufacturer',
        'logo': 'bajaj-logo.png',
        'desc': "Pioneers of performance and sports commuting in India, famous for the Pulsar, Platina, and Discover series.",
        'details': "Bajaj Auto is famous for introducing performance biking to the Indian masses through the iconic Pulsar range. Bajaj is also highly trusted for its mileage-oriented commuter bikes like the Platina and CT100. We stock premium genuine parts, cables, and clutch plates for Bajaj motorcycles to preserve their signature power and performance.",
        'is_vehicle': True
    },
    'tvs': {
        'name': 'TVS Motor Company',
        'type': 'Vehicle Manufacturer',
        'logo': 'tvs-logo.png',
        'desc': "A leading manufacturer known for racing pedigree, high-tech features, and the Apache and Jupiter brands.",
        'details': "TVS Motor Company is celebrated for its racing heritage and modern tech features. With bestselling models like the TVS Apache RTR series, TVS Jupiter, and TVS Raider, TVS products deliver exceptional performance. We supply genuine TVS spare parts, filters, and brake shoes built to exact factory specifications.",
        'is_vehicle': True
    },
    'castrol': {
        'name': 'Castrol',
        'type': 'Lubricants & Engine Oils',
        'logo': None,
        'desc': 'World-class automotive lubricants designed to protect and enhance engine performance under extreme conditions.',
        'details': 'Castrol is a global leader in lubricant technology. Their range of motorcycle oils, including Castrol Activ with Actibond molecules and Castrol Power 1, provides continuous protection for 4-stroke engines, preventing wear during start-up and high-speed cruising. Perfect for all leading Indian bikes and scooters.',
        'is_vehicle': False
    },
    'motul': {
        'name': 'Motul',
        'type': 'Lubricants & Engine Oils',
        'logo': None,
        'desc': 'Premium high-performance engine lubricants favored by racers and riding enthusiasts worldwide.',
        'details': 'Motul is a French company specializing in high-performance lubricants. Popular among premium motorcycle owners, Motul 3000 (mineral) and Motul 7100 (100% synthetic) oils offer outstanding shear stability, engine protection, and smooth gear shifts. Ideal for riders who demand top performance.',
        'is_vehicle': False
    },
    'gulf': {
        'name': 'Gulf',
        'type': 'Lubricants & Engine Oils',
        'logo': None,
        'desc': 'Quality lubricants engineered to deliver high mileage and superior wear protection.',
        'details': 'Gulf Oil offers advanced engine and gear oils tailored for heavy-traffic commuter riding. Their signature formulation ensures lower engine operating temperatures and protects crucial engine components over long intervals.',
        'is_vehicle': False
    },
    'exide': {
        'name': 'Exide Batteries',
        'type': 'Power & Batteries',
        'logo': None,
        'desc': "India's most trusted battery manufacturer, offering maintenance-free, long-lasting power.",
        'details': "Exide is the leading manufacturer of lead-acid storage batteries in India. The Exide Xplore range features maintenance-free, VRLA technology designed to handle tough road conditions, hot climates, and frequent start-stops, ensuring a quick start every time for your motorcycle or scooter.",
        'is_vehicle': False
    },
    'amaron': {
        'name': 'Amaron Batteries',
        'type': 'Power & Batteries',
        'logo': None,
        'desc': 'Famous for long-lasting performance and zero-maintenance batteries with silver-alloy technology.',
        'details': 'Amaron batteries, produced by Amara Raja, are known for their trademark green color and "lasts long, really long" promise. Utilizing proprietary Silven X alloy technology, Amaron Pro Rider batteries offer high cranking power and high vibration resistance, making them a premium choice for two-wheelers.',
        'is_vehicle': False
    },
    'mrf': {
        'name': 'MRF Tyres',
        'type': 'Tyres & Rubber',
        'logo': None,
        'desc': "India's largest tyre manufacturer, providing exceptional grip, durability, and road safety.",
        'details': 'MRF (Madras Rubber Factory) is India\'s top tyre maker. Famous for tyres like the Nylogrip Zapper, Mogrip, and Revz series, MRF tyres are engineered to deliver superior wet and dry grip, outstanding mileage, and stability on all Indian road surfaces.',
        'is_vehicle': False
    },
    'ceat': {
        'name': 'CEAT Tyres',
        'type': 'Tyres & Rubber',
        'logo': None,
        'desc': 'Pioneers of safe, high-grip tubeless tyres designed for city riding and highway commuting.',
        'details': 'CEAT is a leading tyre manufacturer focusing on safety and control. Their Zoom and Secura series of two-wheeler tyres offer excellent cornering stability and short braking distances, making them ideal for both daily city commuting and highway riding.',
        'is_vehicle': False
    },
    'ngk': {
        'name': 'NGK Spark Plugs',
        'type': 'Engine Ignition Parts',
        'logo': None,
        'desc': 'Global leaders in spark plug technology, providing optimum combustion and quick starts.',
        'details': "NGK is the world's number one spark plug brand. Trusted by OEMs globally, NGK spark plugs feature high-grade materials that resist thermal shock and electrical wear, ensuring smooth engine idling, quick cold starts, and maximum fuel efficiency.",
        'is_vehicle': False
    }
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT,
        description TEXT,
        price TEXT,
        available INTEGER DEFAULT 1,
        image_url TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Migration to check if image_url column exists and add it if not
    c.execute("PRAGMA table_info(products)")
    columns = [row[1] for row in c.fetchall()]
    if 'image_url' not in columns:
        c.execute("ALTER TABLE products ADD COLUMN image_url TEXT")
    
    c.execute('''CREATE TABLE IF NOT EXISTS inquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        vehicle TEXT,
        message TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        is_read INTEGER DEFAULT 0
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )''')
    
    # Default admin
    c.execute("SELECT * FROM admin WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO admin (username, password) VALUES ('admin', 'varahi@2024')")
    
    # Sample products
    c.execute("SELECT COUNT(*) FROM products")
    count = c.fetchone()[0]
    if count == 0 or count == 18 or count == 26:
        c.execute("DELETE FROM products")
        sample_products = [
            # Lubricants
            ('Castrol Activ 4T Engine Oil 1L', 'Lubricants', 'Castrol', 'High performance 4T engine oil for bikes with Actibond molecules.', '₹350', 1, 'castrol_oil.png'),
            ('Motul 3000 4T 20W-40 Engine Oil', 'Lubricants', 'Motul', 'Mineral engine oil for 4-stroke motorcycles, excellent wet-clutch performance.', '₹420', 1, None),
            ('Castrol Power 1 Scooter 10W-30 800ml', 'Lubricants', 'Castrol', 'Specially formulated synthetic technology oil for scooters.', '₹380', 1, None),
            ('Motul 7100 4T 10W-50 Synthetic Oil 1L', 'Lubricants', 'Motul', '100% synthetic double ester engine oil for high performance bikes.', '₹850', 1, None),
            ('Gulf Pride 4T 20W-40 1L', 'Lubricants', 'Gulf', 'High quality mineral engine oil for everyday commuter bikes.', '₹320', 1, None),
            ('Gulf Gear Oil 80W-90 500ml', 'Lubricants', 'Gulf', 'Premium gear oil for smooth gear shifting and transmission protection.', '₹180', 1, None),
            
            # Wires and Cables
            ('Front Brake Cable / Wire (Hero Splendor)', 'Spare Parts', 'Genuine', 'High-tensile front brake wire for Hero Splendor, Passion, and HF Deluxe.', '₹90', 1, None),
            ('Rear Brake Cable / Wire (Honda Activa)', 'Spare Parts', 'Genuine', 'OEM quality rear brake wire/cable for Honda Activa 3G/4G/5G/6G.', '₹120', 1, None),
            ('Front Brake Cable / Wire (TVS Jupiter)', 'Spare Parts', 'Genuine', 'Genuine front brake cable for TVS Jupiter and Wego scooters.', '₹110', 1, None),
            ('Accelerator Cable / Throttle Wire (Bajaj Pulsar)', 'Spare Parts', 'Genuine', 'Flexible throttle/accelerator cable set for Bajaj Pulsar 150/180.', '₹130', 1, None),
            ('Clutch Cable / Wire (Hero Passion Pro)', 'Spare Parts', 'Genuine', 'Heavy duty replacement clutch cable for Hero Passion Pro.', '₹110', 1, None),
            ('Clutch Cable / Wire (Bajaj Pulsar 150)', 'Spare Parts', 'Genuine', 'High durability clutch wire/cable for Bajaj Pulsar 150.', '₹140', 1, 'pulsar_cable.png'),
            
            # Spare Parts
            ('NGK Spark Plug CR7HSA', 'Spare Parts', 'NGK', 'Standard spark plug for Hero, Honda, and TVS 2-wheelers.', '₹120', 1, None),
            ('Brake Shoe Set (Front/Rear)', 'Spare Parts', 'Genuine', 'OEM quality brake shoes for Hero Splendor/Passion and Honda Activa.', '₹250', 1, None),
            ('Engine Air Filter Element', 'Spare Parts', 'Genuine', 'High filtration air filter compatible with Hero Splendor and Passion.', '₹180', 1, None),
            ('Chain Sprocket Kit', 'Spare Parts', 'Genuine', 'Complete heavy duty chain & sprocket kit for 100cc-125cc motorcycles.', '₹850', 1, None),
            ('Clutch Plate Set', 'Spare Parts', 'Genuine', 'Heavy duty clutch plates for smooth gear shifts and power transfer.', '₹650', 1, None),
            
            # Electrical
            ('Osram Headlight Bulb 12V 35/35W', 'Electrical', 'Osram', 'Standard high-brightness headlight bulb for all two-wheelers.', '₹80', 1, None),
            ('Indicator Bulb Set (4 Pcs)', 'Electrical', 'Genuine', 'Front & rear orange indicator bulbs for Hero and Honda bikes.', '₹60', 1, None),
            
            # Batteries
            ('Exide Xplore 12V 5Ah Battery', 'Batteries', 'Exide', 'Maintenance-free VRLA battery for self-start bikes and scooters.', '₹1,850', 1, 'exide_battery.png'),
            ('Amaron Pro Rider 12V 5Ah', 'Batteries', 'Amaron', 'High cranking power maintenance-free battery for two-wheelers.', '₹1,950', 1, None),
            
            # Tyres
            ('MRF Nylogrip Zapper 90/90-17', 'Tyres', 'MRF', 'Tubeless rear motorcycle tyre, offering excellent wet and dry grip.', '₹1,400', 1, 'mrf_tyre.png'),
            ('CEAT Zoom 90/90-10', 'Tyres', 'CEAT', 'High grip tubeless scooter tyre compatible with Honda Activa and TVS Jupiter.', '₹1,200', 1, None),
            
            # Accessories
            ('Handlebar Grip Set', 'Accessories', 'Generic', 'Comfortable anti-slip rubber handlebar grips for all bikes.', '₹120', 1, None),
            ('Side Mirror Pair (Universal)', 'Accessories', 'Generic', 'Universal clear side mirrors with adjustable mounting brackets.', '₹220', 1, None),
            ('Waterproof Bike Cover', 'Accessories', 'Generic', 'Full size waterproof and dustproof protective bike cover.', '₹350', 1, None),
        ]
        c.executemany(
            "INSERT INTO products (name, category, brand, description, price, available, image_url) VALUES (?,?,?,?,?,?,?)",
            sample_products
        )
    
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ─── PUBLIC ROUTES ───────────────────────────────────────────

@app.route('/')
def index():
    conn = get_db()
    categories = conn.execute(
        "SELECT category, COUNT(*) as count FROM products WHERE available=1 GROUP BY category"
    ).fetchall()
    featured = conn.execute(
        "SELECT * FROM products WHERE available=1 LIMIT 6"
    ).fetchall()
    conn.close()
    return render_template('index.html', categories=categories, featured=featured)

@app.route('/products')
def products():
    cat = request.args.get('category', '')
    brand = request.args.get('brand', '')
    search = request.args.get('search', '')
    conn = get_db()
    
    query = "SELECT * FROM products WHERE available=1"
    params = []
    if cat:
        query += " AND category=?"
        params.append(cat)
    if brand:
        query += " AND brand=?"
        params.append(brand)
    if search:
        query += " AND (name LIKE ? OR brand LIKE ? OR description LIKE ?)"
        params += [f'%{search}%', f'%{search}%', f'%{search}%']
    
    items = conn.execute(query, params).fetchall()
    cats = conn.execute("SELECT DISTINCT category FROM products WHERE available=1").fetchall()
    brands = conn.execute("SELECT DISTINCT brand FROM products WHERE available=1 ORDER BY brand").fetchall()
    conn.close()
    return render_template('products.html', products=items, categories=cats, brands=brands,
                           selected_cat=cat, selected_brand=brand, search=search)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/brand/<brand_name>')
def brand_detail(brand_name):
    key = brand_name.lower().strip()
    if key not in BRANDS_INFO:
        flash(f"Brand '{brand_name}' not found.", "error")
        return redirect(url_for('index'))
    
    brand_data = BRANDS_INFO[key]
    cat = request.args.get('category', '')
    search = request.args.get('search', '')
    
    conn = get_db()
    canonical_brand = brand_data['name'].split()[0]
    
    if brand_data['is_vehicle']:
        query = "SELECT * FROM products WHERE available=1 AND (brand = ? OR name LIKE ? OR description LIKE ?)"
        params = [canonical_brand, f'%{canonical_brand}%', f'%{canonical_brand}%']
    else:
        query = "SELECT * FROM products WHERE available=1 AND brand = ?"
        params = [canonical_brand]
        
    if cat:
        query += " AND category = ?"
        params.append(cat)
        
    if search:
        query += " AND (name LIKE ? OR description LIKE ?)"
        params += [f'%{search}%', f'%{search}%']
        
    products = conn.execute(query, params).fetchall()
    
    if brand_data['is_vehicle']:
        cat_query = "SELECT DISTINCT category FROM products WHERE available=1 AND (brand = ? OR name LIKE ? OR description LIKE ?)"
        cat_params = [canonical_brand, f'%{canonical_brand}%', f'%{canonical_brand}%']
    else:
        cat_query = "SELECT DISTINCT category FROM products WHERE available=1 AND brand = ?"
        cat_params = [canonical_brand]
        
    cats_raw = conn.execute(cat_query, cat_params).fetchall()
    categories = [row['category'] for row in cats_raw]
    
    conn.close()
    
    return render_template('brand_detail.html', 
                           brand=brand_data, 
                           products=products, 
                           categories=categories, 
                           selected_cat=cat, 
                           search=search,
                           brand_key=brand_name)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        vehicle = request.form.get('vehicle', '').strip()
        message = request.form.get('message', '').strip()
        
        if name and phone:
            conn = get_db()
            conn.execute(
                "INSERT INTO inquiries (name, phone, vehicle, message) VALUES (?,?,?,?)",
                (name, phone, vehicle, message)
            )
            conn.commit()
            conn.close()
            flash('Thank you! We will contact you shortly.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in your name and phone number.', 'error')
    
    return render_template('contact.html')

# ─── ADMIN ROUTES ────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db()
        admin = conn.execute(
            "SELECT * FROM admin WHERE username=? AND password=?", (username, password)
        ).fetchone()
        conn.close()
        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    conn = get_db()
    product_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    inquiry_count = conn.execute("SELECT COUNT(*) FROM inquiries").fetchone()[0]
    unread = conn.execute("SELECT COUNT(*) FROM inquiries WHERE is_read=0").fetchone()[0]
    recent = conn.execute("SELECT * FROM inquiries ORDER BY created_at DESC LIMIT 5").fetchall()
    conn.close()
    return render_template('admin/dashboard.html', product_count=product_count,
                           inquiry_count=inquiry_count, unread=unread, recent_inquiries=recent)

@app.route('/admin/products')
@login_required
def admin_products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products ORDER BY category, name").fetchall()
    conn.close()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if request.method == 'POST':
        image_file = request.files.get('image')
        image_url = None
        if image_file and image_file.filename != '':
            ext = os.path.splitext(image_file.filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                filename = f"{uuid.uuid4()}{ext}"
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = filename
            else:
                flash('Invalid image format. Allowed: jpg, jpeg, png, gif, webp', 'error')
        
        conn = get_db()
        conn.execute(
            "INSERT INTO products (name, category, brand, description, price, available, image_url) VALUES (?,?,?,?,?,?,?)",
            (request.form['name'], request.form['category'], request.form['brand'],
             request.form['description'], request.form['price'], 1 if request.form.get('available') else 0, image_url)
        )
        conn.commit()
        conn.close()
        flash('Product added!', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin/product_form.html', product=None)

@app.route('/admin/products/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(pid):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    if request.method == 'POST':
        image_file = request.files.get('image')
        image_url = product['image_url']
        
        if image_file and image_file.filename != '':
            ext = os.path.splitext(image_file.filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                # Delete old image if it exists
                if image_url:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], image_url)
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except Exception as e:
                            print(f"Error removing old image: {e}")
                
                filename = f"{uuid.uuid4()}{ext}"
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = filename
            else:
                flash('Invalid image format. Allowed: jpg, jpeg, png, gif, webp', 'error')
        
        if request.form.get('remove_image'):
            if image_url:
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], image_url)
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except Exception as e:
                        print(f"Error removing image: {e}")
            image_url = None
            
        conn.execute(
            "UPDATE products SET name=?, category=?, brand=?, description=?, price=?, available=?, image_url=? WHERE id=?",
            (request.form['name'], request.form['category'], request.form['brand'],
             request.form['description'], request.form['price'],
             1 if request.form.get('available') else 0, image_url, pid)
        )
        conn.commit()
        conn.close()
        flash('Product updated!', 'success')
        return redirect(url_for('admin_products'))
    conn.close()
    return render_template('admin/product_form.html', product=product)

@app.route('/admin/products/delete/<int:pid>')
@login_required
def admin_delete_product(pid):
    conn = get_db()
    product = conn.execute("SELECT image_url FROM products WHERE id=?", (pid,)).fetchone()
    if product and product['image_url']:
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], product['image_url'])
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception as e:
                print(f"Error removing deleted product image: {e}")
    conn.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    flash('Product deleted.', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/inquiries')
@login_required
def admin_inquiries():
    conn = get_db()
    inquiries = conn.execute("SELECT * FROM inquiries ORDER BY created_at DESC").fetchall()
    conn.execute("UPDATE inquiries SET is_read=1")
    conn.commit()
    conn.close()
    return render_template('admin/inquiries.html', inquiries=inquiries)

# Initialize the database on startup (runs locally and under Gunicorn/WSGI production)
init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
