import streamlit as st
import pandas as pd
from product_filter import recommend_items, df
import time
import matplotlib.pyplot as plt

def plot_pie_chart(data, category_column):
    # Count the number of items per category
    category_counts = data[category_column].value_counts()

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Number of Items per General Category')
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.

    return plt


st.set_page_config(
    page_title="Best Experience",
    page_icon="🍉",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an extremely cool app!"
    },
)

# Custom CSS for the sidebar
sidebar_style = """
<style>
    [data-testid="stSidebar"] button {
        background-color: #c2fbd7;
        border-radius: 100px;
        box-shadow: rgba(44, 187, 99, .2) 0 -25px 18px -14px inset, rgba(44, 187, 99, .15) 0 1px 2px, rgba(44, 187, 99, .15) 0 2px 4px, rgba(44, 187, 99, .15) 0 4px 8px, rgba(44, 187, 99, .15) 0 8px 16px, rgba(44, 187, 99, .15) 0 16px 32px;
        color: green;
        cursor: pointer;
        display: inline-block;
        font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;
        padding: 7px 20px;
        text-align: center;
        text-decoration: none;
        transition: all 250ms;
        border: 0;
        font-size: 16px;
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
    }
    [data-testid="stSidebarCollapseButton"] {
        display: none;
    }
    button:hover {
        box-shadow: rgba(44, 187, 99, .35) 0 -25px 18px -14px inset, rgba(44, 187, 99, .25) 0 1px 2px, rgba(44, 187, 99, .25) 0 2px 4px, rgba(44, 187, 99, .25) 0 4px 8px, rgba(44, 187, 99, .25) 0 8px 16px, rgba(44, 187, 99, .25) 0 16px 32px;
        transform: scale(1.05) rotate(-1deg);
    }
</style>
"""

# Custom CSS for sidebar
sidebar_color = "#063740"  # Replace this with your desired color
sidebar_text_color = "#edf8fa"  # Replace this with your desired text color

st.markdown(
    f"""
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_color};
        color: {sidebar_text_color};
    }}

    /* Sidebar text color */
    [data-testid="stSidebar"] * {{
        color: {sidebar_text_color};
    }}

    /* Sidebar link color */
    [data-testid="stSidebar"] a {{
        color: {sidebar_text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Initialize RAG chain
    top_recommended_products = pd.DataFrame()


    # Inject the CSS into the Streamlit app
    st.markdown(sidebar_style, unsafe_allow_html=True)
    st.subheader("Distribution of Items per division  cx²")
    pie_chart = plot_pie_chart(df, 'division_name')  # Replace 'general_category' with your actual column name
    st.pyplot(pie_chart)
    with st.sidebar:
            st.title('Products Evaluation System')
            # Select class_name (first line)
            class_name = df['class_name'].unique().tolist()
            class_name.insert(0, 'All')
            Product_type = st.selectbox('Select your class_name:', class_name)
            # Load data from the helper script (you can load unique department_name directly)
            unique_labels = df['department_name'].unique().tolist()
            unique_labels.insert(0, 'All')
            # Select label filter (second line)
            label_filter = st.selectbox('Filter by label (optional):', unique_labels)
            # Select rank filter (third line)
            rank_filter = st.slider('Select rank range:', 
                                    min_value=int(df['rating'].min()), 
                                    max_value=int(df['rating'].max()), 
                                    value=(int(df['rating'].min()), int(df['rating'].max())))

            unique_brands = df['division_name'].unique().tolist()
            unique_brands.insert(0, 'All')

            # Select division_name filter (fourth line)
            brand_filter = st.selectbox('Filter by brand (optional):', unique_brands)

            # Button to find similar products (fifth line)
            if st.button('Find similar products!'):
                top_recommended_products = recommend_items(Product_type, label_filter, brand_filter, rank_filter)
                top_recommended_products.reset_index(inplace=True, drop=True)

        # Check if top_recommended_products is empty
    if top_recommended_products.empty:
            st.write("No recommended products available.")
    else:
            with st.spinner("Just a moment while we create your personalized recommendation 🧴✨"):
                st.empty()

                # Create a clickable table with expandable details
                st.subheader('Recommended Products')

                # Debug: Print the DataFrame structure
                st.write(top_recommended_products)

                for index, row in top_recommended_products.iterrows():
                    with st.expander(f"Details for {row['division_name']}", expanded=True):  # You can set 'expanded=True' to have it open by default
                        st.write(f"*Division Name*: {row['division_name']}")
                        st.write(f"*Rating*: {row['rating']}")
                        st.write(f"*weighted_vadar*: {row['weighted_vadar']}")
                        # Add any other relevant information from the row as needed
                        # st.write(f"*Other Info*: {row['other_column_name']}")  # Uncomment and replace with actual columns if needed

if __name__ == "__main__":
  main()