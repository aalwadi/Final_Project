import pandas as pd


# Load data
file_path = '../data/final_vader.csv'
df = pd.read_csv(file_path)



def recommend_items(class_name, department_name, division_name, rating_range, num_recommendations=5):
    # Apply initial filters
    filtered_products = df.copy()  # Use a copy of the DataFrame to avoid modifying the original
    
    if class_name != 'All':
        filtered_products = filtered_products[filtered_products['class_name'] == class_name]
    
    if department_name != 'All':
        filtered_products = filtered_products[filtered_products['department_name'] == department_name]
    
    if division_name != 'All':
        filtered_products = filtered_products[filtered_products['division_name'] == division_name]
    

    
    # Filter by rating
    filtered_products = filtered_products[
        (filtered_products['rating'] >= rating_range[0]) & 
        (filtered_products['rating'] <= rating_range[1])
    ]
    
    
    # Select the top recommendations based on rating
    recommended_items = filtered_products.nlargest(num_recommendations, 'rating')

    return recommended_items.reset_index(drop=True)