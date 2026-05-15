from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import random
import datetime
import hashlib

app = Flask(__name__)
app.secret_key = "microearnhub_secret_2024"

# ──────────────────────────────────────────────────────────────────────────────
#  IN-MEMORY DATA STORE  (no database needed — resets when server restarts)
# ──────────────────────────────────────────────────────────────────────────────

USERS = {}          # email → user dict
GIGS  = []          # list of gig dicts posted by students
BIDS  = []          # list of bid/application dicts

SKILLS_LIST = [
    "Web Development", "App Development", "Python / ML",
    "Graphic Design", "UI/UX Design", "Video Editing",
    "Content Writing", "Data Analysis", "Cybersecurity",
    "Database Management", "Digital Marketing", "3D Modeling",
    "Game Development", "Cloud Computing", "Tutoring / Teaching"
]

# ── Seed data so the app feels populated on first load ──
def seed_data():
    # Create some sample users
    sample_students = [
        {"name": "Aarav Sharma",   "email": "aarav@muj.edu",   "role": "student",
         "skill": "Web Development",  "experience": 2, "price": 1500, "bio": "MERN stack dev, 2 years exp.", "rating": 4.8, "jobs_done": 12},
        {"name": "Priya Mehta",    "email": "priya@muj.edu",   "role": "student",
         "skill": "Graphic Design",   "experience": 1, "price": 800,  "bio": "Figma & Adobe Suite expert.",   "rating": 4.6, "jobs_done": 8},
        {"name": "Rohan Kapoor",   "email": "rohan@muj.edu",   "role": "student",
         "skill": "Python / ML",      "experience": 3, "price": 2000, "bio": "ML models & data pipelines.",   "rating": 4.9, "jobs_done": 20},
        {"name": "Sneha Tiwari",   "email": "sneha@muj.edu",   "role": "student",
         "skill": "Content Writing",  "experience": 1, "price": 600,  "bio": "SEO blogs & academic writing.", "rating": 4.5, "jobs_done": 15},
        {"name": "Mehul Jain",     "email": "mehul@muj.edu",   "role": "student",
         "skill": "Video Editing",    "experience": 2, "price": 1200, "bio": "Premiere Pro & After Effects.",  "rating": 4.7, "jobs_done": 10},
        {"name": "Ananya Rao",     "email": "ananya@muj.edu",  "role": "student",
         "skill": "UI/UX Design",     "experience": 3, "price": 2500, "bio": "Product design & prototyping.", "rating": 4.9, "jobs_done": 18},
        {"name": "Kabir Das",      "email": "kabir@muj.edu",   "role": "student",
         "skill": "App Development",  "experience": 2, "price": 1800, "bio": "Flutter & React Native dev.",    "rating": 4.6, "jobs_done": 9},
        {"name": "Nisha Patel",    "email": "nisha@muj.edu",   "role": "student",
         "skill": "Data Analysis",    "experience": 1, "price": 1000, "bio": "Excel, Power BI & SQL.",         "rating": 4.4, "jobs_done": 6},
        {"name": "Varun Lal",      "email": "varun@muj.edu",   "role": "student",
         "skill": "Cybersecurity",    "experience": 2, "price": 2200, "bio": "Ethical hacking & pen testing.", "rating": 4.8, "jobs_done": 7},
        {"name": "Tanya Gupta",    "email": "tanya@muj.edu",   "role": "student",
         "skill": "Digital Marketing","experience": 1, "price": 900,  "bio": "Social media & Google Ads.",     "rating": 4.3, "jobs_done": 11},
    ]
    for s in sample_students:
        s["password"] = hashlib.md5(b"password123").hexdigest()
        s["joined"]   = "Jan 2024"
        s["availability"] = random.randint(10, 30)
        USERS[s["email"]] = s

    sample_hirers = [
        {"name": "TechStart Club",  "email": "techstart@muj.edu", "role": "hirer",
         "org": "Entrepreneurship Cell", "bio": "Building campus tech products."},
        {"name": "Naveen Kumar",    "email": "naveen@gmail.com",   "role": "hirer",
         "org": "Individual",            "bio": "Small business owner needing digital help."},
        {"name": "IEEE WIE MUJ",    "email": "ieee@muj.edu",       "role": "hirer",
         "org": "IEEE Student Branch",   "bio": "Student org needing design & web help."},
    ]
    for h in sample_hirers:
        h["password"] = hashlib.md5(b"password123").hexdigest()
        h["joined"]   = "Feb 2024"
        USERS[h["email"]] = h

    # Sample gigs
    sample_gigs = [
        {"id": 1, "title": "Build a Club Website",         "hirer": "TechStart Club",
         "hirer_email": "techstart@muj.edu", "skill": "Web Development",
         "budget": 2000, "deadline": "2 weeks", "description": "Need a 5-page website for our club with event listings and member portal.",
         "status": "open", "posted": "2 days ago", "applicants": 3},
        {"id": 2, "title": "Design Event Poster",          "hirer": "IEEE WIE MUJ",
         "hirer_email": "ieee@muj.edu",       "skill": "Graphic Design",
         "budget": 500,  "deadline": "3 days", "description": "Design a poster for our upcoming hackathon. Must be vibrant and professional.",
         "status": "open", "posted": "1 day ago", "applicants": 5},
        {"id": 3, "title": "Python Data Analysis Script",  "hirer": "Naveen Kumar",
         "hirer_email": "naveen@gmail.com",   "skill": "Python / ML",
         "budget": 1500, "deadline": "1 week", "description": "Analyze 3 months of sales data. Visualize trends. Deliver Jupyter notebook.",
         "status": "open", "posted": "3 days ago", "applicants": 2},
        {"id": 4, "title": "Write 10 Blog Articles",       "hirer": "Naveen Kumar",
         "hirer_email": "naveen@gmail.com",   "skill": "Content Writing",
         "budget": 800,  "deadline": "2 weeks","description": "SEO-optimized blogs for our e-commerce store. Each ~800 words.",
         "status": "open", "posted": "5 days ago", "applicants": 7},
        {"id": 5, "title": "Edit Promotional Video",       "hirer": "TechStart Club",
         "hirer_email": "techstart@muj.edu",  "skill": "Video Editing",
         "budget": 1200, "deadline": "4 days", "description": "Edit a 3-min promo video. Add transitions, captions, background music.",
         "status": "open", "posted": "1 day ago", "applicants": 1},
        {"id": 6, "title": "UI Redesign for Mobile App",   "hirer": "IEEE WIE MUJ",
         "hirer_email": "ieee@muj.edu",       "skill": "UI/UX Design",
         "budget": 3000, "deadline": "3 weeks","description": "Redesign our club app's UI. Deliver Figma prototype with 10 screens.",
         "status": "open", "posted": "1 week ago", "applicants": 4},
        {"id": 7, "title": "Instagram Content Strategy",   "hirer": "Naveen Kumar",
         "hirer_email": "naveen@gmail.com",   "skill": "Digital Marketing",
         "budget": 700,  "deadline": "ongoing","description": "Manage Instagram page. Create 12 posts/month + captions & hashtags.",
         "status": "open", "posted": "2 days ago", "applicants": 6},
        {"id": 8, "title": "Build Flutter Mobile App",     "hirer": "TechStart Club",
         "hirer_email": "techstart@muj.edu",  "skill": "App Development",
         "budget": 4000, "deadline": "1 month","description": "Simple task management app with login, task list, and notifications.",
         "status": "open", "posted": "4 days ago", "applicants": 2},
    ]
    GIGS.extend(sample_gigs)

seed_data()


# ──────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def current_user():
    if "email" in session:
        return USERS.get(session["email"])
    return None

def next_gig_id():
    return max((g["id"] for g in GIGS), default=0) + 1


# ──────────────────────────────────────────────────────────────────────────────
#  AUTH ROUTES
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/")
def landing():
    stats = {
        "students": sum(1 for u in USERS.values() if u["role"] == "student"),
        "hirers":   sum(1 for u in USERS.values() if u["role"] == "hirer"),
        "gigs":     len(GIGS),
    }
    return render_template("landing.html", stats=stats)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role     = request.form.get("role", "student")

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))
        if email in USERS:
            flash("Email already registered.", "error")
            return redirect(url_for("register"))

        user = {
            "name":     name,
            "email":    email,
            "password": hashlib.md5(password.encode()).hexdigest(),
            "role":     role,
            "joined":   datetime.datetime.now().strftime("%b %Y"),
        }
        if role == "student":
            user.update({
                "skill": request.form.get("skill", "Web Development"),
                "experience":   int(request.form.get("experience", 1)),
                "price":        int(request.form.get("price", 500)),
                "availability": int(request.form.get("availability", 10)),
                "bio":          request.form.get("bio", ""),
                "rating":       0,
                "jobs_done":    0,
            })
        else:
            user.update({
                "org": request.form.get("org", "Individual"),
                "bio": request.form.get("bio", ""),
            })

        USERS[email] = user
        session["email"] = email
        flash("Account created successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("register.html", skills=SKILLS_LIST)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = USERS.get(email)
        if user and user["password"] == hashlib.md5(password.encode()).hexdigest():
            session["email"] = email
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


# ──────────────────────────────────────────────────────────────────────────────
#  DASHBOARD  (role-based)
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    if user["role"] == "student":
        # Gigs matching this student's skill
        my_bids   = [b for b in BIDS if b["student_email"] == user["email"]]
        bid_gig_ids = {b["gig_id"] for b in my_bids}
        matching  = [g for g in GIGS if g["skill"] == user.get("skill") and g["status"] == "open"]
        return render_template("student_dashboard.html",
                               user=user, matching_gigs=matching[:5],
                               my_bids=my_bids, bid_gig_ids=bid_gig_ids)
    else:
        my_gigs = [g for g in GIGS if g.get("hirer_email") == user["email"]]
        # For each gig get its bids
        gig_bids = {g["id"]: [b for b in BIDS if b["gig_id"] == g["id"]] for g in my_gigs}
        return render_template("hirer_dashboard.html",
                               user=user, my_gigs=my_gigs, gig_bids=gig_bids)


# ──────────────────────────────────────────────────────────────────────────────
#  BROWSE GIGS  (public)
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/gigs")
def browse_gigs():
    skill_filter  = request.args.get("skill", "all")
    sort_by       = request.args.get("sort", "newest")
    search_query  = request.args.get("q", "").lower()

    gigs = [g for g in GIGS if g["status"] == "open"]

    if skill_filter != "all":
        gigs = [g for g in gigs if g["skill"] == skill_filter]
    if search_query:
        gigs = [g for g in gigs if search_query in g["title"].lower()
                or search_query in g["description"].lower()]
    if sort_by == "budget_high":
        gigs = sorted(gigs, key=lambda g: g["budget"], reverse=True)
    elif sort_by == "budget_low":
        gigs = sorted(gigs, key=lambda g: g["budget"])

    user = current_user()
    bid_gig_ids = set()
    if user and user["role"] == "student":
        bid_gig_ids = {b["gig_id"] for b in BIDS if b["student_email"] == user["email"]}

    return render_template("browse_gigs.html", gigs=gigs, skills=SKILLS_LIST,
                           skill_filter=skill_filter, sort_by=sort_by,
                           search_query=search_query, user=user,
                           bid_gig_ids=bid_gig_ids)


# ──────────────────────────────────────────────────────────────────────────────
#  POST A GIG  (hirers only)
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/post_gig", methods=["GET", "POST"])
def post_gig():
    user = current_user()
    if not user or user["role"] != "hirer":
        flash("Only hirers can post gigs.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        gig = {
            "id":          next_gig_id(),
            "title":       request.form.get("title", "").strip(),
            "hirer":       user["name"],
            "hirer_email": user["email"],
            "skill":       request.form.get("skill"),
            "budget":      int(request.form.get("budget", 500)),
            "deadline":    request.form.get("deadline", "1 week"),
            "description": request.form.get("description", "").strip(),
            "status":      "open",
            "posted":      "Just now",
            "applicants":  0,
        }
        GIGS.append(gig)
        flash("Gig posted successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("post_gig.html", user=user, skills=SKILLS_LIST)


# ──────────────────────────────────────────────────────────────────────────────
#  APPLY TO GIG  (students only)
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/apply/<int:gig_id>", methods=["POST"])
def apply_gig(gig_id):
    user = current_user()
    if not user or user["role"] != "student":
        return jsonify({"ok": False, "msg": "Login as student first."})

    # Check not already applied
    already = any(b["gig_id"] == gig_id and b["student_email"] == user["email"] for b in BIDS)
    if already:
        return jsonify({"ok": False, "msg": "Already applied."})

    gig = next((g for g in GIGS if g["id"] == gig_id), None)
    if not gig:
        return jsonify({"ok": False, "msg": "Gig not found."})

    data = request.get_json()
    bid = {
        "gig_id":        gig_id,
        "gig_title":     gig["title"],
        "student_email": user["email"],
        "student_name":  user["name"],
        "skill":         user.get("skill"),
        "experience":    user.get("experience"),
        "price":         user.get("price"),
        "message":       data.get("message", ""),
        "status":        "pending",
        "applied":       "Just now",
    }
    BIDS.append(bid)
    gig["applicants"] += 1
    return jsonify({"ok": True, "msg": "Application sent!"})


# ──────────────────────────────────────────────────────────────────────────────
#  BROWSE STUDENTS  (public talent marketplace)
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/students")
def browse_students():
    skill_filter = request.args.get("skill", "all")
    sort_by      = request.args.get("sort", "rating")
    search_query = request.args.get("q", "").lower()

    students = [u for u in USERS.values() if u["role"] == "student"]

    if skill_filter != "all":
        students = [s for s in students if s.get("skill") == skill_filter]
    if search_query:
        students = [s for s in students if search_query in s["name"].lower()
                    or search_query in s.get("skill", "").lower()]
    if sort_by == "rating":
        students = sorted(students, key=lambda s: s.get("rating", 0), reverse=True)
    elif sort_by == "price_low":
        students = sorted(students, key=lambda s: s.get("price", 0))
    elif sort_by == "price_high":
        students = sorted(students, key=lambda s: s.get("price", 0), reverse=True)
    elif sort_by == "experience":
        students = sorted(students, key=lambda s: s.get("experience", 0), reverse=True)

    user = current_user()
    return render_template("browse_students.html", students=students,
                           skills=SKILLS_LIST, skill_filter=skill_filter,
                           sort_by=sort_by, search_query=search_query, user=user)


# ──────────────────────────────────────────────────────────────────────────────
#  AI TOOLS PAGE
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/tools")
def tools():
    user = current_user()
    return render_template("tools.html", user=user, skills=SKILLS_LIST)

# ── Pay Prediction ──
@app.route("/api/predict_pay", methods=["POST"])
def api_predict_pay():
    d = request.get_json()
    exp   = float(d.get("experience", 1))
    avail = float(d.get("availability", 10))
    price = float(d.get("price", 500))

    base     = price * (avail / 10)
    exp_mult = 1 + (exp * 0.28)
    noise    = random.uniform(0.93, 1.07)
    earning  = round(base * exp_mult * noise)

    # breakdown
    gigs_per_month = round(avail * 4.2 / 5)
    return jsonify({
        "monthly_earning": earning,
        "gigs_estimate":   gigs_per_month,
        "hourly_rate":     round(price / 3),
        "annual_estimate": earning * 12,
    })

# ── Price Suggestion ──
@app.route("/api/suggest_price", methods=["POST"])
def api_suggest_price():
    d = request.get_json()
    exp        = float(d.get("experience", 1))
    avail      = float(d.get("availability", 10))
    has_earned = d.get("has_earned", "no").lower()
    skill      = d.get("skill", "Web Development")

    skill_multipliers = {
        "Web Development": 1.3, "App Development": 1.4, "Python / ML": 1.35,
        "Cybersecurity": 1.4,   "Cloud Computing": 1.35, "UI/UX Design": 1.25,
        "Data Analysis": 1.2,   "Graphic Design": 1.0,   "Video Editing": 1.1,
        "Digital Marketing": 1.0,"Content Writing": 0.85, "Tutoring / Teaching": 0.9,
        "Game Development": 1.3, "3D Modeling": 1.2,      "Database Management": 1.2,
    }
    base = 400 + (exp * 350)
    mult = skill_multipliers.get(skill, 1.0)
    earned_bonus = 150 if has_earned == "yes" else 0
    avail_factor = 1.0 if avail >= 15 else 0.92

    suggested = round((base * mult + earned_bonus) * avail_factor / 50) * 50
    low  = round(suggested * 0.80 / 50) * 50
    high = round(suggested * 1.25 / 50) * 50

    return jsonify({"suggested": suggested, "low": low, "high": high})

# ── Hiring Prediction ──
@app.route("/api/predict_hiring", methods=["POST"])
def api_predict_hiring():
    d = request.get_json()
    exp      = float(d.get("experience", 1))
    price    = float(d.get("price", 500))
    adoption = float(d.get("adoption_score", 5))

    score = 0
    factors = []
    if exp >= 3:   score += 3; factors.append(("Experience", "Strong", "+3"))
    elif exp >= 1: score += 2; factors.append(("Experience", "Moderate", "+2"))
    else:          score += 0; factors.append(("Experience", "Weak", "+0"))

    if price <= 1000:   score += 3; factors.append(("Pricing", "Very Competitive", "+3"))
    elif price <= 2000: score += 2; factors.append(("Pricing", "Competitive", "+2"))
    elif price <= 3000: score += 1; factors.append(("Pricing", "Moderate", "+1"))
    else:               score += 0; factors.append(("Pricing", "High", "+0"))

    if adoption >= 8:   score += 4; factors.append(("Adoption Score", "Excellent", "+4"))
    elif adoption >= 6: score += 3; factors.append(("Adoption Score", "Good", "+3"))
    elif adoption >= 4: score += 2; factors.append(("Adoption Score", "Fair", "+2"))
    else:               score += 1; factors.append(("Adoption Score", "Low", "+1"))

    max_score = 10
    probability = round((score / max_score) * 100)
    result = "Likely to Hire" if score >= 5 else "Not Likely to Hire"
    label  = "positive" if score >= 5 else "negative"

    return jsonify({"result": result, "label": label,
                    "score": score, "probability": probability, "factors": factors})

# ── Recommendation ──
@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    d = request.get_json()
    skill  = d.get("skill", "Web Development")
    exp    = float(d.get("experience", 1))
    budget = float(d.get("budget", 1000))

    students = [u for u in USERS.values() if u["role"] == "student"]
    
    # Pehle sirf matching skill wale students lo
    skill_matched = [s for s in students if s.get("skill") == skill]
    
    # Agar koi nahi mila toh clear message do
    if not skill_matched:
        return jsonify({
            "recommendations": [],
            "message": f"No students found with skill: {skill}"
        })
    
    # Ab sirf matching students mein se best sort karo by experience & price
    scored = []
    for s in skill_matched:
        exp_diff   = abs(s.get("experience", 1) - exp)
        price_diff = abs(s.get("price", 500) - budget) / 1000
        distance   = exp_diff + price_diff
        scored.append((distance, s))

    scored.sort(key=lambda x: x[0])
    
    recs = []
    for _, s in scored[:5]:
        recs.append({
            "name":       s["name"],
            "skill":      s.get("skill"),
            "experience": s.get("experience"),
            "price":      s.get("price"),
            "rating":     s.get("rating", 0),
            "jobs_done":  s.get("jobs_done", 0),
            "bio":        s.get("bio", ""),
        })

    return jsonify({"recommendations": recs})

# ──────────────────────────────────────────────────────────────────────────────
#  PROFILE
# ──────────────────────────────────────────────────────────────────────────────
@app.route("/profile", methods=["GET", "POST"])
def profile():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        user["bio"] = request.form.get("bio", user.get("bio", ""))
        if user["role"] == "student":
            user["skill"]        = request.form.get("skill", user.get("skill"))
            user["experience"]   = int(request.form.get("experience", user.get("experience", 1)))
            user["price"]        = int(request.form.get("price", user.get("price", 500)))
            user["availability"] = int(request.form.get("availability", user.get("availability", 10)))
        else:
            user["org"] = request.form.get("org", user.get("org", "Individual"))
        flash("Profile updated!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", user=user, skills=SKILLS_LIST)


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
