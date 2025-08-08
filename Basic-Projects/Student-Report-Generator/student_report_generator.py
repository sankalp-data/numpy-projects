
import numpy as np
import json
from pprint import pprint

filepath = r"Basic-Projects\report_file.json"

def open_report_file(file):
    '''Save the updated student data back to the JSON file'''
    with open(filepath, "w") as f:
        json.dump(file, f, indent=4)

def loading_file():
    '''Load data from existing JSON or return empty dict if file doesn't exist or is invalid'''
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

class Student:
    def taking_input(self, name, roll_no):
        data = loading_file()

        # Avoid overwriting existing student data with same roll number
        student_key = f"Details of {roll_no}"
        if student_key in data:
            print(f"⚠️ Roll number {roll_no} already exists. Overwriting previous data.")
        
        data[student_key] = {
            "Name": name,
            "Performance": {}
        }

        try:
            total_sub = int(input("Total Subjects: ").strip())
        except ValueError:
            print("❌ Invalid Input!")
            return

        for _ in range(total_sub):
            try:
                sub_name = input("Subject: ").strip()
                marks = float(input("Marks: ").strip())
                data[student_key]["Performance"][sub_name] = marks
            except ValueError:
                print("❌ Invalid Input! Skipping subject...")
                continue

        open_report_file(data)
        print("✅ Student data has been successfully uploaded!")
        pprint(data)


    def individual_student_stat(self,roll_no):
        '''Display statistics for an individual student.'''


        data = loading_file()

        if not data:
            print("Nothing in report file.")
            return

        if f"Details of {roll_no}" not in data.keys():
            print("No Such Student!")
            return
        
        list_of_marks = []
        for marks in data[f"Details of {roll_no}"]["Performance"].values():
            list_of_marks.append(marks)

        print(f"Average Marks of roll number {roll_no} = {np.mean(list_of_marks):.2f}")
        print(f"Median Marks of roll number {roll_no} = {np.median(list_of_marks):.2f}")
        print(f"Percentage of roll number {roll_no} = {(np.sum(list_of_marks)/(len(list_of_marks)*100))*100:.2f}%")

    def comparing_students(self):
        '''Compare performance across multiple students.'''


        data = loading_file()
        if not data:
            print("Nothing in report file.")
            return

        try:
            total = int(input("How many students do you want to compare? ").strip())
        except ValueError:
            print("❌ Invalid number input.")
            return

        stats = {}

        for _ in range(total):
            try:
                roll = input("Enter roll number: ").strip()
                student_key = f"Details of {roll}"

                if student_key not in data:
                    print(f"⚠️ Student with roll number {roll} not found.")
                    continue

                name = data[student_key]["Name"]
                marks = list(data[student_key]["Performance"].values())
                marks_array = np.array(marks)

                stats[roll] = {
                    "Name": name,
                    "Average": np.mean(marks_array),
                    "Percentage": (np.sum(marks_array) / (len(marks_array) * 100)) * 100
                }
            except Exception as e:
                print(f"⚠️ Error while processing roll {roll}: {e}")
                continue

        if not stats:
            print("❌ No valid students to compare.")
            return

        print("\n📊 Comparison Report:")
        for roll, info in stats.items():
            print(f"Roll: {roll} | Name: {info['Name']} | Avg: {info['Average']:.2f} | %: {info['Percentage']:.2f}")

        #Print top performer
        top = max(stats.items(), key=lambda x: x[1]["Average"])
        print(f"\n🏆 Top Performer: {top[1]['Name']} (Roll Number {top[0]}) with Average {top[1]['Average']:.2f}")

    
    def sub_wise_analysis(self):
        '''Display subject-wise performance analysis.'''

        data = loading_file()
        if not data:
            print("Nothing in report file.")
            return
        
        print("Subjects list:")
        sub_lst = []
        # for content in data:
        for val in data.values():
            for sub in val["Performance"].keys():
                if sub not in sub_lst:
                    sub_lst.append(sub)
                else:
                    continue
        pprint(sub_lst)

        print("\n📊 Subject-Wise Analysis:")
        for subject in sub_lst:
            marks = []

            # Collect marks for the current subject from all students
            for student in data.values():
                if subject in student["Performance"]:
                    marks.append(student["Performance"][subject])

            if marks:
                print(f"\n📘 Subject: {subject}")
                print(f"Total Students: {len(marks)}")
                print(f"Average Marks: {np.mean(marks):.2f}")
                print(f"Highest Marks: {np.max(marks):.2f}")
                print(f"Lowest Marks: {np.min(marks):.2f}")
            else:
                print(f"\n📘 Subject: {subject}")
                print("No data available.")

    def update_or_delete(self):
        '''Delete a student's record or update existing student's marks'''

        data = loading_file()

        if not data:
            print("Nothing in report file.")
            return

        action = input("Enter 1 for Updating existing student's marks\nEnter 2 for Deleting a Student's Record\n>>>> ").strip()

        if action not in ["1", "2"]:
            print("❌ Please reply with 1 or 2.")
            return

        roll_no = input("Enter Roll Number: ").strip()
        student_key = f"Details of {roll_no}"

        if student_key not in data:
            print("❌ No such student found.")
            return

        if action == "2":
            # Delete student record
            confirm = input(f"Are you sure you want to delete record of roll number {roll_no}? (yes/no): ").strip().lower()
            if confirm == "yes":
                del data[student_key]
                open_report_file(data)
                print("✅ Student record deleted.")
            
        
            else:
                print("Cancelled.")
            return

        # === Update marks section ===
        while True:
            update_choice = input("\nEnter 1 to edit subject marks\nEnter 2 to add new subjects\nEnter 3 to quit\n>>>> ").strip()

            if update_choice == "1":
                subjects = data[student_key]["Performance"]
                if not subjects:
                    print("This student has no subjects recorded yet.")
                    continue
                print("\n📘 Current Subjects:")
                for sub in subjects:
                    print(f"- {sub}: {subjects[sub]}")

                sub_to_edit = input("Enter subject name to update: ").strip()
                if sub_to_edit in subjects:
                    try:
                        new_marks = float(input(f"Enter new marks for {sub_to_edit}: ").strip())
                        subjects[sub_to_edit] = new_marks
                        print(f"✅ Updated marks for {sub_to_edit}.")
                    except ValueError:
                        print("❌ Invalid marks entered.")
                else:
                    print("❌ Subject not found.")

            elif update_choice == "2":
                try:
                    sub_name = input("Enter new subject name: ").strip()
                    if sub_name in data[student_key]["Performance"]:
                        print("⚠️ Subject already exists. Use option 1 to update it.")
                        continue
                    marks = float(input(f"Enter marks for {sub_name}: ").strip())
                    data[student_key]["Performance"][sub_name] = marks
                    print(f"✅ Added subject {sub_name}.")
                except ValueError:
                    print("❌ Invalid marks entered.")

            elif update_choice == "3":
                break
            else:
                print("❌ Please enter a valid choice (1, 2, or 3).")

        # Save changes after update
        open_report_file(data)
        print("✅ Student record has been updated.")

    