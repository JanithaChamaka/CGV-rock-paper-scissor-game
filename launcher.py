import tkinter as tk
from tkinter import messagebox
import threading
import Main
def start_game():
    root.destroy()  # close the launcher window
    threading.Thread(target=Main.main).start()  # run the game in a new thread

# GUI window
root = tk.Tk()
root.title("Rock Paper Scissors Game")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

label = tk.Label(root, text="Welcome to Rock Paper Scissors!", font=("Arial", 20), bg="#f0f0f0")
label.pack(pady=50)

start_btn = tk.Button(root, text="Play", font=("Arial", 25), command=start_game, bg="#4CAF50", fg="white", width=5, height=1)
start_btn.pack(side="left", padx=100)

exit_btn = tk.Button(root, text="Exit", font=("Arial", 25), command=root.quit, bg="#f44336", fg="white", width=5, height=1)
exit_btn.pack(side="left", padx=100)

root.mainloop()
