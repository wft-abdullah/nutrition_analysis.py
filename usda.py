import requests
import json

API_KEY = "kcqwL92mqQmEgSE9d8kXnJ0iSX2tRx9wHXPRfWWs"


def search_food(query):
    """Search for a food item in USDA FoodData Central."""
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 1  # Get only the top result
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if data['foods']:
        return data['foods'][0]  # Return the top search result
    return None


def get_food_details(fdc_id):
    """Fetch nutrient details for a specific food by FDC ID."""
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    crop = "broccoli"  # Change this to any crop you want
    print(f"Searching for '{crop}'...")
    search_result = search_food(crop)

    if search_result:
        fdc_id = search_result['fdcId']
        print(f"Found '{crop}' with FDC ID: {fdc_id}")

        print(f"Fetching details for FDC ID {fdc_id}...")
        details = get_food_details(fdc_id)

        # Print the full details
        print(json.dumps(details, indent=2))  # Pretty-print the JSON response

        # Extract and display nutrient info
        print("\n--- Nutrient Information ---")
        for nutrient in details.get("foodNutrients", []):
            print(
                f"{nutrient.get('nutrientName', 'Unknown')}: {nutrient.get('value', 'N/A')} {nutrient.get('unitName', '')}")
    else:
        print(f"'{crop}' not found in the USDA database.")
