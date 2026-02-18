# 🏰 Tower of Hanoi - Full-Stack Game

A professional implementation of the classic Tower of Hanoi puzzle using a modern tech stack. This project features a web-based UI, real-time database tracking, and interactive Python game logic.

## 🚀 How to Run the Game
Open your terminal in the project folder and run these 3 commands:

   pip install flask pygame pyttsx3 firebase-admin &
   dir &
   python app.py

   Once running, open http://127.0.0.1:5000 in your browser.

  ## Game Features & Functionality
Interactive Homepage: A clean UI where users enter their name and select the number of disks (3-9) from a dropdown.

Real-Time Gameplay: The game tracks steps taken and compares them with the mathematical minimum steps required.

Firebase Integration: All player data, including names, steps, and optional feedback, is updated in real-time to the Firebase Firestore database.

Terminal Analytics: Detailed stats (Username, Steps, Feedback) are displayed directly in the terminal after the game ends.

Voice Support: Interactive audio prompt at satrt of the game using pyttsx3.

   
