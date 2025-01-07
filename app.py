import requests
import json
import pandas as pd
import os

# Constants
API_ID = "a8de8263"
API_KEY = "5f45acbebd82e1d200469b2b14457943"
BASE_URL = "https://api.edamam.com/api/nutrition-details"
SAVE_FILE = "saved_recipes.json"


def analyze_recipe(title, ingredients):
    url = f"{BASE_URL}?app_id={API_ID}&app_key={API_KEY}"
    payload = {
        "title": title,
        "ingr": ingredients
    }

    print("Payload being sent to API:", json.dumps(payload, indent=2))  # Debugging step

    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print("Response content:", response.text)  # Detailed server response
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Error parsing the JSON response")

    return None


def display_nutrition_info(nutrition_data, title):
    """
    Displays nutritional information from the API response in a readable format.
    """
    if not nutrition_data:
        print("No nutrition data to display.")
        return

    print(f"\n=== Nutrition Analysis for {title} ===")
    print(f"Calories: {nutrition_data.get('calories', 'N/A')} kcal")

    total_nutrients = nutrition_data.get("totalNutrients", {})
    for nutrient, details in total_nutrients.items():
        print(f"{details['label']}: {details['quantity']:.2f} {details['unit']}")
    print("===========================")


def save_nutrition_to_excel(nutrition_data, title, ingredients):
    """
    Saves nutritional analysis for each ingredient and overall meal to an Excel file.
    """
    # Parse overall meal nutrition data
    total_nutrients = nutrition_data.get("totalNutrients", {})
    overall_nutrition = {
        "Nutrient": [],
        "Amount": [],
        "Unit": []
    }
    for nutrient, details in total_nutrients.items():
        overall_nutrition["Nutrient"].append(details["label"])
        overall_nutrition["Amount"].append(details["quantity"])
        overall_nutrition["Unit"].append(details["unit"])

    # Create dataframes
    overall_df = pd.DataFrame(overall_nutrition)
    ingredients_df = pd.DataFrame({"Ingredient": ingredients})

    # Excel writer to save to an Excel file with multiple sheets
    excel_filename = f"{title.replace(' ', '_').lower()}_nutrition_analysis.xlsx"
    with pd.ExcelWriter(excel_filename, engine="openpyxl") as writer:
        ingredients_df.to_excel(writer, sheet_name="Ingredients", index=False)
        overall_df.to_excel(writer, sheet_name="Meal Nutrients", index=False)

    print(f"Nutrition analysis saved to {excel_filename}")


def get_user_ingredients():
    """
    Prompts the user to enter ingredients for the recipe, allowing them to edit the list.
    """
    ingredients = []
    print("Enter each ingredient, or type 'done' when finished:")
    while True:
        ingredient = input("Ingredient: ")
        if ingredient.lower() == 'done':
            break
        ingredients.append(ingredient)
    return ingredients


def main():
    while True:
        print("\n=== Recipe Nutrition Analysis ===")
        print("1. Analyze a new recipe")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            title = input("\nEnter the recipe title: ")
            ingredients = get_user_ingredients()
            nutrition_data = analyze_recipe(title, ingredients)

            if nutrition_data:
                display_nutrition_info(nutrition_data, title)

                # Save the analysis to Excel
                save_nutrition_to_excel(nutrition_data, title, ingredients)

        elif choice == '2':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
