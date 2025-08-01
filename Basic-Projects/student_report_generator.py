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










    
