import tkinter as tk
from tkinter import messagebox


class ProductivityTimer:
	def __init__(self, root):
		self.root = root
		self.root.title("Productivity Timer")
		self.root.resizable(False, False)

		self.remaining_seconds = 25 * 60
		self.timer_running = False
		self.timer_job = None

		self.minutes = tk.StringVar(value="25")
		self.display = tk.StringVar()
		self.status = tk.StringVar(value="Ready to focus")

		tk.Label(
			root,
			text="PRODUCTIVITY TIMER",
			font=("Arial", 16, "bold"),
			pady=12,
		).pack()

		tk.Label(
			root,
			textvariable=self.display,
			font=("Arial", 48, "bold"),
			width=5,
		).pack(pady=8)

		tk.Label(root, textvariable=self.status, font=("Arial", 11)).pack()

		settings = tk.Frame(root, pady=12)
		settings.pack()
		tk.Label(settings, text="Minutes:").pack(side=tk.LEFT, padx=(0, 6))
		tk.Entry(settings, textvariable=self.minutes, width=5, justify="center").pack(
			side=tk.LEFT
		)

		controls = tk.Frame(root, pady=8)
		controls.pack()
		self.start_button = tk.Button(
			controls, text="Start", width=10, command=self.toggle_timer
		)
		self.start_button.pack(side=tk.LEFT, padx=4)
		tk.Button(controls, text="Reset", width=10, command=self.reset_timer).pack(
			side=tk.LEFT, padx=4
		)

		self.update_display()

	def update_display(self):
		minutes, seconds = divmod(self.remaining_seconds, 60)
		self.display.set(f"{minutes:02d}:{seconds:02d}")

	def toggle_timer(self):
		if self.timer_running:
			self.pause_timer()
		else:
			self.start_timer()

	def start_timer(self):
		if self.remaining_seconds <= 0:
			self.reset_timer()

		if not self.timer_running:
			self.timer_running = True
			self.start_button.config(text="Pause")
			self.status.set("Focus time")
			self.countdown()

	def pause_timer(self):
		self.timer_running = False
		self.start_button.config(text="Start")
		self.status.set("Paused")
		if self.timer_job is not None:
			self.root.after_cancel(self.timer_job)
			self.timer_job = None

	def reset_timer(self):
		try:
			minutes = int(self.minutes.get())
			if minutes <= 0:
				raise ValueError
		except ValueError:
			messagebox.showerror("Invalid time", "Enter a whole number greater than 0.")
			return

		self.pause_timer()
		self.remaining_seconds = minutes * 60
		self.status.set("Ready to focus")
		self.update_display()

	def countdown(self):
		self.update_display()
		if self.remaining_seconds == 0:
			self.timer_running = False
			self.start_button.config(text="Start")
			self.status.set("Time is up!")
			self.root.bell()
			messagebox.showinfo("Timer complete", "Great work. Time for a break!")
			return

		self.remaining_seconds -= 1
		self.timer_job = self.root.after(1000, self.countdown)


if __name__ == "__main__":
	window = tk.Tk()
	window.attributes("-fullscreen", True)
	window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))
	ProductivityTimer(window)
	window.mainloop()
