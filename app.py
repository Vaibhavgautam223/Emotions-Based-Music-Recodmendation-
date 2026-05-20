from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for

import auth
import db_helper
from mood_map import MOOD_MAP
from spotify_helper import get_playlist

app = Flask(__name__)
app.secret_key = "moodtunes_secret_key_2024"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def detect_mood_from_text(mood_text):
    mood_text = (mood_text or "").strip().lower()
    if not mood_text:
        return None

    keywords = {
        "happy": ["happy", "joy", "good", "great", "excited", "cheerful"],
        "sad": ["sad", "down", "upset", "depressed", "cry", "heartbroken"],
        "calm": ["calm", "peaceful", "relaxed", "ease", "serene"],
        "energetic": ["energetic", "pumped", "workout", "active", "hype"],
        "angry": ["angry", "mad", "furious", "annoyed", "rage"],
        "romantic": ["romantic", "love", "loving", "date", "crush"],
        "focused": ["focused", "study", "studying", "work", "productive", "concentrate"],
        "sleepy": ["sleepy", "tired", "sleep", "drowsy", "bedtime"],
    }

    for mood, words in keywords.items():
        if any(word in mood_text for word in words):
            return mood
    return None


@app.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        moods=MOOD_MAP,
        username=session.get("username", "Listener"),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        result = auth.register_user(username, email, password)
        if result != "ok":
            flash(result, "error")
            return render_template("register.html")

        flash("Account created. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = auth.login_user(username, password)

        if not user:
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash("Logged in successfully.", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/playlist", methods=["POST"])
@login_required
def playlist():
    selected_mood = request.form.get("mood", "").strip().lower()
    detected_mood = detect_mood_from_text(request.form.get("mood_text", ""))
    mood = selected_mood or detected_mood or "happy"

    if mood not in MOOD_MAP:
        flash("Unsupported mood selected.", "error")
        return redirect(url_for("index"))

    songs = get_playlist(mood)
    db_helper.save_session(session["user_id"], mood, songs)
    return render_template(
        "playlist.html",
        mood=mood,
        mood_data=MOOD_MAP[mood],
        songs=songs,
    )


@app.route("/history")
@login_required
def history():
    records = db_helper.get_history(session["user_id"])
    return render_template(
        "history.html",
        records=records,
        username=session.get("username", "Listener"),
    )


db_helper.init_db()


if __name__ == "__main__":
    app.run(debug=True)
