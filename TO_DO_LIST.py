import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, description, priority, due_date):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        
        self.tasks = []
        
        # Create labels
        tk.Label(root, text="Task Description").grid(row=0, column=0)
        tk.Label(root, text="Priority (High/Medium/Low)").grid(row=1, column=0)
        tk.Label(root, text="Due Date").grid(row=2, column=0)
        
        # Entry fields
        self.description_entry = tk.Entry(root)
        self.priority_entry = tk.Entry(root)
        self.due_date_entry = tk.Entry(root)
        
        self.description_entry.grid(row=0, column=1)
        self.priority_entry.grid(row=1, column=1)
        self.due_date_entry.grid(row=2, column=1)
        
        # Buttons
        tk.Button(root, text="Add Task", command=self.add_task).grid(row=3, column=0)
        tk.Button(root, text="Remove Task", command=self.remove_task).grid(row=3, column=1)
        tk.Button(root, text="Mark as Completed", command=self.mark_completed).grid(row=3, column=2)
        
        # Task Listbox
        self.task_listbox = tk.Listbox(root, width=50, height=15)
        self.task_listbox.grid(row=4, columnspan=3)
        
        # Load tasks from file
        self.load_tasks()
        self.update_listbox()
    
    def add_task(self):
        description = self.description_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()
        
        if description and priority and due_date:
            task = Task(description, priority, due_date)
            self.tasks.append(task)
            self.update_listbox()
            self.save_tasks()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")
    
    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            self.update_listbox()
            self.save_tasks()
    
    def mark_completed(self):
        selected_task_index = self.task_listbox.curselection()
        
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index].completed = True
            self.update_listbox()
            self.save_tasks()
    
    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[x]" if task.completed else "[ ]"
            self.task_listbox.insert(tk.END, f"{status} {task.description} (Priority: {task.priority}, Due: {task.due_date})")
    
    def clear_entries(self):
        self.description_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
    
    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task.description},{task.priority},{task.due_date},{task.completed}\n")
    
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(",")
                    description, priority, due_date, completed = data
                    task = Task(description, priority, due_date)
                    if completed == "True":
                        task.completed = True
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
