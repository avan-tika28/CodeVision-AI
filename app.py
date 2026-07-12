from flask import Flask, render_template, request, redirect, session
import sqlite3
import matplotlib.pyplot as plt
import io
import contextlib

app = Flask(__name__)
app.secret_key = "codevisionai"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user_name"] = user[1]
            session["user_email"] = user[2]
            return redirect("/dashboard")
        else:
            return render_template("login_failed.html")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return render_template("register_success.html")

    return render_template("register.html")
# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user_name" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Total Problems
    cursor.execute("SELECT COUNT(*) FROM problems")
    total = cursor.fetchone()[0]

    # Solved Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE status='Solved'")
    solved = cursor.fetchone()[0]
    # Favorite Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE favorite='Yes'")
    favorites = cursor.fetchone()[0]

    # Easy Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE difficulty='Easy'")
    easy = cursor.fetchone()[0]

    # Medium Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE difficulty='Medium'")
    medium = cursor.fetchone()[0]

    # Hard Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE difficulty='Hard'")
    hard = cursor.fetchone()[0]

    # Achievement Badge
    if solved >= 20:
        badge = "👑 Code Master"
    elif solved >= 15:
        badge = "🥇 Gold Coder"
    elif solved >= 10:
        badge = "🥈 Silver Coder"
    elif solved >= 5:
        badge = "🥉 Bronze Coder"
    else:
        badge = "🔰 Beginner"

    # Remaining Problems
    remaining = total - solved

    # Create Pie Chart
    plt.figure(figsize=(5, 5))

    plt.pie(
        [solved, remaining],
        labels=["Solved", "Remaining"],
        autopct="%1.1f%%",
        colors=["green", "red"]
    )

    plt.title("Problem Progress")
    plt.savefig("static/charts/progress.png")
    plt.close()

    # Progress Percentage
    if total > 0:
        progress = int((solved / total) * 100)
    else:
        progress = 0

    conn.close()

    return render_template(
        "dashboard.html",
        username=session["user_name"],
        total=total,
        solved=solved,
        remaining=remaining,
        progress=progress,
        easy=easy,
        medium=medium,
        hard=hard,
        badge=badge,
        favorites=favorites
    )
@app.route("/submit_code/<int:id>", methods=["POST"])
def submit_code(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE problems SET status='Solved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()
    return redirect("/problem/" + str(id) + "?submitted=1")
# ---------------- PROBLEMS ----------------
@app.route("/problems")
def problems():

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")

    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    query = "SELECT * FROM problems WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append("%" + search + "%")

    if difficulty:
        query += " AND difficulty=?"
        params.append(difficulty)

    # Count total records
    count_query = query
    cursor.execute(count_query, params)
    total = len(cursor.fetchall())

    # Fetch paginated records
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    problems = cursor.fetchall()

    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "problems.html",
        problems=problems,
        search=search,
        difficulty=difficulty,
        page=page,
        total_pages=total_pages
    )

#-----------create problem page--------
@app.route("/problem/<int:problem_id>")
def problem_detail(problem_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM problems WHERE id=?", (problem_id,))
    problem = cursor.fetchone()

    conn.close()

    return render_template("problem_detail.html", problem=problem)
# ---------------- LEADERBOARD ----------------
@app.route("/leaderboard")
def leaderboard():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        name,
        (SELECT COUNT(*) FROM problems WHERE status='Solved') AS solved,
        (SELECT COUNT(*) FROM problems WHERE favorite='Yes') AS favorites
    FROM users
    """)

    users = cursor.fetchall()

    conn.close()

    return render_template("leaderboard.html", users=users)


# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    return render_template("profile.html")


# ---------------- PROGRESS ----------------
@app.route("/progress")
def progress():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Total Problems
    cursor.execute("SELECT COUNT(*) FROM problems")
    total = cursor.fetchone()[0]

    # Solved Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE status='Solved'")
    solved = cursor.fetchone()[0]

    # Remaining Problems
    remaining = total - solved

    # Progress Percentage
    if total > 0:
        progress = int((solved / total) * 100)
    else:
        progress = 0

    conn.close()

    return render_template(
        "progress.html",
        total=total,
        solved=solved,
        remaining=remaining,
        progress=progress
    )



# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
# ---------------- ADD PROBLEM ----------------
@app.route("/add_problem", methods=["GET", "POST"])
def add_problem():

    if request.method == "POST":

        title = request.form["title"]
        difficulty = request.form["difficulty"]
        description = request.form["description"]
        status = "Not Solved"

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
    "INSERT INTO problems(title, difficulty, description, status) VALUES(?, ?, ?, ?)",
    (title, difficulty, description, status)
)

        conn.commit()
        conn.close()

        return render_template("problem_added.html")

    return render_template("add_problem.html")


# ---------------- EDIT PROBLEM ----------------
@app.route("/edit_problem/<int:id>", methods=["GET", "POST"])
def edit_problem(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        difficulty = request.form["difficulty"]
        description = request.form["description"]

        cursor.execute(
            "UPDATE problems SET title=?, difficulty=?, description=? WHERE id=?",
            (title, difficulty, description, id)
        )

        conn.commit()
        conn.close()

        return redirect("/problems")

    cursor.execute(
        "SELECT * FROM problems WHERE id=?",
        (id,)
    )

    problem = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_problem.html",
        problem=problem
    )


# ---------------- DELETE PROBLEM ----------------
@app.route("/delete_problem/<int:id>")
def delete_problem(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM problems WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/problems")

# ---------------- MARK AS SOLVED ----------------
@app.route("/solve_problem/<int:id>")
def solve_problem(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE problems SET status='Solved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/problems")

# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET password=? WHERE email=?",
            (password, email)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("forgot_password.html")

@app.route("/ai_hint/<int:id>")
def ai_hint(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM problems WHERE id=?",
        (id,)
    )

    problem = cursor.fetchone()

    conn.close()

    hint = ""

    if "Binary" in problem[1]:
        hint = "Use low, high and mid pointers."

    elif "Two Sum" in problem[1]:
        hint = "Think about using a HashMap to store visited numbers."

    elif "Linked List" in problem[1]:
        hint = "Use three pointers: previous, current and next."

    elif "Merge" in problem[1]:
        hint = "Sort the intervals before merging."

    else:
        hint = "Break the problem into smaller steps and choose the best data structure."

    return render_template(
        "ai_hint.html",
        problem=problem,
        hint=hint
    )
@app.route("/favorite/<int:id>")
def favorite(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT favorite FROM problems WHERE id=?",
        (id,)
    )

    current = cursor.fetchone()[0]

    if current == "Yes":
        cursor.execute(
            "UPDATE problems SET favorite='No' WHERE id=?",
            (id,)
        )
    else:
        cursor.execute(
            "UPDATE problems SET favorite='Yes' WHERE id=?",
            (id,)
        )

    conn.commit()
    conn.close()

    return redirect("/problems")


@app.route("/statistics")
def statistics():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Total Problems
    cursor.execute("SELECT COUNT(*) FROM problems")
    total = cursor.fetchone()[0]

    # Solved Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE status='Solved'")
    solved = cursor.fetchone()[0]

    # Easy Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE difficulty='Easy'")
    easy = cursor.fetchone()[0]

    # Medium Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE difficulty='Medium'")
    medium = cursor.fetchone()[0]

    # Hard Problems
    cursor.execute("SELECT COUNT(*) FROM problems WHERE difficulty='Hard'")
    hard = cursor.fetchone()[0]

    remaining = total - solved

    if solved >= 20:
        badge = "👑 Code Master"
    elif solved >= 15:
        badge = "🥇 Gold Coder"
    elif solved >= 10:
        badge = "🥈 Silver Coder"
    elif solved >= 5:
        badge = "🥉 Bronze Coder"
    else:
        badge = "🔰 Beginner"

    conn.close()

    return render_template(
        "statistics.html",
        total=total,
        solved=solved,
        remaining=remaining,
        easy=easy,
        medium=medium,
        hard=hard,
        badge=badge
    )
@app.route("/run_code/<int:id>", methods=["POST"])
def run_code(id):

    code = request.form["code"]

    output_buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {})

        output = output_buffer.getvalue()

        if output.strip() == "":
            output = "Program executed successfully. No output."

    except Exception as e:
        output = f"Error:\n{e}"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM problems WHERE id=?", (id,))
    problem = cursor.fetchone()

    conn.close()

    return render_template(
        "problem_detail.html",
        problem=problem,
        code=code,
        output=output
    )
@app.route("/favorites")
def favorites():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM problems WHERE favorite='Yes'"
    )

    problems = cursor.fetchall()

    conn.close()

    return render_template(
        "favorites.html",
        problems=problems
    )


    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, status
        FROM problems
        ORDER BY status DESC, title ASC
        LIMIT 20
    """)

    problems = cursor.fetchall()

    conn.close()

    return render_template(
        "leaderboard.html",
        problems=problems
    )
# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
