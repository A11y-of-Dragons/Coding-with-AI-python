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
		self.break_remaining_seconds = 5 * 60
		self.break_timer_running = False
		self.break_timer_job = None

		self.minutes = tk.StringVar(value="25")
		self.display = tk.StringVar()
		self.status = tk.StringVar(value="Ready to focus")
		self.break_minutes = tk.StringVar(value="5")
		self.break_display = tk.StringVar()
		self.break_status = tk.StringVar(value="Ready for a break")

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

		break_frame = tk.Frame(root, pady=12)
		break_frame.pack()
		tk.Label(
			break_frame,
			text="BREAK TIMER",
			font=("Arial", 14, "bold"),
		).pack()
		tk.Label(
			break_frame,
			textvariable=self.break_display,
			font=("Arial", 36, "bold"),
			width=5,
		).pack(pady=4)
		tk.Label(break_frame, textvariable=self.break_status, font=("Arial", 11)).pack()

		break_settings = tk.Frame(break_frame, pady=8)
		break_settings.pack()
		tk.Label(break_settings, text="Break minutes:").pack(side=tk.LEFT, padx=(0, 6))
		tk.Entry(
			break_settings, textvariable=self.break_minutes, width=5, justify="center"
		).pack(side=tk.LEFT)

		break_controls = tk.Frame(break_frame, pady=4)
		break_controls.pack()
		self.break_start_button = tk.Button(
			break_controls, text="Start Break", width=10, command=self.toggle_break_timer
		)
		self.break_start_button.pack(side=tk.LEFT, padx=4)
		tk.Button(
			break_controls, text="Reset Break", width=10, command=self.reset_break_timer
		).pack(side=tk.LEFT, padx=4)

		self.update_display()
		self.update_break_display()

	def update_display(self):
		minutes, seconds = divmod(self.remaining_seconds, 60)
		self.display.set(f"{minutes:02d}:{seconds:02d}")

	def update_break_display(self):
		minutes, seconds = divmod(self.break_remaining_seconds, 60)
		self.break_display.set(f"{minutes:02d}:{seconds:02d}")

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

	def toggle_break_timer(self):
		if self.break_timer_running:
			self.pause_break_timer()
		else:
			self.start_break_timer()

	def start_break_timer(self):
		if self.break_remaining_seconds <= 0:
			self.reset_break_timer()

		if not self.break_timer_running:
			self.break_timer_running = True
			self.break_start_button.config(text="Pause Break")
			self.break_status.set("Break time")
			self.break_countdown()

	def pause_break_timer(self):
		self.break_timer_running = False
		self.break_start_button.config(text="Start Break")
		self.break_status.set("Break paused")
		if self.break_timer_job is not None:
			self.root.after_cancel(self.break_timer_job)
			self.break_timer_job = None

	def reset_break_timer(self):
		try:
			minutes = int(self.break_minutes.get())
			if minutes <= 0:
				raise ValueError
		except ValueError:
			messagebox.showerror("Invalid break time", "Enter a whole number greater than 0.")
			return

		self.pause_break_timer()
		self.break_remaining_seconds = minutes * 60
		self.break_status.set("Ready for a break")
		self.update_break_display()

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

	def break_countdown(self):
		self.update_break_display()
		if self.break_remaining_seconds == 0:
			self.break_timer_running = False
			self.break_start_button.config(text="Start Break")
			self.break_status.set("Break is over")
			self.root.bell()
			messagebox.showinfo("Break complete", "Break is over. Ready to focus?")
			return

		self.break_remaining_seconds -= 1
		self.break_timer_job = self.root.after(1000, self.break_countdown)


if __name__ == "__main__":
	window = tk.Tk()
	window.attributes("-fullscreen", True)
	window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))
	ProductivityTimer(window)
	window.mainloop()
