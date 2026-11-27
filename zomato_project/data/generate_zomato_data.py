"""
Generates clean, realistic Zomato / Swiggy Restaurant dataset
for Aditi's Data Analytics portfolio.
"""
import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'zomato_restaurants_data.csv')

def generate_zomato_data(num_rows=5000):
    np.random.seed(42)

    cities_data = {
        "Bangalore": ["Koramangala", "Indiranagar", "HSR Layout", "Whitefield", "Jayanagar", "MG Road"],
        "Delhi-NCR": ["Connaught Place", "Cyber Hub", "Hauz Khas", "Saket", "Noida Sector 18", "Rajouri Garden"],
        "Mumbai": ["Bandra West", "Andheri West", "Juhu", "Lower Parel", "Powai", "Colaba"],
        "Hyderabad": ["Gachibowli", "Jubilee Hills", "Banjara Hills", "Madhapur", "Kondapur"],
        "Pune": ["Baner", "Koregaon Park", "Viman Nagar", "Kothrud", "Wakad"],
        "Kolkata": ["Park Street", "Salt Lake", "Ballygunge", "New Town", "Sector V"]
    }

    cuisines_info = [
        ("North Indian", 450, 1200, 0.22),
        ("Biryani", 350, 850, 0.18),
        ("Chinese", 300, 750, 0.16),
        ("Fast Food", 200, 500, 0.15),
        ("South Indian", 150, 400, 0.10),
        ("Desserts", 180, 450, 0.08),
        ("Italian", 600, 1600, 0.06),
        ("Mughlai", 500, 1400, 0.05)
    ]
    cuisines = [c[0] for c in cuisines_info]
    cuisine_weights = [c[3] for c in cuisines_info]

    chain_prefixes = {
        "North Indian": ["Punjabi Rasoi", "Dhaba by Claridges", "Pind Balluchi", "Gulati Express", "Haveli"],
        "Biryani": ["Behrouz Biryani", "Paradise Biryani", "Bawarchi", "Biryani By Kilo", "Meghana Foods"],
        "Chinese": ["Mainland China", "Wow! Momo", "Chowman", "Dragon House", "The Fatty Bao"],
        "Fast Food": ["Burger King", "McDonald's", "Subway", "Domino's Pizza", "KFC"],
        "South Indian": ["Sagar Ratna", "Saravana Bhavan", "Vidyarthi Bhavan", "A2B - Adyar Ananda Bhavan", "Udupi Grand"],
        "Desserts": ["The Belgian Waffle Co.", "Baskin Robbins", "Keventers", "Giani Ice Cream", "Sweet Truth"],
        "Italian": ["Toscano", "Little Italy", "PizzaExpress", "Chianti", "Smoke House Deli"],
        "Mughlai": ["Karim's", "Al Jawahar", "Dastarkhwan", "Tunday Kababi", "Bademiya"]
    }

    rows = []
    for i in range(1, num_rows + 1):
        rest_id = f"ZOM-{10000 + i}"
        
        city = np.random.choice(list(cities_data.keys()), p=[0.25, 0.23, 0.20, 0.14, 0.10, 0.08])
        locality = np.random.choice(cities_data[city])

        cuisine_idx = np.random.choice(len(cuisines), p=cuisine_weights)
        cuisine_name, min_cost, max_cost, _ = cuisines_info[cuisine_idx]

        base_name = np.random.choice(chain_prefixes[cuisine_name])
        rest_name = f"{base_name} - {locality}"

        # Cost for two
        cost_for_two = int(np.random.uniform(min_cost, max_cost) // 50 * 50)
        if cost_for_two < 150: cost_for_two = 150

        # Price Category
        if cost_for_two <= 400:
            price_category = "Budget (< ₹400)"
        elif cost_for_two <= 800:
            price_category = "Mid-Range (₹400 - ₹800)"
        else:
            price_category = "Fine Dining (> ₹800)"

        # Online Delivery & Table Booking
        has_online_delivery = np.random.choice(["Yes", "No"], p=[0.78, 0.22])
        has_table_booking = np.random.choice(["Yes", "No"], p=[0.15 if cost_for_two < 800 else 0.55, 0.85 if cost_for_two < 800 else 0.45])

        # Delivery Time
        if has_online_delivery == "Yes":
            delivery_time = int(np.random.choice([25, 30, 35, 40, 45, 52, 60], p=[0.15, 0.25, 0.28, 0.16, 0.08, 0.05, 0.03]))
        else:
            delivery_time = 0

        # Rating logic: Faster delivery & quality restaurants get higher ratings
        if has_online_delivery == "Yes" and delivery_time > 45:
            # Latency penalty: customer review drops
            rating = round(float(np.random.uniform(3.0, 3.9)), 1)
        elif cost_for_two > 1000:
            # Fine dining usually has higher ratings
            rating = round(float(np.random.uniform(3.9, 4.8)), 1)
        else:
            rating = round(float(np.random.uniform(3.4, 4.6)), 1)

        # Rating Status
        if rating >= 4.5:
            rating_status = "Excellent"
        elif rating >= 4.0:
            rating_status = "Very Good"
        elif rating >= 3.5:
            rating_status = "Good"
        else:
            rating_status = "Average"

        # Votes (Customer Reviews Count)
        if rating >= 4.2:
            votes = int(np.random.exponential(scale=650) + 200)
        else:
            votes = int(np.random.exponential(scale=250) + 40)

        rows.append({
            "Restaurant_ID": rest_id,
            "Restaurant_Name": rest_name,
            "City": city,
            "Locality": locality,
            "Cuisine": cuisine_name,
            "Average_Cost_for_Two": cost_for_two,
            "Price_Category": price_category,
            "Has_Online_Delivery": has_online_delivery,
            "Has_Table_Booking": has_table_booking,
            "Rating": rating,
            "Rating_Status": rating_status,
            "Votes": votes,
            "Delivery_Time_Min": delivery_time
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Zomato dataset created successfully at: {OUTPUT_PATH}")
    print(f"Total Restaurants: {len(df)}")
    print(f"Cities Covered: {df['City'].nunique()}")
    print(f"Average Cost for Two: ₹{df['Average_Cost_for_Two'].mean():.1f}")
    print(f"Average Rating: {df['Rating'].mean():.2f}")
    print(f"Online Delivery Enabled: {len(df[df['Has_Online_Delivery'] == 'Yes'])} ({len(df[df['Has_Online_Delivery'] == 'Yes']) / len(df) * 100:.1f}%)")

if __name__ == "__main__":
    generate_zomato_data()
