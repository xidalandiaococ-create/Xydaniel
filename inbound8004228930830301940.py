from datetime import date, datetime

tasks = []
next_task_id = 1

subjects = [
    "GEN 001",
    "GEN 002",
    "GEN 006",
    "ITE 260",
    "ITE 366",
    "MAT 152",
    "NST 021",
    "PED 030"
]

priorities = ["High", "Medium", "Low"]


def get_deadline():
    today = date.today()

    while True:
        deadline_str = input(
            f"Deadline (YYYY-MM-DD, must be >= {today}): "
        ).strip()

        try:
            deadline_date = datetime.strptime(
                deadline_str, "%Y-%m-%d"
            ).date()

            if deadline_date < today:
                print("Deadline cannot be in the past.")
            else:
                return deadline_str

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD.")


def print_table(task_list, title="TASK VIEW - TABLE"):
    # Sort by earliest deadline first (year-month-day).
    task_list = sorted(
        task_list,
        key=lambda task: datetime.strptime(task["deadline"], "%Y-%m-%d").date()
    )
    print(f"\n--- {title} (EARLIEST DEADLINE FIRST) ---")

    if not task_list:
        print("No tasks recorded.")
        return

    headers = [
        "ID", "TASK NAME", "SUBJECT",
        "DATE", "PRIORITY", "STATUS"
    ]

    rows = [
        [
            str(task["id"]),
            task["name"],
            task["subject"],
            task["deadline"],
            task["priority"],
            task["status"]
        ]
        for task in task_list
    ]

    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]

    separator = "+-" + "-+-".join("-" * w for w in widths) + "-+"

    print(separator)
    print(
        "| " + " | ".join(
            headers[i].ljust(widths[i])
            for i in range(len(headers))
        ) + " |"
    )
    print(separator)

    for row in rows:
        print(
            "| " + " | ".join(
                row[i].ljust(widths[i])
                for i in range(len(row))
            ) + " |"
        )

    print(separator)


def add_task():
    global next_task_id

    print("\n--- ADD TASK ---")

    while True:
        name = input("Task Name: ").strip()

        if name:
            break

        print("Task name cannot be empty.")

    print("\nAvailable Subjects:")
    for i, subject_name in enumerate(subjects, 1):
        print(f"{i}. {subject_name}")

    while True:
        choice = input("Select Subject (1-8): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(subjects):
            subject = subjects[int(choice) - 1]
            break

        print("Invalid choice! Please select 1-8.")

    deadline = get_deadline()

    while True:
        priority = input(
            "Priority (High/Medium/Low): "
        ).strip().capitalize()

        if priority in priorities:
            break

        print("Invalid priority! Enter High, Medium, or Low.")

    task = {
        "id": next_task_id,
        "name": name,
        "subject": subject,
        "deadline": deadline,
        "priority": priority,
        "status": "Pending"
    }

    tasks.append(task)
    next_task_id += 1

    print("\nTask added successfully!")
    print_table([task], "ADDED TASK - TABLE")


def view_tasks():
    print_table(tasks, "TASK VIEW - TABLE")


def pending_tasks():
    print("\n--- PENDING TASKS / UPDATE TASK ---")

    pending = [
        task for task in tasks
        if task["status"] == "Pending"
    ]

    pending.sort(key=lambda task: task["deadline"])

    if not pending:
        print("No pending tasks available.")
        return

    print_table(pending, "PENDING TASKS")

    try:
        task_id = int(input("\nEnter Task ID to update (0 to cancel): "))
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return

    if task_id == 0:
        return

    task = next(
        (t for t in pending if t["id"] == task_id),
        None
    )

    if task is None:
        print("Task ID not found in pending tasks.")
        return

    print("\nPress Enter to keep the current value.")

    new_name = input(
        f"Task Name [{task['name']}]: "
    ).strip()

    if new_name:
        task["name"] = new_name

    while True:
        new_date = input(
            f"Deadline [{task['deadline']}] (YYYY-MM-DD): "
        ).strip()

        if not new_date:
            break

        try:
            date_value = datetime.strptime(
                new_date, "%Y-%m-%d"
            ).date()

            if date_value < date.today():
                print("Deadline cannot be in the past.")
                continue

            task["deadline"] = new_date
            break

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD.")

    while True:
        new_priority = input(
            f"Priority [{task['priority']}] (High/Medium/Low): "
        ).strip().capitalize()

        if not new_priority:
            break

        if new_priority in priorities:
            task["priority"] = new_priority
            break

        print("Invalid priority! Enter High, Medium, or Low.")

    print("\nTask updated successfully!")

    tasks.sort(key=lambda task: task["deadline"])

    print_table(tasks, "UPDATED TASK VIEW - TABLE")


    if task is None:
        print("Task ID not found.")
        return

    print("\nCurrent Task Information:")
    print(f"Task Name: {task['name']}")
    print(f"Date:      {task['deadline']}")
    print(f"Priority:  {task['priority']}")

    print("\nPress Enter to keep the current value.")

    # Update task name
    new_name = input(
        f"New Task Name [{task['name']}]: "
    ).strip()

    if new_name:
        task["name"] = new_name

    # Update date
    while True:
        new_date = input(
            f"New Date [{task['deadline']}] (YYYY-MM-DD): "
        ).strip()

        if not new_date:
            break

        try:
            date_value = datetime.strptime(new_date, "%Y-%m-%d").date()

            if date_value < date.today():
                print("Date cannot be in the past.")
                continue

            task["deadline"] = new_date
            break

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD.")

    # Update priority
    while True:
        new_priority = input(
            f"New Priority [{task['priority']}] (High/Medium/Low): "
        ).strip().capitalize()

        if not new_priority:
            break

        if new_priority in priorities:
            task["priority"] = new_priority
            break

        print("Invalid priority! Enter High, Medium, or Low.")

    print("\nTask updated successfully!")
    print_table([task], "UPDATED TASK - TABLE")

def search_task():
    print("\n--- SEARCH TASK ---")

    keyword = input("Enter task name to search: ").strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    found_tasks = [
        task for task in tasks
        if keyword in task["name"].lower()
    ]

    if not found_tasks:
        print("No matching task found.")
        return

    found_tasks.sort(key=lambda task: task["deadline"])
    print_table(found_tasks, "SEARCH RESULTS")

def mark_task_as_completed():
    """Mark a selected pending task as completed."""
    print("\n--- MARK TASK AS COMPLETED ---")

    if not tasks:
        print("No tasks available. Please add a task first.")
        return

    print_table(tasks, "SELECT A TASK TO COMPLETE")

    try:
        task_id = int(input("\nEnter Task ID to mark as completed: ").strip())
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return

    task = next((item for item in tasks if item["id"] == task_id), None)

    if task is None:
        print("Task ID not found.")
        return

    if task["status"] == "Completed":
        print(f'Task "{task["name"]}" is already completed.')
        return

    task["status"] = "Completed"
    print(f'\nTask "{task["name"]}" marked as Completed successfully!')
    print_table(tasks, "UPDATED TASK VIEW - TABLE")


def main():
    while True:
        print("\n===== TASK MANAGER =====")
        print("1. Add Task")
        print("2. Task View Table")
        print("3. Pending Task / Update Task")
        print("4. Search Task")
        print("5. Mark Task as Completed")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            add_task()

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            pending_tasks()

        elif choice == "4":
            search_task()

        elif choice == "5":
            mark_task_as_completed()

        elif choice == "6":
            print("Exiting Task Manager. Goodbye!")
            break

        else:
            print("Invalid option! Please choose between 1 and 6.")


if __name__ == "__main__":
    main()