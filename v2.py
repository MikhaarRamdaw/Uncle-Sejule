import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# Initialize session state for tasks and default time
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

if "default_time" not in st.session_state:
    st.session_state["default_time"] = time(9, 0)  # Default to 9:00 AM

# Title
st.title("AI Task Scheduler")
st.write("Input your tasks, and the scheduler will create a weekly plan for you.")

# Task Input
st.header("Add a Task")
task_name = st.text_input("Task Name", placeholder="E.g., Complete project report")
deadline = st.date_input("Deadline", min_value=datetime.today())
start_time = st.time_input("Start Time", value=st.session_state["default_time"])
duration = st.number_input("Duration (hours)", min_value=1, max_value=8, step=1)
priority = st.selectbox("Priority", ["High", "Medium", "Low"])
available_time = st.number_input("Daily Available Hours (optional)", min_value=1, value=8)

# Add task button
if st.button("Add Task"):
    st.session_state["tasks"].append({
        "name": task_name,
        "deadline": deadline,
        "start_time": start_time,
        "duration": duration,
        "priority": priority
    })
    st.success(f"Task '{task_name}' added!")

# Display task list
if st.session_state["tasks"]:
    st.header("Task List")
    tasks_df = pd.DataFrame(st.session_state["tasks"])
    st.dataframe(tasks_df)

# Generate Schedule
if st.button("Generate Schedule"):
    tasks = sorted(
        st.session_state["tasks"], 
        key=lambda x: (x["priority"], x["deadline"])
    )
    
    # Weekly schedule initialization
    today = datetime.today()
    week_dates = [(today + timedelta(days=i)) for i in range(7)]
    schedule = {date.strftime("%A, %d %b"): [] for date in week_dates}
    
    daily_limit = available_time

    # Assign tasks to the schedule
    for task in tasks:
        task_deadline = datetime.combine(task["deadline"], task["start_time"])
        task_duration = task["duration"]
        for day_date in week_dates:
            day_name = day_date.strftime("%A, %d %b")
            if task_deadline.date() >= day_date.date() and task_duration > 0:
                hours_to_assign = min(task_duration, daily_limit)
                schedule[day_name].append(f"{task['name']} ({hours_to_assign} hrs)")
                task_duration -= hours_to_assign
                if task_duration <= 0:
                    break

    # Display the weekly schedule in a calendar view
    st.header("Weekly Schedule")
    columns = st.columns(7)  # 7 columns for 7 days
    for col, day in zip(columns, schedule.keys()):
        with col:
            st.subheader(day)
            if schedule[day]:
                for task in schedule[day]:
                    st.write(task)
            else:
                st.write("No tasks assigned.")
