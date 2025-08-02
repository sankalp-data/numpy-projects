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

        print(f"Average Marks of {roll_no} = {np.mean(list_of_marks):.2f}")
        print(f"Median Marks of {roll_no} = {np.median(list_of_marks):.2f}")

    '''UPCOMING FEATURE'''
    # def sub_wise_analytics(self):
    #     data = loading_file()

    #     if not data:
    #         print("Nothing")




        











    
