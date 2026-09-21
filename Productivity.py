import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


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
		self.session_number = 0

		self.minutes = tk.StringVar(value="25")
		self.display = tk.StringVar()
		self.status = tk.StringVar(value="Ready to focus")
		self.break_minutes = tk.StringVar(value="5")
		self.break_display = tk.StringVar()
		self.break_status = tk.StringVar(value="Ready for a break")
		self.task_text = tk.StringVar()

		notebook = ttk.Notebook(root)
		notebook.pack(fill="both", expand=True)
		timer_tab = tk.Frame(notebook, bg="#f6efe6")
		history_tab = tk.Frame(notebook)
		notebook.add(timer_tab, text="Timers")
		notebook.add(history_tab, text="History")
		self.create_dorm_background(timer_tab)

		tk.Label(
			timer_tab,
			text="PRODUCTIVITY TIMER",
			font=("Arial", 16, "bold"),
			pady=12,
		).pack()

		tk.Label(
			timer_tab,
			textvariable=self.display,
			font=("Arial", 48, "bold"),
			width=5,
		).pack(pady=8)

		tk.Label(timer_tab, textvariable=self.status, font=("Arial", 11)).pack()

		settings = tk.Frame(timer_tab, pady=12)
		settings.pack()
		tk.Label(settings, text="Minutes:").pack(side=tk.LEFT, padx=(0, 6))
		tk.Entry(settings, textvariable=self.minutes, width=5, justify="center").pack(
			side=tk.LEFT
		)

		controls = tk.Frame(timer_tab, pady=8)
		controls.pack()
		self.start_button = tk.Button(
			controls, text="Start", width=10, command=self.toggle_timer
		)
		self.start_button.pack(side=tk.LEFT, padx=4)
		tk.Button(controls, text="Reset", width=10, command=self.reset_timer).pack(
			side=tk.LEFT, padx=4
		)

		tasks_frame = tk.Frame(timer_tab, pady=8)
		tasks_frame.pack()
		tk.Label(tasks_frame, text="TASKS", font=("Arial", 14, "bold")).pack()
		task_entry_frame = tk.Frame(tasks_frame, pady=6)
		task_entry_frame.pack()
		task_entry = tk.Entry(task_entry_frame, textvariable=self.task_text, width=34)
		task_entry.pack(side=tk.LEFT, padx=(0, 6))
		task_entry.bind("<Return>", lambda event: self.add_task())
		tk.Button(task_entry_frame, text="Add", command=self.add_task).pack(
			side=tk.LEFT
		)
		self.task_list = tk.Listbox(tasks_frame, width=44, height=5)
		self.task_list.pack()
		tk.Button(
			tasks_frame, text="Remove Selected", command=self.remove_selected_task
		).pack(pady=(6, 0))

		break_frame = tk.Frame(timer_tab, pady=12)
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

		tk.Label(
			history_tab, text="COMPLETED SESSIONS", font=("Arial", 14, "bold")
		).pack(pady=(16, 8))
		history_frame = tk.Frame(history_tab)
		history_frame.pack(padx=16, pady=4)
		self.history = ttk.Treeview(
			history_frame,
			columns=("session", "type", "duration", "status"),
			show="headings",
			height=12,
		)
		self.history.heading("session", text="#")
		self.history.heading("type", text="Type")
		self.history.heading("duration", text="Duration")
		self.history.heading("status", text="Status")
		self.history.column("session", width=45, anchor="center")
		self.history.column("type", width=100, anchor="center")
		self.history.column("duration", width=100, anchor="center")
		self.history.column("status", width=100, anchor="center")
		self.history.pack()
		tk.Button(
			history_tab, text="Clear History", command=self.clear_history
		).pack(pady=12)

		self.update_display()
		self.update_break_display()

	def create_dorm_background(self, parent):
		background = tk.Canvas(
			parent, bg="#f6efe6", highlightthickness=0, bd=0
		)
		background.place(relx=0, rely=0, relwidth=1, relheight=1)

		background.create_rectangle(0, 0, 1400, 620, fill="#f6efe6", outline="")
		background.create_rectangle(0, 620, 1400, 900, fill="#d9c3ae", outline="")
		background.create_line(0, 620, 1400, 620, fill="#c8ac96", width=5)

		background.create_rectangle(70, 85, 350, 330, fill="#d6e9ec", outline="#8bb1b7", width=8)
		background.create_line(210, 90, 210, 325, fill="#8bb1b7", width=6)
		background.create_line(75, 205, 345, 205, fill="#8bb1b7", width=6)
		background.create_oval(105, 120, 145, 160, fill="#fff3b0", outline="")
		background.create_oval(270, 120, 310, 160, fill="#fff3b0", outline="")

		background.create_rectangle(830, 170, 1260, 560, fill="#a98472", outline="#795f57", width=8)
		background.create_rectangle(870, 215, 1220, 540, fill="#dbe8ec", outline="")
		background.create_rectangle(870, 215, 1220, 325, fill="#c4dce1", outline="")
		background.create_oval(885, 235, 935, 285, fill="#fff3b0", outline="")
		background.create_line(870, 325, 1220, 325, fill="#b7ced2", width=4)

		background.create_rectangle(500, 420, 790, 585, fill="#c98f83", outline="#9e6b65", width=6)
		background.create_rectangle(465, 365, 790, 470, fill="#e7b1a5", outline="#9e6b65", width=6)
		background.create_rectangle(490, 385, 620, 455, fill="#f7d8c8", outline="")
		background.create_rectangle(720, 365, 790, 585, fill="#8c6c62", outline="#70534e", width=5)
		background.create_oval(735, 390, 775, 430, fill="#f0c6a8", outline="")

		background.create_rectangle(80, 485, 390, 535, fill="#b87d5c", outline="#855a49", width=5)
		background.create_rectangle(105, 535, 135, 625, fill="#855a49", outline="")
		background.create_rectangle(335, 535, 365, 625, fill="#855a49", outline="")
		background.create_rectangle(165, 440, 305, 485, fill="#f0d49b", outline="#a67d56", width=4)
		background.create_rectangle(200, 390, 270, 440, fill="#f7e7bf", outline="#a67d56", width=4)

		background.create_rectangle(1170, 510, 1250, 555, fill="#e7a58e", outline="#a66e67", width=4)
		background.create_line(1190, 510, 1165, 440, fill="#6f916e", width=10)
		background.create_line(1210, 510, 1240, 420, fill="#6f916e", width=10)
		background.create_oval(1135, 415, 1190, 465, fill="#8caf82", outline="#648061", width=3)
		background.create_oval(1215, 395, 1270, 450, fill="#8caf82", outline="#648061", width=3)
		background.create_oval(1165, 455, 1220, 505, fill="#8caf82", outline="#648061", width=3)
	def update_display(self):
		minutes, seconds = divmod(self.remaining_seconds, 60)
		self.display.set(f"{minutes:02d}:{seconds:02d}")

	def update_break_display(self):
		minutes, seconds = divmod(self.break_remaining_seconds, 60)
		self.break_display.set(f"{minutes:02d}:{seconds:02d}")

	def add_task(self):
		task = self.task_text.get().strip()
		if task:
			self.task_list.insert(tk.END, task)
			self.task_text.set("")

	def remove_selected_task(self):
		selected_tasks = self.task_list.curselection()
		for task_index in reversed(selected_tasks):
			self.task_list.delete(task_index)

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

	def add_history_entry(self, timer_type, duration_minutes):
		self.session_number += 1
		self.history.insert(
			"",
			"end",
			values=(self.session_number, timer_type, f"{duration_minutes} min", "Completed"),
		)

	def clear_history(self):
		for item in self.history.get_children():
			self.history.delete(item)
		self.session_number = 0

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
			self.add_history_entry("Focus", self.minutes.get())
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
			self.add_history_entry("Break", self.break_minutes.get())
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
