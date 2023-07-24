# Import the pandas library under its usual alias
import pandas as pd

# Load the business.csv file as a DataFrame called businesses
businesses = pd.read_csv("datasets/businesses.csv")

# Sort businesses from oldest businesses to youngest
sorted_businesses = businesses.sort_values('year_founded')

# Display the first few lines of sorted_businesses
print("\n--------------- sorted_businesses ----------------\n")
print(sorted_businesses.head())

# Load countries.csv to a DataFrame
countries = pd.read_csv('datasets/countries.csv')

# Merge sorted_businesses with countries
businesses_countries = sorted_businesses.merge(countries, on="country_code")

# Filter businesses_countries to include countries in North America only
north_america = businesses_countries[businesses_countries['continent'] == 'North America']
print("\n--------------- north_america ----------------\n")
print(north_america.head())

# Create continent, which lists only the continent and oldest year_founded
continent = businesses_countries.groupby("continent").agg({"year_founded":"min"})

# Merge continent with businesses_countries
merged_continent = continent.merge(businesses_countries, on=["continent", "year_founded"])

# Subset continent so that only the four columns of interest are included
subset_merged_continent = merged_continent[['continent', 'country', 'business', 'year_founded']]
print("\n--------------- subset_merged_continent ----------------\n")
print(subset_merged_continent)

# Use .merge() to create a DataFrame, all_countries
all_countries = businesses.merge(countries, on="country_code", how="right",  indicator=True)

# Filter to include only countries without oldest businesses
missing_countries = all_countries[all_countries["_merge"] != "both"]

# Create a series of the country names with missing oldest business data
missing_countries_series = missing_countries['country']

# Display the series
print("\n--------------- missing_countries_series ----------------\n")
print(missing_countries_series)

# Import new_businesses.csv
new_businesses = pd.read_csv('datasets/new_businesses.csv')

# Add the data in new_businesses to the existing businesses
all_businesses = pd.concat([new_businesses, businesses])

# Merge and filter to find countries with missing business data
new_all_countries = all_businesses.merge(countries, on="country_code", how="outer", indicator=True)
new_missing_countries = new_all_countries[new_all_countries["_merge"] != "both"]

# Group by continent and create a "count_missing" column
count_missing = new_missing_countries.groupby("continent").agg({"country":"count"})
count_missing.columns = ["count_missing"]
print("\n--------------- count_missing ----------------\n")
print(count_missing)

# Import categories.csv and merge to businesses
categories = pd.read_csv("datasets/categories.csv")
businesses_categories = businesses.merge(categories, on='category_code')

# Create a DataFrame which lists the number of oldest businesses in each category
count_business_cats = businesses_categories.groupby("category").agg({"business":"count"})

# Create a DataFrame which lists the cumulative years businesses from each category have been operating
years_business_cats = businesses_categories.groupby("category").agg({"year_founded":"sum"})

# Rename columns and display the first five rows of both DataFrames
count_business_cats.columns = ['count']
years_business_cats.columns = ['total_years_in_business']
print("\n--------------- count_business_cats ----------------\n")
print(count_business_cats.head())
print("\n--------------- years_business_cats ----------------\n")
print(years_business_cats.head())

# Filter using .query() for CAT4 businesses founded before 1800; sort results
old_restaurants = businesses_categories.query("category_code == 'CAT4' and year_founded < 1800")

# Sort the DataFrame
old_restaurants = old_restaurants.sort_values('year_founded')
print("\n--------------- old_restaurants ----------------\n")
print(old_restaurants)

# Merge all businesses, countries, and categories together
businesses_categories_countries = businesses_categories.merge(countries, on="country_code")

# Sort businesses_categories_countries from oldest to most recent
businesses_categories_countries = businesses_categories_countries.sort_values("year_founded")

# Create the oldest by continent and category DataFrame
oldest_by_continent_category = businesses_categories_countries.groupby(["continent", "category"]).agg({"year_founded":"min"})
print("\n--------------- oldest_by_continent_category ----------------\n")
print(oldest_by_continent_category.head())

