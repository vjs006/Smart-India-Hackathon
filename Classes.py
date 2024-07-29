import pymongo, numpy as np
from datetime import datetime
from datetime import timedelta as dt

# import json
client = pymongo.MongoClient(
    "mongodb+srv://ams1234:ams1234@cluster0.ph4hzjn.mongodb.net/"
)
db = client["AMS-Test"]


class Doctor:
    def __init__(self, id=None):
        if id == None:
            print("\nCreating and Getting Doctor Details:\n")
            self.doctor_id = self.retrieve_last_added_id() + 1
            name = input("Enter your name: ")
            try:
                self.first_name = name.split(" ")[0]
                self.last_name = name.split(" ")[1]
            except:
                self.first_name = name
                self.last_name = None
            self.specialization = input("Enter specialization: ")
            col_spl = db["Specialization"]
           
            spl_document = col_spl.find_one({"name": self.specialization})
            if spl_document:
                spl_document["doctors"].append({"doctor_id": self.doctor_id, "name": self.first_name + ' ' + self.last_name})
                filter_criteria = {"name": self.specialization}
                col_spl.replace_one(filter_criteria, spl_document)
            else:
                spl = Specialization()
                spl.insert_data()
               
            self.email = input("Enter your email: ")
            self.phone = input("Enter your phone-number(telephone): ")
            print("Enter your office hours: ")
            self.mn_hr = input("Enter your working hours on Monday: ")
            self.tue_hr = input("Enter your working hours on Tuesday: ")
            self.wed_hr = input("Enter your working hours on Wednesday: ")
            self.thurs_hr = input("Enter your working hours on Thursday: ")
            self.fri_hr = input("Enter your working hours on Friday: ")
            self.sat_hr = input("Enter your working hours on Saturay: ")
            self.sun_hr = input("Enter your working hours on Sunday: ")
            langs = input(
                "Enter the languages that you are proficient in (separated by a comma): "
            )
            l = langs.split(",")
            self.languages = np.array(l)
            self.location = {}
            self.location["latitude"], self.location["longitude"] = 15.499493, -83.2829
            self.work_schedule = {
                "monday": self.mn_hr,
                "tuesday": self.tue_hr,
                "wednesday": self.wed_hr,
                "thursday": self.thurs_hr,
                "friday": self.fri_hr,
                "saturday": self.sat_hr,
                "sunday": self.sun_hr,
            }
            self.time_slots = self.create_time_slots()
            self.status = False
           
        else:
            self.doctor_id = id
            doctor_document = db["Doctor"].find_one({"doctor_id": self.doctor_id})
            if doctor_document:
                # print(doctor_document)
                self.first_name = doctor_document["first_name"]
                self.last_name = doctor_document["last_name"]
                self.specialization = doctor_document["specialization"]
                self.email = doctor_document["email"]
                self.phone = doctor_document["phone"]
                timings = doctor_document["office_hours"]
                self.office_hours = timings
                self.mn_hr = timings["monday"]
                self.tue_hr = timings["tuesday"]
                self.wed_hr = timings["wednesday"]
                self.thurs_hr = timings["thursday"]
                self.fri_hr = timings["friday"]
                self.sat_hr = timings["saturday"]
                self.sun_hr = timings["sunday"]
                self.languages = doctor_document["languages"]
                self.location = doctor_document["location"]
                self.status = doctor_document["status"]

    def retrieve_last_added_id(self):
        col = db["Doctor"]
        doc_list = list(col.find({}))
        # print(doc_list)
        return doc_list[-1]["doctor_id"]

    # Function to create time slots
    def create_time_slots(self):
        slot_duration = dt(minutes=45)
        break_duration = dt(minutes=15)
        lunch_duration = dt(hours=1)
        time_slots = {}
        for day, timings in self.work_schedule.items():
            # Parse the start and end times from the string
            start_time_str, end_time_str = timings.split(" - ")
            start_time = datetime.strptime(start_time_str, "%I:%M %p")
            end_time = datetime.strptime(end_time_str, "%I:%M %p")

            # Initialize the current time as the start time
            current_time = start_time

            # Initialize a list for slots on this day
            day_time_slots = {}

            # Loop to create time slots
            while current_time + slot_duration <= end_time:
                # Check if it's lunchtime
                if current_time == datetime.strptime("12:00 PM", "%I:%M %p"):
                    current_time += lunch_duration
                    continue

                # Create a time slot
                slot_start = current_time.strftime("%I:%M %p")
                current_time += slot_duration
                slot_end = current_time.strftime("%I:%M %p")

                # Add the time slot to the day and None by deafult.
                day_time_slots[f"{slot_start} - {slot_end}"] = None

                # Add break time after the slot
                current_time += break_duration

            # Store the time slots for this day
            time_slots[day] = day_time_slots

        # Return the generated time slots
        return time_slots

    def insert_data(self):
        collection = db["Doctor"]
        data_to_insert = {
            "doctor_id": self.doctor_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specialization": self.specialization,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "office_hours": self.time_slots,
            "languages": self.languages.tolist(),
            "status": self.status,
        }
        inserted_document = collection.insert_one(data_to_insert)

    """
    def update_status(self):
        # if action.trigger() naa -> func call made
            col = db["Doctor"]
            query = {"doctor_id":input_doctor_id*}
            doc_to_update = col.find_one(query)
            if doc_to_update:
                status = doc_to_upate["status"]
                if status == True:
                    doc_to_update["status"] = False
                doc_to_update["status"] = True
                col.update_one(query,{"$set":{"status":doc_to_update["status"]}})
    """


class Patient:
    def __init__(self, id=None):
        if id == None:
            print("\nCreating and Getting Patient Details:\n")
            name = input("Enter Patient Name: ")
            try:
                self.first_name = name.split()[0]
                self.last_name = name.split()[1]
            except:
                self.first_name = name.split()[0]
                self.last_name = None
            self.patient_id = self.retrieve_last_added_id() + 1
            self.dob = input("Enter Your DOB: ")
            self.past_history = []
            hist_patient = {}
            while True:
                ch = input("Past history(y/n): ")
                if ch == "y":
                    hist_patient["date"] = input("\tEnter Date: ")
                    hist_patient["condition"] = input("\tEnter condition: ")
                    hist_patient["treatment"] = input(
                        "\tEnter Treatment measure used: "
                    )
                    self.past_history.append(hist_patient)
                    hist_patient = {}
                elif ch == "n":
                    break
                else:
                    print("Invalid choice!")
            self.location = {}
            self.location["latitude"] = 12.78654
            self.location["longitude"] = 80.214442
            self.phone_no = input("Enter your number:")
        else:
            self.patient_id = id
            patient_document = db["Patient"].find_one({"patient_id": self.patient_id})
            if patient_document:
                self.first_name = patient_document["first_name"]
                self.last_name = patient_document["last_name"]
                self.dob = patient_document["dob"]
                self.past_history = patient_document["past_history"]
                self.location = patient_document["location"]
                self.phone_no = patient_document["phone_no"]

    def retrieve_last_added_id(self):
        col = db["Patient"]
        doc_list = list(col.find({}))
        # print(doc_list)
        last_id = int(doc_list[-1]["patient_id"][1:])
        return last_id

    def insert_data(self):
        collection = db["Patient"]
        data_to_insert = {
            "patient_id": "P" + str(self.patient_id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob,
            "past_history": self.past_history,
            "location": self.location,
            "phone_no": self.phone_no
        }
        inserted_document = collection.insert_one(data_to_insert)

class Specialization:
    def __init__(self, id=None):
        if id == None:
            print("\nCreating and Getting Specialization Details:\n")
           
            self.specialization_id = "SP" + str(int(self.retrieve_last_added_id()) + 1)
            self.specialization_name = input("\tEnter name: ")
            self.description =  input("\tEnter Description: ")
            self.doctors = []
            doctor = {}
            while True:
                ch = input("Enter Doctor?(y/n): ")
                if ch == "y":
                    doctor["doctor_id"] = input("\tEnter Doc ID: ")
                    doctor["name"] = input("\tEnter Doctor Name: ")
                    self.doctors.append(doctor)
                    doctor = {}
                elif ch == "n":
                    break
                else:
                    print("Invalid choice!")
           
        else:
            self.specialization_id = id
            special_document = db["Specialization"].find_one({"specialization_id": self.specialization_id})
            if special_document:
                self.specialization_name = special_document["name"]
                self.description =  special_document["description"]
                self.doctors = special_document["doctors"]
               
    def retrieve_last_added_id(self):
        col = db["Specialization"]
        doc_list = list(col.find({}))
        # print(doc_list)
        last_id = (doc_list[-1]["specialization_id"][2:])
        return last_id

    def insert_data(self):
        collection = db["Specialization"]
        data_to_insert = {
            "specialization_id": str(self.specialization_id),
            "name": self.specialization_name,
            "description": self.description,
            "doctors": self.doctors
        }
        inserted_document = collection.insert_one(data_to_insert)

'''
if __name__ == "__main__":
    while True:
        ch = int(
            input(
                "\nMenu:\n  1 - New Doctor\n  2 - New Patient\n  3 - Display existing Doctor\n  4 - Display existing Patient\n  5 - Exit\nEnter Choice: "
            )
        )
        if ch == 1:
            doctor = Doctor()
            print()
            print(f"First Name: {doctor.first_name}")
            print(f"Last Name: {doctor.last_name}")
            print(f"ID: {doctor.id}")
            print(f"Specialization: {doctor.specialization}")
            print(f"Email: {doctor.email}")
            print(f"Phone: {doctor.phone}")
            print(f"Monday Office Hours: {doctor.mn_hr}")
            print(f"Tuesday Office Hours: {doctor.tue_hr}")
            print(f"Wednesday Office Hours: {doctor.wed_hr}")
            print(f"Thursday Office Hours: {doctor.thurs_hr}")
            print(f"Friday Office Hours: {doctor.fri_hr}")
            print(f"Saturday Office Hours: {doctor.sat_hr}")
            print(f"Sunday Office Hours: {doctor.sun_hr}")
            print(f"Languages: {doctor.languages}")

            doctor.insert_data()

        elif ch == 2:
            patient = Patient()

            print(f"First Name: {patient.first_name}")
            print(f"Last Name: {patient.last_name}")
            print(f"Date of Birth: {patient.dob}")

            print("Past History:")
            for history in patient.past_history:
                print(
                    f"\tDate: {history['date']}, Condition: {history['condition']}, Treatment: {history['treatment']}"
                )

            print(
                f"Location - Latitude: {patient.location['latitude']}, Longitude: {patient.location['longitude']}"
            )

            patient.insert_data()
            
        elif ch == 6:
            spl = Specialization()
            spl.insert_data()
            print("\nSpecialization Details:")
            print("Specialization ID:", spl.specialization_id)
            print("Name:", spl.specialization_name)
            print("Description:", spl.description)
            print("Doctors:")
            for doctor in spl.doctors:
                print("\tDoctor ID:", doctor.get("doctor_id"))
                print("\tDoctor Name:", doctor.get("name"))

        elif ch == 3:
            # Doctor Details
            db = client["AMS-Test"]
            col = db["Doctor"]
            doctor_doc_list = list(col.find({}))
            for i in doctor_doc_list:
                for j in i:
                    print(j, ":", i[j], end="\n")
                print()

        elif ch == 4:
            # Patient details
            db = client["AMS-Test"]
            col = db["Patient"]
            pat_doc_list = list(col.find({}))

            for i in pat_doc_list:
                for j in i:
                    print(j, ":", i[j], end="\n")
                print()

        elif ch == 5:
            print("Exit Successful!!")
            break

        else:
            print("Invalid Input!!")
'''