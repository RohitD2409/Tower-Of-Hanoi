# ==============================================
# Tower of Hanoi - Flask Application
# ==============================================
# This file manages all routing logic, templates rendering,
# and game integration for the Tower of Hanoi Flask-based web app.
# ==============================================

# -------------------
# Import dependencies
# -------------------
from flask import Flask, render_template, request, redirect, url_for
import subprocess
import sys
import os

# -------------------
# Initialize Flask app
# -------------------
app = Flask(__name__)

# ==============================================
# ROUTES DEFINITIONS
# ==============================================

# -------------------
# Home Page (Index)
# -------------------
@app.route('/')
def index():
    """
    Render the main home page.
    This is the landing screen where player can enter name and disk count.
    """
    print("\n📌 Rendering: index.html (Home Page)\n")
    return render_template('index.html')


# -------------------
# Start Game
# -------------------
@app.route('/start_game', methods=['POST'])
def start_game():
    """
    Starts the Tower of Hanoi game using subprocess.
    Accepts player details and launches the Python game file.
    """
    player_name = request.form.get('playerName')
    disks = request.form.get('disks')

    # Input validation
    if not player_name or not disks:
        print("⚠ Missing player details. Redirecting to Home.")
        return redirect(url_for('index'))

    # Prepare script path and execute
    script_path = os.path.abspath('Towerofhanoi.py')

    try:
        # Launch the game window
        subprocess.Popen([sys.executable, script_path, player_name, disks], shell=True)
        print(f"\n🎮 Game started successfully for player '{player_name}' with {disks} disks.\n")
    except Exception as e:
        print(f"⚠ Error launching TowerofHanoi.py -> {e}")

    # Redirect to home or waiting screen
    return redirect(url_for('index'))


# -------------------
# Game Over Page
# -------------------
@app.route('/game_over')
def game_over_page():
    """
    Displays the 'Game Over' page.
    Includes Play Again and Go Home navigation options.
    Dynamically passes last player's stats to the template for View Stats form.
    """
    print("\n🏁 Rendering: Game Over Screen\n")

    # Use query parameters sent by Towerofhanoi.py
    player_name = request.args.get('username', 'Guest')
    disks_count = request.args.get('disks', 3)
    total_moves = request.args.get('moves', 0)
    feedback_status = request.args.get('feedback', None)  # None means feedback not given yet

    # Determine if feedback form should be shown
    show_feedback_form = True if feedback_status is None else False

    return render_template(
        'game_over.html',
        show_play_again=not show_feedback_form,  # only show play again if feedback given or skipped
        show_feedback_form=show_feedback_form,
        message="Game completed successfully!" if not show_feedback_form else None,
        username=player_name,
        disks=disks_count,
        moves=total_moves,
        feedback_status=feedback_status if feedback_status else "No"
    )


# -------------------
# Feedback Page
# -------------------
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """
    Handles feedback from the player.
    - GET: Shows feedback form.
    - POST: Captures feedback and displays acknowledgment.
    """
    if request.method == 'POST':
        user_feedback = request.form.get('feedback_text', '').strip()
        player_name = request.form.get('username', 'Guest')
        disks = request.form.get('disks', 3)
        moves = request.form.get('moves', 0)

        if user_feedback:
            feedback_status = "Yes"
            print("\n💬 Feedback Received from Player:")
            print("----------------------------------")
            print(user_feedback)
            print("----------------------------------\n")
            message = "✅ Feedback submitted successfully! Thank you for your response."
        else:
            feedback_status = "No"
            print("\nℹ Feedback form submitted empty or skipped by player.\n")
            message = "ℹ You skipped feedback submission."

        # Redirect to Game Over page with feedback processed
        return redirect(url_for('game_over_page',
                                username=player_name,
                                disks=disks,
                                moves=moves,
                                feedback=feedback_status))

    # GET request renders the feedback form
    print("\n📝 Rendering: feedback.html\n")
    return render_template('feedback.html', message=None)


# -------------------
# Skip Feedback
# -------------------
@app.route('/skip_feedback')
def skip_feedback():
    """
    Route triggered when player chooses to skip feedback.
    Returns Game Over page with replay options enabled.
    """
    print("\nℹ Player skipped feedback voluntarily.\n")

    player_name = request.args.get('username', 'Guest')
    disks_count = request.args.get('disks', 3)
    total_moves = request.args.get('moves', 0)
    feedback_status = "No"

    return redirect(url_for('game_over_page',
                            username=player_name,
                            disks=disks_count,
                            moves=total_moves,
                            feedback=feedback_status))


# -------------------
# About Page
# -------------------
@app.route('/about')
def about_page():
    """
    Renders the About page which describes the project,
    tools used, and developer details.
    """
    print("\n📄 Rendering: about.html (About Page)\n")
    return render_template('about.html')


# -------------------
# Gameplay Tips Page
# -------------------
@app.route('/tips')
def tips_page():
    """
    Displays a visually rich 'Gameplay Tips' page.
    Offers hints, strategies, and logic-building advice.
    """
    print("\n💡 Rendering: tips.html (Gameplay Tips Page)\n")
    return render_template('tips.html')


# -------------------
# Game Stats Page
# -------------------
@app.route('/stats', methods=['GET', 'POST'])
def stats_page():
    """
    Renders a statistics page displaying player scores.
    - POST: Receives player stats from game completion and displays dynamically.
    - GET: Shows placeholder/default stats if no game has been played yet.
    """
    print("\n📊 Rendering: stats.html (Player Stats Page)\n")

    if request.method == 'POST':
        username = request.form.get('username')
        disks = request.form.get('disks')
        moves = request.form.get('moves')
        feedback = request.form.get('feedback') or "No"
        print(f"📌 Stats Received -> Player: {username}, Disks: {disks}, Moves: {moves}, Feedback: {feedback}")
        return render_template(
            'stats.html',
            username=username,
            disks=disks,
            moves=moves,
            feedback=feedback
        )

    # GET request shows default placeholder stats
    return render_template(
        'stats.html',
        username=None,
        disks=None,
        moves=None,
        feedback="No"
    )


# -------------------
# Error Handlers (Optional enhancement)
# -------------------
@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 Error Page (future-proof addition).
    Currently redirects users safely to home.
    """
    print("⚠ 404 Page Not Found. Redirecting to Home Page.")
    return redirect(url_for('index'))


# ==============================================
# MAIN EXECUTION POINT
# ==============================================
if __name__ == '__main__':
    print("\n🚀 Launching Tower of Hanoi Flask App ...")
    print("🔗 Visit http://127.0.0.1:5000/ to access the game interface.\n")
    app.run(debug=True)
