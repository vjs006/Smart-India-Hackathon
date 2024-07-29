'''from Classes import Doctor, Patient, Specialization
import pymongo, datetime, calendar, math, speech_recognition as sr, numpy as np, nltk
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta as dt
from deep_translator import GoogleTranslator
from nltk.tokenize import word_tokenize
from nltk import pos_tag 

client = pymongo.MongoClient(
    "mongodb+srv://ams1234:ams1234@cluster0.ph4hzjn.mongodb.net/"
)
db = client["AMS-Test"]


class Appointment(Doctor, Patient):
    def __init__(self) -> None:
''''''doc_id = int(input("Enter doctor ID:"))
        doctor = Doctor(doc_id)
        pat_id = input("Enter patient ID:")
        patient = Patient(pat_id)
        self.app_id = self.retrieve_last_app_id()
        self.patient_id = patient.patient_id
        self.doctor_id = doctor.doctor_id
        self.date = datetime.date.today()
        self.day = calendar.day_name[datetime.date.today().weekday()].lower()
        self.status, self.symptoms, self.doctor_location = None, None, doctor.location
        self.bill_info = {}'''
'''
        self.day = calendar.day_name[datetime.date.today().weekday()].lower()
        self.spl_id = None

    def retrieve_last_app_id(self):
        col = db["Appointments"]
        doc_list = list(col.find({}))
        last_id = int(doc_list[-1]["appointment_id"][1:])
        current_id = "A" + str(last_id+1)
        return current_id
    
    def get_symp_decide_spltn(self):
        s = Speech()
        ''''''keywords = s.keywords
        condition = [{"keywords":{"$in":keyword}} for keyword in keywords]
        query = {"$or":condition} ''''''
        print(s.keywords)
        query = {'keywords':{'$in':s.keywords}}
        matched_col = db["Specialization"].find(query)
        best_match_count, best_match_doc = 0, None
        #print(matched_col) 
        for doc in matched_col:
            best_match = sum(keyword in doc.get("keywords") for keyword in s.keywords)
            if best_match > best_match_count:
                best_match_count = best_match
                best_match_doc = doc 
        if best_match_doc:
            self.spl_id = best_match_doc.get("specialization_id")
        else:
            pass
    
    def get_specialization_doctors(self, id):
        col = db["Doctor"]
        col2 = db["Specialization"]
        doc_list2 = list(col2.find({}))
       
        doctors = []
        for i in doc_list2:
            if i["specialization_id"] == id:
                doctors = i["doctors"]

        specific_doctors = []
        for i in doctors:
            specific_doctors.append(col.find_one({"doctor_id": i}))
               
        return doctors
    
    def get_available_doctors(self):
        col = db["Doctor"]
        spl_docs = self.get_specialization_doctors(self.spl_id)
        #print(spl_docs)
        avl_docs = []
        for i in spl_docs:
            doc = col.find_one({"doctor_id": int(i["doctor_id"])})
            if self.time_slot(i["doctor_id"]) != [] and doc["status"] == "true":
                avl_docs.append(i)
        # print(avl_docs)
        return avl_docs
    
    def fix_doctor(self, patient_id):
        dist_of_doctors = []
        #Patient in question //Nithish's part
       
        avl_docs = self.get_available_doctors(self.spl_id)
        patient = Patient(patient_id)
        for i in avl_docs:
            temp = []
            temp.append(Doctor(int(i["doctor_id"])))
            dist_of_doctors.append(temp)
        for i in dist_of_doctors:
            i.append(self.haversine(i[0].location, patient.location))
        dist_of_doctors = self.quicksort(dist_of_doctors)

        for i in dist_of_doctors:
            print(i[0].first_name, i[0].last_name , ":", i[1])
   
         
    def time_slot(self, id):
        #print(id, type(id))
        available_slots = []
        doctor_document = db["Doctor"].find_one({"doctor_id": int(id)})
        #print(doctor_document)
        office_hours = doctor_document["office_hours"][self.day]
        for time_slot, status in office_hours.items():
            if status is None:
                available_slots.append(time_slot)
        return available_slots


    def get_address_from_lat_lng(self, latitude, longitude):
        # Initialize the Nominatim geocoder
        geolocator = Nominatim(user_agent="reverse_geocoding_example")

        try:
            location = geolocator.reverse((latitude, longitude), language="en")
           
            if location:
                return location.address
            else:
                return "Address not found"

        except Exception as e:
            return f"Error: {str(e)}"

    def haversine(self, doc_Loc, pat_Loc):
        earth_radius = 6371000  # Approximate value for average radius
       
        # Convert latitudes and longitudes from degrees to radians
        lat1 = math.radians(doc_Loc["latitude"])
        lon1 = math.radians(doc_Loc["longitude"])
        lat2 = math.radians(pat_Loc["latitude"])
        lon2 = math.radians(pat_Loc["longitude"])
       
        # Calculate differences in latitude, longitude, and elevation
        dlat = lat2 - lat1
        dlon = lon2 - lon1
       
        # Calculate the 3D distance using the Haversine formula
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c
       
        return "{:.{}f}".format(distance/1000, 4)

    def quicksort(self, arr):
        if len(arr) <= 1:
            return arr  

        pivot = arr[len(arr) // 2][1]  # Choose the middle element as the pivot
        left = [x for x in arr if x[1] < pivot]
        middle = [x for x in arr if x[1] == pivot]
        right = [x for x in arr if x[1] > pivot]

        return self.quicksort(left) + middle + self.quicksort(right)
    
'''
import nltk
nltk.download()
