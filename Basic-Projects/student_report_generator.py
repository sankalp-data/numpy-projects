'''⚠️                IN                  PROGRESS               ⚠️'''

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
        '''Stats of any student'''

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
        '''Comparing different students'''

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

        # Optional: Print top performer
        top = max(stats.items(), key=lambda x: x[1]["Average"])
        print(f"\n🏆 Top Performer: {top[1]['Name']} (Roll Number {top[0]}) with Average {top[1]['Average']:.2f}")

    
    def sub_wise_analysis(self):
        '''Display Subject Wise Analysis'''

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






            











        











    
