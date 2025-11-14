#!/usr/bin/env python3
"""
Simple persistent CLI To-Do app.
Stores tasks in a text file 'tasks.txt' with one task per line in the format:
<status>|<task text>
where status is 0 (not done) or 1 (done).
"""

import os
import sys

TASKS_FILE = "tasks.txt"


def load_tasks():
    tasks = []
    if not os.path.exists(TASKS_FILE):
        return tasks
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            # expected format: status|task
            parts = line.split("|", 1)
            if len(parts) == 2 and parts[0] in ("0", "1"):
                status = int(parts[0])
                text = parts[1]
                tasks.append({"done": bool(status), "text": text})
            else:
                # fallback: treat whole line as a not-done task
                tasks.append({"done": False, "text": line})
    return tasks


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        for t in tasks:
            status = "1" if t.get("done") else "0"
            f.write(f"{status}|{t.get('text','')}\n")


def list_tasks(tasks):
    if not tasks:
        print("No tasks yet. Add one!\n")
        return
    print("\nYour To-Do List:")
    for i, t in enumerate(tasks, start=1):
        mark = "[x]" if t.get("done") else "[ ]"
        print(f"{i:2d}. {mark} {t.get('text')}")
    print()


def add_task(tasks, text):
    text = text.strip()
    if not text:
        print("Empty task not added.")
        return
    tasks.append({"done": False, "text": text})
    save_tasks(tasks)
    print(f"Added task: {text}")


def remove_task(tasks, index):
    try:
        idx = int(index) - 1
        if idx < 0 or idx >= len(tasks):
            print("Invalid task number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    removed = tasks.pop(idx)
    save_tasks(tasks)
    print(f"Removed task: {removed.get('text')}")


def mark_done(tasks, index, done=True):
    try:
        idx = int(index) - 1
        if idx < 0 or idx >= len(tasks):
            print("Invalid task number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    tasks[idx]["done"] = bool(done)
    save_tasks(tasks)
    state = "Done" if done else "Not done"
    print(f"Marked task {index} as: {state}")


def clear_tasks():
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
    print("All tasks cleared.")


def show_help():
    print(
        """
Commands:
  l, list                 - List all tasks
  a, add <task text>      - Add a new task
  r, remove <task no>     - Remove a task by its number
  d, done <task no>       - Mark task done
  u, undo <task no>       - Mark task not done
  c, clear                - Remove all tasks
  h, help                 - Show this help
  q, quit, exit           - Exit the app
"""
    )


def main():
    tasks = load_tasks()
    print("Simple To-Do CLI (persistent). Type 'h' or 'help' for commands.\n")
    while True:
        try:
            cmd = input("todo> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not cmd:
            continue

        parts = cmd.split(" ", 1)
        action = parts[0].lower()

        arg = parts[1] if len(parts) > 1 else ""

        if action in ("l", "list"):
            list_tasks(tasks)
        elif action in ("a", "add"):
            if not arg:
                arg = input("Task text: ").strip()
            add_task(tasks, arg)
            tasks = load_tasks()
        elif action in ("r", "remove"):
            if not arg:
                arg = input("Task number to remove: ").strip()
            remove_task(tasks, arg)
            tasks = load_tasks()
        elif action in ("d", "done"):
            if not arg:
                arg = input("Task number to mark done: ").strip()
            mark_done(tasks, arg, done=True)
            tasks = load_tasks()
        elif action in ("u", "undo"):
            if not arg:
                arg = input("Task number to mark not done: ").strip()
            mark_done(tasks, arg, done=False)
            tasks = load_tasks()
        elif action in ("c", "clear"):
            confirm = input("Are you sure you want to remove ALL tasks? (y/N): ").strip().lower()
            if confirm == "y":
                clear_tasks()
                tasks = []
            else:
                print("Canceled.")
        elif action in ("h", "help"):
            show_help()
        elif action in ("q", "quit", "exit"):
            print("Bye!")
            break
        else:
            print("Unknown command. Type 'h' or 'help' to see commands.")


if __name__ == "__main__":
    main()
