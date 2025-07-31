import numpy as np
import json


class Student:
    def __init__(self, name: str, roll_no: int):
        """Initialize student with name and roll number."""
        self.data = {
            "Name": name,
            "Roll Number": roll_no,
            "Performance": {}
        }

    def sub_marks(self):
        """Input subjects and marks from the user."""
        try:
            sub_count = int(input("Total Subjects: ").strip())
        except ValueError:
            print("❌ Invalid number of subjects.")
            return self.data

        for _ in range(sub_count):
            sub_name = input("Subject: ").strip()
            try:
                marks = float(input("Marks: ").strip())
            except ValueError:
                print("❌ Invalid marks input.")
                continue  # Skip and continue to next subject

            self.data["Performance"][sub_name] = marks

        return self.data