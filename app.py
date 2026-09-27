import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
DATABASE = os.environ.get("DATABASE_PATH", "car_rental.db")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS vehicles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price_per_day REAL NOT NULL,
        location TEXT NOT NULL,
        available INTEGER NOT NULL DEFAULT 1
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        customer_name TEXT NOT NULL,
        email TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        payment_status TEXT NOT NULL DEFAULT 'Pending',
        tracking_status TEXT NOT NULL DEFAULT 'Booking Confirmed',
        created_at TEXT NOT NULL,
        FOREIGN KEY(vehicle_id) REFERENCES vehicles(id)
    )""")
    if conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO vehicles(name,category,price_per_day,location,available) VALUES(?,?,?,?,?)",
            [
                ("Toyota Camry", "Sedan", 45.0, "Chennai", 1),
                ("Hyundai Creta", "SUV", 55.0, "Chennai", 1),
                ("Maruti Swift", "Hatchback", 30.0, "Ponneri", 1),
                ("Kia Carens", "MPV", 60.0, "Chennai", 1),
            ],
        )
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    vehicles = conn.execute("SELECT * FROM vehicles WHERE available=1 ORDER BY id").fetchall()
    conn.close()
    return render_template("index.html", vehicles=vehicles)

@app.route("/book/<int:vehicle_id>", methods=["GET", "POST"])
def book(vehicle_id):
    conn = get_db()
    vehicle = conn.execute("SELECT * FROM vehicles WHERE id=?", (vehicle_id,)).fetchone()
    if not vehicle:
        conn.close()
        return "Vehicle not found", 404

    if request.method == "POST":
        customer_name = request.form["customer_name"].strip()
        email = request.form["email"].strip()
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        if not customer_name or not email or not start_date or not end_date:
            flash("All booking fields are required.", "error")
            return render_template("book.html", vehicle=vehicle)

        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            days = (end - start).days
            if days <= 0:
                raise ValueError
        except ValueError:
            flash("Please enter a valid date range.", "error")
            return render_template("book.html", vehicle=vehicle)

        cur = conn.execute(
            """INSERT INTO bookings(vehicle_id,customer_name,email,start_date,end_date,
               payment_status,tracking_status,created_at)
               VALUES(?,?,?,?,?,?,?,?)""",
            (vehicle_id, customer_name, email, start_date, end_date,
             "Paid (Demo)", "Booking Confirmed", datetime.utcnow().isoformat())
        )
        booking_id = cur.lastrowid
        conn.commit()
        conn.close()
        return redirect(url_for("confirmation", booking_id=booking_id))

    conn.close()
    return render_template("book.html", vehicle=vehicle)

@app.route("/confirmation/<int:booking_id>")
def confirmation(booking_id):
    conn = get_db()
    booking = conn.execute("""SELECT b.*, v.name, v.category, v.price_per_day
                              FROM bookings b JOIN vehicles v ON b.vehicle_id=v.id
                              WHERE b.id=?""", (booking_id,)).fetchone()
    conn.close()
    if not booking:
        return "Booking not found", 404
    return render_template("confirmation.html", booking=booking)

@app.route("/tracking/<int:booking_id>")
def tracking(booking_id):
    conn = get_db()
    booking = conn.execute("""SELECT b.*, v.name
                              FROM bookings b JOIN vehicles v ON b.vehicle_id=v.id
                              WHERE b.id=?""", (booking_id,)).fetchone()
    conn.close()
    if not booking:
        return "Booking not found", 404
    return render_template("tracking.html", booking=booking)

@app.route("/api/vehicles")
def api_vehicles():
    conn = get_db()
    rows = conn.execute("SELECT * FROM vehicles WHERE available=1").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "car-rental-app"})

@app.errorhandler(500)
def server_error(error):
    app.logger.exception("Unhandled server error")
    return render_template("error.html"), 500

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
