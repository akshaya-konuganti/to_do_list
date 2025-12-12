import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os
from datetime import datetime

# File for saving tasks
TASK_FILE = "tasks.json"

# Load/save functions
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Cute To-Do List 🌸💕")
        self.geometry("800x600")
        self.configure(bg="#FFB6C1")

        self.tasks = load_tasks()
        self.selected_task = None

        # Sidebar
        self.sidebar = tk.Frame(self, bg="#FF69B4", width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(self.sidebar, text="Categories", bg="#FF69B4", fg="white", font=("Helvetica", 16, "bold")).pack(pady=10)
        self.category_var = tk.StringVar(value="All")
        self.category_menu = ttk.Combobox(self.sidebar, textvariable=self.category_var, values=["All", "Work", "Personal", "Health"], state="readonly")
        self.category_menu.pack(pady=5)
        self.category_menu.bind("<<ComboboxSelected>>", self.filter_tasks)

        tk.Label(self.sidebar, text="Progress", bg="#FF69B4", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.progress_bar = ttk.Progressbar(self.sidebar, orient="horizontal", length=150, mode="determinate")
        self.progress_bar.pack(pady=5)
        self.update_progress()

        # Main frame
        self.main_frame = tk.Frame(self, bg="#FFF0F5")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(self.main_frame, text="Akki's pink-themed To-Do 💕", bg="#FFF0F5", fg="#FF69B4", font=("Helvetica", 24, "bold")).pack(pady=20)

        # Search
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.main_frame, textvariable=self.search_var, font=("Helvetica", 12), bg="white", fg="#FF69B4")
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_tasks)

        # Input frame
        self.input_frame = tk.Frame(self.main_frame, bg="#FFB6C1")
        self.input_frame.pack(pady=10, fill="x")

        self.task_entry = tk.Entry(self.input_frame, font=("Helvetica", 12), bg="white", fg="#FF69B4", width=30)
        self.task_entry.pack(side="left", padx=10, pady=10)

        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.Combobox(self.input_frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], state="readonly", width=10)
        self.priority_menu.pack(side="left", padx=5)

        self.category_add_var = tk.StringVar(value="Personal")
        self.category_add_menu = ttk.Combobox(self.input_frame, textvariable=self.category_add_var, values=["Work", "Personal", "Health"], state="readonly", width=10)
        self.category_add_menu.pack(side="left", padx=5)

        self.due_entry = tk.Entry(self.input_frame, font=("Helvetica", 12), bg="white", fg="#FF69B4", width=15)
        self.due_entry.pack(side="left", padx=5)

        tk.Button(self.input_frame, text="Add Task ➕", command=self.add_task, bg="#FF69B4", fg="white", font=("Helvetica", 10, "bold")).pack(side="right", padx=10)

        # Task list
        self.task_listbox = tk.Listbox(self.main_frame, width=80, height=15, font=("Helvetica", 12), bg="white", fg="#FF69B4", selectbackground="#FFB6C1")
        self.task_listbox.pack(pady=10, fill="both", expand=True)
        self.task_listbox.bind("<<ListboxSelect>>", self.on_select)

        # Buttons
        self.button_frame = tk.Frame(self.main_frame, bg="#FFB6C1")
        self.button_frame.pack(pady=10, fill="x")

        tk.Button(self.button_frame, text="Mark Done ✅", command=self.mark_done, bg="#FF69B4", fg="white", font=("Helvetica", 10, "bold")).pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Delete 🗑️", command=self.delete_task, bg="#FF69B4", fg="white", font=("Helvetica", 10, "bold")).pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Clear All 🔄", command=self.clear_all, bg="#FF69B4", fg="white", font=("Helvetica", 10, "bold")).pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Export 📄", command=self.export_tasks, bg="#FF69B4", fg="white", font=("Helvetica", 10, "bold")).pack(side="right", padx=10)

        self.display_tasks()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                "text": task_text,
                "priority": self.priority_var.get(),
                "category": self.category_add_var.get(),
                "due_date": self.due_entry.get().strip(),
                "done": False
            }
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.due_entry.delete(0, tk.END)
            self.display_tasks()
            self.update_progress()
            save_tasks(self.tasks)
        else:
            messagebox.showwarning("Warning", "Please enter a task! 🌸")

    def display_tasks(self, filtered=None):
        self.task_listbox.delete(0, tk.END)
        tasks_to_show = filtered if filtered else self.tasks
        for task in tasks_to_show:
            color = {"High": "red", "Medium": "orange", "Low": "green"}[task["priority"]]
            status = "✓ " if task["done"] else "○ "
            due_text = f" (Due: {task['due_date']})" if task["due_date"] else ""
            display_text = f"{status}{task['text']} - {task['category']}{due_text}"
            self.task_listbox.insert(tk.END, display_text)
            self.task_listbox.itemconfig(tk.END, {'fg': color if not task["done"] else "gray"})

    def on_select(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            self.selected_task = selection[0]

    def mark_done(self):
        if self.selected_task is not None:
            self.tasks[self.selected_task]["done"] = True
            self.display_tasks()
            self.update_progress()
            save_tasks(self.tasks)
            self.selected_task = None
        else:
            messagebox.showwarning("Warning", "Please select a task! 💖")

    def delete_task(self):
        if self.selected_task is not None:
            del self.tasks[self.selected_task]
            self.display_tasks()
            self.update_progress()
            save_tasks(self.tasks)
            self.selected_task = None
        else:
            messagebox.showwarning("Warning", "Please select a task! 🗑️")

    def clear_all(self):
        self.tasks = []
        self.display_tasks()
        self.update_progress()
        save_tasks(self.tasks)

    def filter_tasks(self, event=None):
        category = self.category_var.get()
        search = self.search_var.get().lower()
        filtered = [t for t in self.tasks if (category == "All" or t["category"] == category) and search in t["text"].lower()]
        self.display_tasks(filtered)

    def update_progress(self):
        if self.tasks:
            done = sum(1 for t in self.tasks if t["done"])
            self.progress_bar["value"] = (done / len(self.tasks)) * 100
        else:
            self.progress_bar["value"] = 0

    def export_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                for task in self.tasks:
                    f.write(f"{task['text']} - {task['category']} - {'Done' if task['done'] else 'Pending'}\n")

    def on_close(self):
        save_tasks(self.tasks)
        self.destroy()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
