import random
import csv
from datetime import datetime, timedelta

"""
Swedish User Data Generator (Python)

Generates 1000 user records with the fields:
"user_id", "user_name", "location", "gender", "education", "invest_goal"

Based on Swedish demographic statistics and Avanza investor data.
"""

# Create a list of major Swedish counties with approximate population distribution
counties = [
    {"name": "Stockholm", "ratio": 0.23},
    {"name": "Uppsala", "ratio": 0.04},
    {"name": "Södermanland", "ratio": 0.03},
    {"name": "Östergötland", "ratio": 0.05},
    {"name": "Jönköping", "ratio": 0.04},
    {"name": "Kronoberg", "ratio": 0.02},
    {"name": "Kalmar", "ratio": 0.025},
    {"name": "Gotland", "ratio": 0.006},
    {"name": "Blekinge", "ratio": 0.016},
    {"name": "Skåne", "ratio": 0.14},
    {"name": "Halland", "ratio": 0.035},
    {"name": "Västra Götaland", "ratio": 0.17},
    {"name": "Värmland", "ratio": 0.028},
    {"name": "Örebro", "ratio": 0.03},
    {"name": "Västmanland", "ratio": 0.028},
    {"name": "Dalarna", "ratio": 0.029},
    {"name": "Gävleborg", "ratio": 0.028},
    {"name": "Västernorrland", "ratio": 0.024},
    {"name": "Jämtland", "ratio": 0.013},
    {"name": "Västerbotten", "ratio": 0.028},
    {"name": "Norrbotten", "ratio": 0.025}
]

# Adjustments for investment customers
county_adjustments = {
    "Stockholm": {
        "general_multiplier": 1.3,  # Increase Stockholm representation overall
        "young_male_multiplier": 1.5  # Additional multiplier for males 20-39
    },
    "Västra Götaland": {
        "general_multiplier": 1.1  # Slight increase for Gothenburg area
    },
    "Skåne": {
        "general_multiplier": 1.1  # Slight increase for Malmö area
    }
}

# Gender distribution for Avanza investment customers (39% female, 61% male)
gender_ratio = {"male": 0.61, "female": 0.39}

# Age distribution for Avanza investment customers
age_distribution = [
    {"age_range": "18-19", "percentage": 0.02},
    {"age_range": "20-24", "percentage": 0.07},
    {"age_range": "25-29", "percentage": 0.20},
    {"age_range": "30-34", "percentage": 0.18},
    {"age_range": "35-39", "percentage": 0.15},
    {"age_range": "40-44", "percentage": 0.10},
    {"age_range": "45-49", "percentage": 0.08},
    {"age_range": "50-54", "percentage": 0.06},
    {"age_range": "55-59", "percentage": 0.05},
    {"age_range": "60-64", "percentage": 0.035},
    {"age_range": "65-69", "percentage": 0.025},
    {"age_range": "70-74", "percentage": 0.015},
    {"age_range": "75+", "percentage": 0.01}
]

# Education distribution by gender from the Swedish statistics
education_distribution = {
    "male": {
        "Primary (< 9 years)": 0.0263,
        "Primary (9-10 years)": 0.1452,
        "Upper secondary (< 2 years)": 0.185,
        "Upper secondary (3 years)": 0.2591,
        "Post-secondary (< 3 years)": 0.1484,
        "Post-secondary (≥ 3 years)": 0.1897,
        "Post-graduate": 0.0134,
        "No information": 0.0329
    },
    "female": {
        "Primary (< 9 years)": 0.0271,
        "Primary (9-10 years)": 0.1099,
        "Upper secondary (< 2 years)": 0.1565,
        "Upper secondary (3 years)": 0.2189,
        "Post-secondary (< 3 years)": 0.1594,
        "Post-secondary (≥ 3 years)": 0.2942,
        "Post-graduate": 0.0107,
        "No information": 0.0233
    }
}

# Map education levels to more common degree names
education_map = {
    "Primary (< 9 years)": "Elementary School",
    "Primary (9-10 years)": "Middle School",
    "Upper secondary (< 2 years)": "High School",
    "Upper secondary (3 years)": "High School",
    "Post-secondary (< 3 years)": "Bachelor's Degree",
    "Post-secondary (≥ 3 years)": "Master's Degree",
    "Post-graduate": "PhD",
    "No information": "Unknown"
}

# Sample first names for Sweden
first_names = {
    "male": [
        "Erik", "Lars", "Anders", "Johan", "Karl", "Per", "Nils", "Jan", "Gustav", "Olof",
        "Mikael", "Björn", "Fredrik", "Magnus", "Sven", "Peter", "Thomas", "Hans", "Bengt", "Daniel",
        "David", "Alexander", "Oscar", "Viktor", "William", "Lucas", "Elias", "Jonathan", "Filip", "Emil"
    ],
    "female": [
        "Anna", "Maria", "Eva", "Karin", "Sara", "Lena", "Emma", "Ingrid", "Christina", "Sofia",
        "Linnea", "Kerstin", "Astrid", "Johanna", "Elin", "Hanna", "Helena", "Ida", "Lisa", "Annika",
        "Maja", "Alice", "Julia", "Wilma", "Olivia", "Alicia", "Ebba", "Klara", "Elsa", "Matilda"
    ]
}

# Sample last names for Sweden
last_names = [
    "Andersson", "Johansson", "Karlsson", "Nilsson", "Eriksson", "Larsson", "Olsson", "Persson",
    "Svensson", "Gustafsson", "Pettersson", "Jonsson", "Jansson", "Hansson", "Bengtsson",
    "Jönsson", "Lindberg", "Jakobsson", "Magnusson", "Lindström", "Lindgren", "Axelsson",
    "Berg", "Bergström", "Lundberg", "Lind", "Lundgren", "Lundqvist", "Mattsson", "Ström",
    "Norberg", "Forsberg", "Nordström", "Sandberg", "Holmberg", "Sjöberg", "Nyström", "Wikström",
    "Engström", "Wallin", "Fransson", "Henriksson", "Forslund", "Gunnarsson", "Rosén", "Eklund"
]

# Investment goals with probability (50/50 split)
invest_goals = ["Long-term", "Short-term"]


def get_random_item_with_weight(items, weights):
    """Get a random item based on weights"""
    total_weight = sum(weights)
    random_val = random.random() * total_weight
    
    cumulative_weight = 0
    for i, weight in enumerate(weights):
        cumulative_weight += weight
        if random_val <= cumulative_weight:
            return items[i]
    
    # Fallback
    return items[-1]


def get_age_from_distribution():
    """Get age based on Avanza age distribution"""
    random_val = random.random()
    cumulative_percentage = 0
    
    for age_group in age_distribution:
        cumulative_percentage += age_group["percentage"]
        if random_val <= cumulative_percentage:
            # Parse the age range and get a random age within that range
            age_range = age_group["age_range"]
            
            # Handle "75+" range specially
            if age_range == "75+":
                min_age = 75
                max_age = 80  # Assume 80 as max age for "75+"
            else:
                # Normal range like "20-24"
                range_parts = age_range.split("-")
                min_age = int(range_parts[0])
                max_age = int(range_parts[1])
                
            return random.randint(min_age, max_age)
    
    # Fallback
    return 30


def is_young_adult(age):
    """Check if age is in young adult range (20-39)"""
    return 20 <= age <= 39


def get_county(gender, age):
    """Get county with adjustments based on Avanza data"""
    # Adjust county ratios based on Avanza data
    adjusted_counties = []
    
    for county in counties:
        name = county["name"]
        ratio = county["ratio"]
        multiplier = 1
        
        if name in county_adjustments:
            adjustment = county_adjustments[name]
            multiplier = adjustment.get("general_multiplier", 1)
            
            # Apply additional multiplier for young males in Stockholm
            if (gender == "Male" and is_young_adult(age) and 
                name == "Stockholm" and "young_male_multiplier" in adjustment):
                multiplier *= adjustment["young_male_multiplier"]
        
        adjusted_counties.append({
            "name": name,
            "ratio": ratio * multiplier
        })
    
    # Normalize ratios to sum to 1
    total_ratio = sum(county["ratio"] for county in adjusted_counties)
    normalized_counties = [{
        "name": county["name"],
        "ratio": county["ratio"] / total_ratio
    } for county in adjusted_counties]
    
    return get_random_item_with_weight(
        [county["name"] for county in normalized_counties],
        [county["ratio"] for county in normalized_counties]
    )


def generate_simple_user_csv(count, filename):
    """Generate simple CSV data and write to file"""
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        # Create CSV writer
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        
        # Write header row with added age field
        writer.writerow(["user_id", "user_name", "location", "gender", "age", "education", "invest_goal"])
        
        # Generate and write user records
        for i in range(1, count + 1):
            # Determine gender based on Avanza distribution
            gender = "Male" if random.random() < gender_ratio["male"] else "Female"
            
            # Get specific age based on Avanza age distribution
            age = get_age_from_distribution()
            
            # Get name
            first_name = random.choice(first_names["male" if gender == "Male" else "female"])
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            
            # Get county based on distribution with adjustments for young males in Stockholm
            location = get_county(gender, age)
            
            # Get education level based on gender
            gender_lower = gender.lower()
            education_level = get_random_item_with_weight(
                list(education_distribution[gender_lower].keys()),
                list(education_distribution[gender_lower].values())
            )
            
            # Map to common degree name
            education = education_map[education_level]
            
            # Get investment goal (50/50 split)
            invest_goal = random.choice(invest_goals)
            
            # Create user_id
            user_id = 1000 + i
            
            # Write CSV row with age added
            writer.writerow([
                user_id,        # user_id
                full_name,      # user_name
                location,       # location
                gender,         # gender
                age,            # age
                education,      # education
                invest_goal,    # invest_goal
            ])
    
    print(f"Generated {count} user records and saved to {filename}")
    return filename


def preview_csv(filename, num_rows=10):
    """Preview the first few rows of the generated CSV file"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [next(f) for _ in range(num_rows + 1)]  # +1 for header
    
    print(f"\nPreview of first {num_rows} rows:")
    for line in lines:
        print(line.strip())


# Generate 1000 users and save to CSV file
if __name__ == "__main__":
    output_file = "swedish_users.csv"
    generate_simple_user_csv(1000, output_file)
    preview_csv(output_file)