import streamlit as st
import sqlite3
from datetime import datetime
import csv
import subprocess
from PIL import Image
from io import BytesIO
import pandas as pd
import os

# -------------------------------- DATABASE -------------------------------- #
# Initialize database
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Create table for orders if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization TEXT,
    meal_category TEXT,
    selected_meals TEXT,
    number_of_people INTEGER,
    total_cost REAL,
    total_selling_price REAL,
    contribution_margin REAL,
    cost_margin REAL,
    date TEXT,
    day_of_week TEXT
)
""")
conn.commit()

# Predefined meals and categories
MEAL_CATEGORIES = {
    "Complementary Breakfast": [("TOASTED BREAD", 650,), ("AMERICAN PANCAKE", 1547), ( "BOILED YAM", 508), ("FRIED NOODLES", 1201), ("CORN PAP", 468), ("WATERMELON", 200), ("ORANGE FRUIT", 100), ("BAKED BEANS", 895), ("PUFF-PUFF", 200), ("MINI SANDWICH", 300), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("SUNNY SIDE UP", 747), ("CUSTARD", 442), ("MOI-MOI", 1368), ("PAW-PAW", 250), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI", 800), ("ACHA PUDDING", 1100), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE ", 200), ("SWEET POTATO NUGGET", 910), ("FRESH BREAD", 250), ("BOILED POTATO", 910), ("SPAGHETTI JOLLOF", 777), ("OPEN SANDWICH", 2500), ("NIGERIAN PANCAKE", 1000), ("FRIED SWEET POTATO", 400), ("MASA", 400), ("JOLLOF RICE", 800), ("VEGETABLE SAUCE", 1100), ("GERMAN PANCAKE", 1200), ("GOLDEN YAM", 844), ("OAT", 400), ("EGG SANDWICH", 2000), ("YAM CHIPS", 800), ("VEGETABLE NOODLES", 1500), ("FRITATA", 40), ("STIRFRY MACCARONI", 1200), ("BEANS POTTAGE", 800), ("FRITATA", 1841.18), ("INFUSED WATER", 878.60), ("WATERMELON JUICE", 500), ("EWEDU SOUP", 772.38), ("EFORIRO SOUP", 2357.28), ("KUKA SOUP", 798.18), ("WAFFLES", 226.20), ("SLICED CAKE", 130.51), ("FRUITE CAKE", 1804.23), ("TEA BAG", 117,), ("COFFEE", 100), ( "CHOCOLATE", 200), ("HONEY", 50), ("SUGAR", 26), ("CORNFLAKES", 200), ("BROWN SUGAR", 5), ("COCO POPS", 150), ("RICE CRISPIES", 200), ("TOASTED BREAD", 650), ("BUTTER", 50), ("AMERICAN PANCAKE", 1547), ("PANCAKE SYRUP", 100), ("MINI SANDWICHE", 600), ("PUFF-PUFF", 300), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("SWEET POTATO NUGGET", 910), ("FRESH BREAD", 250), ("OPEN SANDWICH", 2500), ("NIGERIAN PANCAKE", 100), ("EGG SANDWICH", 2000), ("YAM CHIPS", 800), ("GOLDEN YAM", 844), ("STIR FRY MACCARONI", 1200), ("FRIED SWEET POTATO", 400), ("MASA", 400), ("CHICKEN ", 1650), ("JOLLOF RICE", 800), ("BOILED POTATO", 910), ("SPAGHETTI JOLLF", 777), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI",800), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("BOILED YAM", 508), ("FRIED NOODLES", 1201), ("EGG SAUCE", 760), ("SCRAMBLED EGG", 770), ("TOMATO SAUCE", 500), ("FISH SAUCE", 2100), ("KIDNEY SAUCE", 2300), ("VEGETABLE SAUCE", 1100), ("BOILED EGG", 200), ("LIVER SAUCE", 2400), ("BEEF STEW", 1400), ("CHICKEN STEW", 1800), ("FRITATA", 50), ("ACHA PUDDING", 1100), ("AKARA", 960), ("OAT", 400), ("BEANS POTTAGE", 800), ("CORN PAP", 468), ("MOI-MOI", 1368), ("CUSTARD", 442), ("MINI SANDWICH", 300), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("SUNNY SIDE UP", 747), ("CUSTARD", 442), ("INFUSED WATER", 50), ("PAW-PAW", 250), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI", 800), ("ACHA PUDDING", 1100), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE ", 200), ("WATERMELON", 50), ("PAW-PAW FRUIT CUT", 250), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE CUT", 250), ("ORANGE", 100), ("BAKED BEANS", 895), ("STEAMED VEG", 50), ("WATER 75CL", 137), ("SAUSAGE", 425), ("GERMAN PANCAKE", 1200), ("GOLDEN YAM", 844), ("CHICKEN PIE", 350), ("APPLE", 400), ("YAM CHIPS", 800), ("VEGETABLE NOODLES", 1500), ("MILK", 115), ("STIRFRY MACCARONI", 1200)],
    "AM Tea Break": [("TEA BAG", 117,), ("COFFEE", 100), ( "CHOCOLATE", 200), ("HONEY", 50), ("SUGAR", 26), ("CORNFLAKES", 200), ("BROWN SUGAR", 5), ("COCO POPS", 150), ("RICE CRISPIES", 200), ("TOASTED BREAD", 650), ("BUTTER", 50), ("AMERICAN PANCAKE", 1547), ("PANCAKE SYRUP", 100), ("MINI SANDWICHE", 600), ("PUFF-PUFF", 300), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("SWEET POTATO NUGGET", 910), ("FRESH BREAD", 250), ("OPEN SANDWICH", 2500), ("NIGERIAN PANCAKE", 100), ("EGG SANDWICH", 2000), ("YAM CHIPS", 800), ("GOLDEN YAM", 844), ("STIR FRY MACCARONI", 1200), ("FRIED SWEET POTATO", 400), ("MASA", 400), ("CHICKEN ", 1650), ("JOLLOF RICE", 800), ("BOILED POTATO", 910), ("SPAGHETTI JOLLF", 777), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI",800), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("BOILED YAM", 508), ("FRIED NOODLES", 1201), ("EGG SAUCE", 760), ("SCRAMBLED EGG", 770), ("TOMATO SAUCE", 500), ("FISH SAUCE", 2100), ("KIDNEY SAUCE", 2300), ("VEGETABLE SAUCE", 1100), ("BOILED EGG", 200), ("LIVER SAUCE", 2400), ("BEEF STEW", 1400), ("CHICKEN STEW", 1800), ("FRITATA", 50), ("ACHA PUDDING", 1100), ("AKARA", 960), ("OAT", 400), ("BEANS POTTAGE", 800), ("CORN PAP", 468), ("MOI-MOI", 1368), ("CUSTARD", 442), ("MINI SANDWICH", 300), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("SUNNY SIDE UP", 747), ("CUSTARD", 442), ("INFUSED WATER", 50), ("PAW-PAW", 250), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI", 800), ("ACHA PUDDING", 1100), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE ", 200), ("WATERMELON", 50), ("PAW-PAW FRUIT CUT", 250), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE CUT", 250), ("ORANGE", 100), ("BAKED BEANS", 895), ("STEAMED VEG", 50), ("WATER 75CL", 137), ("SAUSAGE", 425), ("GERMAN PANCAKE", 1200), ("GOLDEN YAM", 844), ("CHICKEN PIE", 350), ("APPLE", 400), ("YAM CHIPS", 800), ("VEGETABLE NOODLES", 1500), ("MILK", 115), ("STIRFRY MACCARONI", 1200), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("BOILED YAM", 508), ("FRIED NOODLES", 1201), ("EGG SAUCE", 760), ("SCRAMBLED EGG", 770), ("TOMATO SAUCE", 500), ("FISH SAUCE", 2100), ("KIDNEY SAUCE", 2300), ("VEGETABLE SAUCE", 1100), ("BOILED EGG", 200), ("LIVER SAUCE", 2400), ("BEEF STEW", 1400), ("CHICKEN STEW", 1800), ("FRITATA", 50), ("ACHA PUDDING", 1100), ("AKARA", 960), ("OAT", 400), ("BEANS POTTAGE", 800), ("CORN PAP", 468), ("MOI-MOI", 1368), ("CUSTARD", 442), ("MINI SANDWICH", 300), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("SUNNY SIDE UP", 747), ("CUSTARD", 442), ("INFUSED WATER", 50), ("PAW-PAW", 250), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI", 800), ("ACHA PUDDING", 1100), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE ", 200), ("WATERMELON", 50), ("PAW-PAW FRUIT CUT", 250), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE CUT", 250), ("ORANGE", 100), ("BAKED BEANS", 895), ("STEAMED VEG", 50), ("WATER 75CL", 137), ("SAUSAGE", 425), ("GERMAN PANCAKE", 1200), ("GOLDEN YAM", 844), ("CHICKEN PIE", 350), ("APPLE", 400), ("YAM CHIPS", 800), ("VEGETABLE NOODLES", 1500), ("MILK", 115), ("STIRFRY MACCARONI", 1200)],
    "Buffet Lunch": [("COCONUT RICE", 1300), ("CAT FISH", 1900), ("JOLLOF RICE ", 800), ("MACARONI JOLLOF", 800), ("SEMO", 300), ("OHA", 1710), ("EGUSI", 1700), ("MACKEREL FISH", 1900), ("MEXICAN FRIED RICE", 2000), ("SNOW RICE", 900), ("STIRFY PASTA", 1400), ("WHEAT", 400), ("EBA", 300), ("OGBONO", 1800), ("EWEDU", 1500), ("TOMATO STEW", 600), ("BEEF", 1270), ("VEGETABLE SALAD ", 1400), ("CHINESE FRIED RICE  ", 2400), ("PASTA JOLLOF", 777), ("FRESH OKRO", 1310), ("CHICKEN ", 1650), ("STEAMED VEGETABLE", 50), ("ENGLISH FRIED RICE ", 2000), ("SNOW PASTA", 600), ("EFORIRO", 50), ("GREEN VEGETABLE SAUCE", 1400), ("CURRY FRIED RICE", 1900), ("VEGETABLE SOUP", 1600), ("STEAMED VEGETABLE", 50), ("OYSTER SAUCE", 50), ("BITTERLEAF ", 1800), ("SNOW MACARONI", 600), ("PILLAF RICE  ", 1900), ("VEGETABLE FRIED RICE", 3100), ("KUKA", 900), ("FRUIT IN SEASON", 250), ("MACKEREL FISH", 1800), ("CHICKEN", 1700), ("FRUITE PLATER", 700), ("BEEF", 1300), ("NIGERIAN FRIED RICE", 859), ("FRESH FISH PEPPER SOUP", 2100), ("CORN AND CHICKEN SOUP", 1113), ("GOAT MEAT  PEPPER SOUP", 1600), ("CHICKEN PEPPER SOUP", 1700), ("CHICKEN MINISTRONI", 1400), ("CREAM OF MUSHROOM SOUP", 1300), ("CREAM OF CHICKEN SOUP", 1200), ("GOLDEN YAM", 844), ("YAM PORRIDGE", 1500), ("MASHED POTATOES", 0), ("FINGER FRIED YAM", 0), ("HAND CUT FRIES", 0), ("OVEN BAKED POTATOES ", 1764), ("VANILLA SLICED CAKE", 0), ("CHOCOLATE SLICED CAKE", 0), ("FRUITE PLATER ", 650),("FRUIT CAKE" , 900), ("WATER 75CL", 137), ("EBA", 300), ("COWLEG PEPPER SOUP", 1800), ("BREAD ROLL", 500), ("FRUIT IN SEASON", 250), ("MOI-MOI", 1368), ("SNOW RICE", 900), ("WHITE BEANS", 773), ("MACKEREL FISH", 1800), ("BEEF", 1270), ("JOLLOF", 800), ("GOAT", 1400), ("DRY FISH", 1000), ("CAT FISH", 1900), ("FRIED PLANTAIN", 824), ("CHINESE FRIED RICE", 2400), ("RUSSIAN SALAD", 1710), ("VANILLA SLICED CAKE", 0), ("SEMO", 300), ("EGUSI", 1700), ("FRESH OKRO", 1310), ("WHEAT", 400), ("OGBONO", 1720), ("EBA", 300), ("STEW", 600), ("CHICKEN", 1700), ("WATER MELON", 200), ("VANILLA SLICED CAKE", 0), ("WATER 75CL", 137), ("SARDINE", 0)],
    "PM Tea Break": [("TEA BAG", 117,), ("COFFEE", 100), ( "CHOCOLATE", 200), ("HONEY", 50), ("SUGAR", 26), ("CORNFLAKES", 200), ("BROWN SUGAR", 5), ("COCO POPS", 150), ("RICE CRISPIES", 200), ("TOASTED BREAD", 650), ("BUTTER", 50), ("AMERICAN PANCAKE", 1547), ("PANCAKE SYRUP", 100), ("MINI SANDWICHE", 600), ("PUFF-PUFF", 300), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("SWEET POTATO NUGGET", 910), ("FRESH BREAD", 250), ("OPEN SANDWICH", 2500), ("NIGERIAN PANCAKE", 100), ("EGG SANDWICH", 2000), ("YAM CHIPS", 800), ("GOLDEN YAM", 844), ("STIR FRY MACCARONI", 1200), ("FRIED SWEET POTATO", 400), ("MASA", 400), ("CHICKEN ", 1650), ("JOLLOF RICE", 800), ("BOILED POTATO", 910), ("SPAGHETTI JOLLF", 777), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI",800), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("BOILED YAM", 508), ("FRIED NOODLES", 1201), ("EGG SAUCE", 760), ("SCRAMBLED EGG", 770), ("TOMATO SAUCE", 500), ("FISH SAUCE", 2100), ("KIDNEY SAUCE", 2300), ("VEGETABLE SAUCE", 1100), ("BOILED EGG", 200), ("LIVER SAUCE", 2400), ("BEEF STEW", 1400), ("CHICKEN STEW", 1800), ("FRITATA", 50), ("ACHA PUDDING", 1100), ("AKARA", 960), ("OAT", 400), ("BEANS POTTAGE", 800), ("CORN PAP", 468), ("MOI-MOI", 1368), ("CUSTARD", 442), ("MINI SANDWICH", 300), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("SUNNY SIDE UP", 747), ("CUSTARD", 442), ("INFUSED WATER", 50), ("PAW-PAW", 250), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI", 800), ("ACHA PUDDING", 1100), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE ", 200), ("WATERMELON", 50), ("PAW-PAW FRUIT CUT", 250), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE CUT", 250), ("ORANGE", 100), ("BAKED BEANS", 895), ("STEAMED VEG", 50), ("WATER 75CL", 137), ("SAUSAGE", 425), ("GERMAN PANCAKE", 1200), ("GOLDEN YAM", 844), ("CHICKEN PIE", 350), ("APPLE", 400), ("YAM CHIPS", 800), ("VEGETABLE NOODLES", 1500), ("MILK", 115), ("STIRFRY MACCARONI", 1200), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("BOILED YAM", 508), ("FRIED NOODLES", 1201), ("EGG SAUCE", 760), ("SCRAMBLED EGG", 770), ("TOMATO SAUCE", 500), ("FISH SAUCE", 2100), ("KIDNEY SAUCE", 2300), ("VEGETABLE SAUCE", 1100), ("BOILED EGG", 200), ("LIVER SAUCE", 2400), ("BEEF STEW", 1400), ("CHICKEN STEW", 1800), ("FRITATA", 50), ("ACHA PUDDING", 1100), ("AKARA", 960), ("OAT", 400), ("BEANS POTTAGE", 800), ("CORN PAP", 468), ("MOI-MOI", 1368), ("CUSTARD", 442), ("MINI SANDWICH", 300), ("BOILED SWEET POTATO", 910), ("STIR FRY PASTA", 1344), ("SUNNY SIDE UP", 747), ("CUSTARD", 442), ("INFUSED WATER", 50), ("PAW-PAW", 250), ("BREAD ROLLS", 500), ("WAFFLES", 500), ("OVEN BAKED POTATO", 1764), ("JOLLOF MACCARONI", 800), ("ACHA PUDDING", 1100), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE ", 200), ("WATERMELON", 50), ("PAW-PAW FRUIT CUT", 250), ("WATERMELON JUICE", 500), ("SWEET MELON", 400), ("PINEAPPLE CUT", 250), ("ORANGE", 100), ("BAKED BEANS", 895), ("STEAMED VEG", 50), ("WATER 75CL", 137), ("SAUSAGE", 425), ("GERMAN PANCAKE", 1200), ("GOLDEN YAM", 844), ("CHICKEN PIE", 350), ("APPLE", 400), ("YAM CHIPS", 800), ("VEGETABLE NOODLES", 1500), ("MILK", 115), ("STIRFRY MACCARONI", 1200)],
    "Dinner": [("COWLEG PEPPER SOUP", 1800), ("BREAD ROLL", 500), ("FRUIT IN SEASON", 250), ("MOI-MOI", 1368), ("SNOW RICE", 900), ("WHITE BEANS", 773), ("MACKEREL FISH", 1800), ("BEEF", 1270), ("JOLLOF", 800), ("GOAT", 1400), ("DRY FISH", 1000), ("CAT FISH", 1900), ("FRIED PLANTAIN", 824), ("CHINESE FRIED RICE", 2400), ("RUSSIAN SALAD", 1710), ("VANILLA SLICED CAKE", 0), ("SEMO", 300), ("EGUSI", 1700), ("FRESH OKRO", 1310), ("WHEAT", 400), ("OGBONO", 1720), ("EBA", 300), ("STEW", 600), ("CHICKEN", 1700), ("WATER MELON", 200), ("VANILLA SLICED CAKE", 0), ("WATER 75CL", 137), ("SARDINE", 0), ("COCONUT RICE", 1300), ("CAT FISH", 1900), ("JOLLOF RICE ", 800), ("MACARONI JOLLOF", 800), ("SEMO", 300), ("OHA", 1710), ("EGUSI", 1700), ("MACKEREL FISH", 1900), ("MEXICAN FRIED RICE", 2000), ("SNOW RICE", 900), ("STIRFY PASTA", 1400), ("WHEAT", 400), ("EBA", 300), ("OGBONO", 1800), ("EWEDU", 1500), ("TOMATO STEW", 600), ("BEEF", 1270), ("VEGETABLE SALAD ", 1400), ("CHINESE FRIED RICE  ", 2400), ("PASTA JOLLOF", 777), ("FRESH OKRO", 1310), ("CHICKEN ", 1650), ("STEAMED VEGETABLE", 50), ("ENGLISH FRIED RICE ", 2000), ("SNOW PASTA", 600), ("EFORIRO", 50), ("GREEN VEGETABLE SAUCE", 1400), ("CURRY FRIED RICE", 1900), ("VEGETABLE SOUP", 1600), ("STEAMED VEGETABLE", 50), ("OYSTER SAUCE", 50), ("BITTERLEAF ", 1800), ("SNOW MACARONI", 600), ("PILLAF RICE  ", 1900), ("VEGETABLE FRIED RICE", 3100), ("KUKA", 900), ("FRUIT IN SEASON", 250), ("MACKEREL FISH", 1800), ("CHICKEN", 1700), ("FRUITE PLATER", 700), ("BEEF", 1300), ("NIGERIAN FRIED RICE", 859), ("FRESH FISH PEPPER SOUP", 2100), ("CORN AND CHICKEN SOUP", 1113), ("GOAT MEAT  PEPPER SOUP", 1600), ("CHICKEN PEPPER SOUP", 1700), ("CHICKEN MINISTRONI", 1400), ("CREAM OF MUSHROOM SOUP", 1300), ("CREAM OF CHICKEN SOUP", 1200), ("GOLDEN YAM", 844), ("YAM PORRIDGE", 1500), ("MASHED POTATOES", 0), ("FINGER FRIED YAM", 0), ("HAND CUT FRIES", 0), ("OVEN BAKED POTATOES ", 1764), ("VANILLA SLICED CAKE", 0), ("CHOCOLATE SLICED CAKE", 0), ("FRUITE PLATER ", 650),("FRUIT CAKE" , 900), ("WATER 75CL", 137), ("EBA", 300), ("COWLEG PEPPER SOUP", 1800), ("BREAD ROLL", 500), ("FRUIT IN SEASON", 250), ("MOI-MOI", 1368), ("SNOW RICE", 900), ("WHITE BEANS", 773), ("MACKEREL FISH", 1800), ("BEEF", 1270), ("JOLLOF", 800), ("GOAT", 1400), ("DRY FISH", 1000), ("CAT FISH", 1900), ("FRIED PLANTAIN", 824), ("CHINESE FRIED RICE", 2400), ("RUSSIAN SALAD", 1710), ("VANILLA SLICED CAKE", 0), ("SEMO", 300), ("EGUSI", 1700), ("FRESH OKRO", 1310), ("WHEAT", 400)],
}

# Set page configuration
try:
    st.set_page_config(
        page_title="CRISPAN SUITE & EVENT CENTER JOS",
        layout="centered",
        page_icon="icon.ico"  # Ensure this file exists in the working directory
    )
except Exception as e:
    st.warning(f"Page icon could not be set. Error: {e}")

# -------------------------------- LOGIN FUNCTION -------------------------------- #
# Simple login for the admin user
def login():
    st.title("CRISPAN SUITE & EVENT CENTER JOS")
    st.subheader("COST ANALYSIS APPLICATION")
    
    # Sidebar logo
    try:
        sidebar_img = Image.open("LOGO.png")  # Adjust the path to your logo
        sidebar_img = sidebar_img.resize((80, 80))
        st.sidebar.image(sidebar_img, use_container_width=True)
    except FileNotFoundError:
        st.sidebar.warning("Sidebar logo image not found. Please verify the file path.")
    
    # Login form
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state.logged_in = True
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid username or password")
            st.session_state.logged_in = False

# Check if the user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# -------------------------------- FUNCTIONS -------------------------------- #
# Function to update the meal list based on selected category
def update_meal_list(selected_category):
    meal_list = []
    if selected_category in MEAL_CATEGORIES:
        meal_list = MEAL_CATEGORIES[selected_category]
    return meal_list

# Function to calculate costs and save to database
def calculate_and_save(organization, selected_category, selected_meals, number_of_people, selling_price_per_person):
    try:
        if not selected_category:
            raise ValueError("Please select a meal category.")
        if not selected_meals:
            raise ValueError("Please select at least one meal.")
        if number_of_people <= 0:
            raise ValueError("Number of people must be greater than zero.")

        selected_meal_names = []
        total_cost = 0
        for meal_name, meal_cost in selected_meals:
            selected_meal_names.append(meal_name)
            total_cost += meal_cost * number_of_people

        total_selling_price = selling_price_per_person * number_of_people
        contribution_margin = total_selling_price - total_cost
        cost_margin = (total_cost / total_selling_price) * 100 if total_selling_price else 0

        current_date = datetime.now().strftime('%Y-%m-%d')
        day_of_week = datetime.now().strftime('%A')

        cursor.execute("""
        INSERT INTO orders (
            organization, meal_category, selected_meals, number_of_people, total_cost,
            total_selling_price, contribution_margin, cost_margin, date, day_of_week
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            organization, selected_category, ", ".join(selected_meal_names), number_of_people,
            total_cost, total_selling_price, contribution_margin, cost_margin,
            current_date, day_of_week
        ))
        conn.commit()
        st.success("Order saved successfully!")

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Function to display orders in a table with date range filter
def display_orders(start_date=None, end_date=None):
    query = "SELECT * FROM orders"
    if start_date and end_date:
        query += " WHERE Date BETWEEN ? AND ?"
        cursor.execute(query, (start_date, end_date))
    else:
        cursor.execute(query)

    records = cursor.fetchall()
    if not records:
        st.write("No records found")
    else:
        df = pd.DataFrame(records, columns=["ID", "Organization", "Meal Category", "Selected Meals", "Number of People",
                                            "Total Cost", "Total Selling Price", "Contribution Margin", "Cost Margin",
                                            "Date", "Day of Week"])
        st.write(df)

# Function to export orders to CSV
def export_to_csv():
    cursor.execute("SELECT * FROM orders")
    records = cursor.fetchall()
    if not records:
        st.write("No records to export.")
    else:
        filename = f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Organization", "Meal Category", "Selected Meals", "Number of People",
                             "Total Cost", "Total Selling Price", "Contribution Margin", "Cost Margin",
                             "Date", "Day of Week"])
            writer.writerows(records)
        st.success(f"Records exported successfully to {filename}")

# -------------------------------- STREAMLIT LAYOUT -------------------------------- #
# Sidebar for navigation
st.sidebar.header("Navigation")
app_mode = st.sidebar.radio(
    "Select an option",
    ["🏠 Home", "📋 View Orders", "📂 Export Orders", "📊 Property & Menu Engineering"]
)

# Main logo
try:
    logo_img = Image.open("LOGO.png")  # Adjust the path as needed
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Cost Analysis Application")
    with col2:
        st.image(logo_img, width=100)
except FileNotFoundError:
    st.warning("Main logo image not found. Please verify the file path.")

# Content based on selected option
if app_mode == "🏠 Home":
    st.header("Enter Order Details")

    organization = st.text_input("Organization Name")
    meal_category = st.selectbox("Select Meal Category", options=MEAL_CATEGORIES.keys())
    selected_meals = [meal[0] for meal in MEAL_CATEGORIES[meal_category]]
    meal_selection = st.multiselect("Select Meals", options=selected_meals)
    number_of_people = st.number_input("Number of People", min_value=1)
    selling_price_per_person = st.number_input("Selling Price per Person", min_value=1)

    if st.button("Save Order"):
        selected_meal_info = [meal for meal in MEAL_CATEGORIES[meal_category] if meal[0] in meal_selection]
        calculate_and_save(organization, meal_category, selected_meal_info, number_of_people, selling_price_per_person)

elif app_mode == "📋 View Orders":
    st.header("View All Orders")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date", min_value=start_date)

    if start_date and end_date:
        st.write(f"Displaying orders from **{start_date}** to **{end_date}**")
        display_orders(start_date=start_date, end_date=end_date)
    else:
        display_orders()

elif app_mode == "📂 Export Orders":
    st.header("Export Orders to CSV")
    export_to_csv()

elif app_mode == "📊 Property & Menu Engineering":
    st.header("Running Property & Menu Engineering")
    try:
        link = "https://menu-engineering.streamlit.app"  # Replace with the link you want to redirect to
        st.markdown(f"[Click here to view Menu Engineering]({link})", unsafe_allow_html=True)
        link = "https://cost-hall-room.streamlit.app/"  # Replace with the link you want to redirect to
        st.markdown(f"[Click here to view Room & Halls Costing]({link})", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------------- FOOTER -------------------------------- #
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Contact: costcontroller@crispanhotel.com | Phone: +2348168950765", unsafe_allow_html=True)

# Close database connection
conn.close()