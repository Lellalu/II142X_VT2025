import argparse
import os
import time
import pandas as pd
from syntheticDataGenerators.investment.llm_purchase_generator import LLMPurchaseGenerator, User
from tqdm import tqdm
from investmentByAge import female_investments_by_age_median, male_investments_by_age_median

def generate_basket_description(row):
    """
    Generate a descriptive string for a basket based on its features.
    Only includes features with values >= 0.05 (5%).
    
    Args:
        row: pandas Series containing basket features
        
    Returns:
        str: Descriptive string of the basket features
    """
    # Convert string values to float, replacing any non-numeric values with 0
    numeric_row = pd.to_numeric(row, errors='coerce').fillna(0)
    
    # Filter features with values >= 0.05
    significant_features = numeric_row[numeric_row >= 0.01]
    
    # Convert to percentage and format
    descriptions = []
    for feature, value in significant_features.items():
        percentage = value * 100
        descriptions.append(f"{percentage:.0f}% {' '.join(feature.split('_'))}")
    
    # Join all descriptions
    return ", ".join(descriptions)

def main():
    parser = argparse.ArgumentParser(description='Generate synthetic investment purchase data')
    
    parser.add_argument('--user_data', type=str, required=True,
                      help='Path to CSV file containing user data')
    
    parser.add_argument('--basket_data', type=str, required=True,
                      help='Path to CSV file containing basket data')
    
    parser.add_argument('--max_purchases', type=int, required=True,
                      help='Maximum number of purchases per user')
    
    parser.add_argument('--output_file', type=str, required=True,
                      help='Path to output file')
    
    args = parser.parse_args()
    
    user_data = pd.read_csv(args.user_data)
    basket_data = pd.read_csv(args.basket_data)
    
    # Generate descriptions for each basket
    basket_descriptions = basket_data.apply(generate_basket_description, axis=1)
    all_basket_description = "\n".join([
        f"{basket_name}: {description}"
        for basket_name, description in zip(basket_data['basket_name'], basket_descriptions)
    ])

    llm_purchase_generator = LLMPurchaseGenerator(
        #model_name="openai/gpt-4o-mini",
        model_name="google/gemini-2.0-flash-001",
        all_basket_description=all_basket_description,
        max_number_of_investments=args.max_purchases
    )

    # Read existing output file if it exists
    last_investment_id = -1
    processed_user_ids = set()
    if os.path.exists(args.output_file):
        existing_data = pd.read_csv(args.output_file, sep=';')
        if not existing_data.empty:
            last_investment_id = existing_data['investment_id'].max()
            processed_user_ids = set(existing_data['user_id'].unique())

    investment_id = last_investment_id + 1
    
    # Open file in append mode
    with open(args.output_file, 'a') as f:
        # Write header only if file is empty
        if last_investment_id == -1:
            f.write('investment_id;user_id;basket_name;investment_amount\n')
            
        for _, row in tqdm(user_data.iterrows(), total=len(user_data)):
            # Skip already processed users
            if row['user_id'] in processed_user_ids:
                continue
                
            time.sleep(1)
            if row['gender'] == 'Female':
                user_median_investment_amount = female_investments_by_age_median[int(row['age'])]
            else:
                user_median_investment_amount = male_investments_by_age_median[int(row['age'])]

            user = User(
                user_location=row['location'],
                user_gender=row['gender'],
                user_age=row['age'],
                user_education=row['education'],
                user_invest_goal=row['invest_goal'],
                user_median_investment_amount=user_median_investment_amount
            )
            investments = llm_purchase_generator.generate_investment_by_user(user)
            for investment in investments.investments:
                if investment.basket_name in basket_data['basket_name'].values:
                    f.write(f"{investment_id};{row['user_id']};{investment.basket_name};{investment.investment_amount}\n")
                    investment_id += 1

if __name__ == "__main__":
    main()