import os
import requests
import json
import datetime
import re

nutritionix_app_id = os.environ.get("NUTRITIONIX_APP_ID")
nutritionix_api_key = os.environ.get("NUTRITIONIX_API_KEY")

def extract_miles(text):
    '''extracts how far (in miles) someone has run (or return None)'''
    match = re.search(r'(\d+(?:\.\d+)?)\s*miles?', text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def add_run_info_to_spreadsheet(duration, miles, calories):
    '''adds a new row with run data to sheet1 in google sheets via sheety.co'''
    # add a new row to the exercise sheet using sheety.co
    sheety_body = {
        "sheet1": {
            "date": datetime.datetime.now().strftime("%m/%d/%Y"),
            "machineNumber": "Landstar-3",
            "time (min)": duration,
            "distance": miles_run,
            "min/mile": "unknown",
            "calories": calories
        }
    }
    sheety_response = requests.post(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/projectWorkoutStats/sheet1", json=sheety_body)
    sheety_response.raise_for_status()

# prompt the user for information regarding their last workout
exercise_text = input("Tell me which exercises you did: ")
nutritionix_headers = { "x-app-id": nutritionix_app_id, "x-app-key": nutritionix_api_key }
nutritionix_body = { "query": exercise_text }
response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise", headers=nutritionix_headers, json=nutritionix_body)
response.raise_for_status()
print(json.dumps(response.json(), indent=4))

# if the workout is run related, i want to insert it into my run spreadsheet
# if i ran, collect information about my run, including how far (in miles) i ran for...
was_running_exercise = False
workout = response.json()
for exercise in workout['exercises']:
    if exercise['user_input'] in ["ran", "run"]:
        duration = exercise['duration_min']
        calories = exercise['nf_calories']

        # we've determined i went running; how far did i go?  prompt if it was not originally supplied in exercise_text
        miles_run = extract_miles(exercise_text)
        if miles_run is None:
            miles_run = input("how far did you run for? ")

        was_running_exercise = True
        break

# if i went running, enter the data into the spreadsheet
if was_running_exercise:
    print(f"you went running --> adding data into run spreadsheet")
    add_run_info_to_spreadsheet(duration, miles_run, calories)
    print("successfully added row into spreadsheet")
else:
    print("you didn't go running --> ignoring information")
