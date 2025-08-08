# 📚 Student Report Generator

A Python-based command-line application to manage and analyze student academic performance data.  
This tool stores data in a JSON file, calculates statistics using **NumPy**, and provides multiple options to **add**, **update**, **delete**, and **analyze** student reports.

---

## ✨ Features

- **Add Student Records**  
  Enter student name, roll number, subjects, and marks. Data is stored in a JSON file (`report_file.json`).

- **View Individual Student Statistics**  
  Get **average**, **median**, and **percentage** for a specific student.

- **Compare Students**  
  Compare multiple students’ performance to find the **top performer**.

- **Subject-wise Analysis**  
  See average, highest, and lowest marks for each subject across all students.

- **Update or Delete Records**  
  - Update existing marks
  - Add new subjects
  - Delete a student’s record

---

## 📂 Project Structure

 - Basic-Projects/
 - └── Student-Report-Generator/
 - ├── student_report_generator.py # Main program logic
 - ├── report_file.json # Stores all student data
 - └── README.md # Project documentation


# 🚀 How to Use

1. Clone the repository
 - git clone https://github.com/sankalp-data/numpy-projects.git
 - cd Basic-Projects/Student-Report-Generator

2. Run the script
 - python student_report_generator.py

3. Choose an operation
   > Inside the script, you can call:
   - taking_input(name, roll_no) → Add new student
   - individual_student_stat(roll_no) → View stats of a student
   - comparing_students() → Compare students
   - sub_wise_analysis() → Analyze by subject
   - update_or_delete() → Update or delete a record


# 🔮 Possible Improvements
 - Add a main menu for interactive navigation
 - Export reports to CSV or Excel
 - Add GPA calculation
 - Build a GUI interface