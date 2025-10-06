import os
import requests
import json

nutritionix_app_id = os.environ.get("NUTRITIONIX_APP_ID")
nutritionix_api_key = os.environ.get("NUTRITIONIX_API_KEY")

exercise_text = input("Tell me which exercises you did: ")
nutritionix_headers = { "x-app-id": nutritionix_app_id, "x-app-key": nutritionix_api_key }
nutritionix_body = { "query": exercise_text }
response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise", headers=nutritionix_headers, json=nutritionix_body)
response.raise_for_status()
print(json.dumps(response.json(), indent=4))
workout = response.json()
for exercise in workout['exercises']:
    if exercise['user_input'] in ["ran", "run"]:
        duration = exercise['duration_min']
        calories = exercise['nf_calories']
        print("you ran!")

# add a new row to the exercise sheet using sheety.co
sheety_headers = { }
sheety_body = { }
response = requests.post(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/projectWorkoutStats/sheet1")
response.raise_for_status()