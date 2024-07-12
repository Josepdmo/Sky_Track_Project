import gdown
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px
import requests
from bs4 import BeautifulSoup


def uploading_flight_data():
    """
    Uploads the flight data from a local CSV file. If the local file is not found,
    it downloads the data from Google Drive.

    Explanation:
    This function first attempts to read the flight data from a local CSV file named 'downloaded_file.csv'.
    If the file is not found, it catches the exception and proceeds to download the file from a specified
    Google Drive link. After downloading, it reads the data from the newly downloaded file and returns it
    as a DataFrame.

    Args:
    None

    Returns:
    pd.DataFrame: The flight data loaded into a DataFrame.
    """
    try:
        df = pd.read_csv("downloaded_file.csv")
        return df
    except:
        file_id = '1HZUl8G9vkjTzYCQ43sOsMEIy-MP6k4v8'
        url = f'https://drive.google.com/uc?id={file_id}'
        output_path = 'downloaded_file.csv'  # Change the extension if it's not a CSV
        gdown.download(url, output_path, quiet=False)
        df = pd.read_csv(output_path)
        return df


def uploading_airport_code_data():
    """
    Uploads the airport code data from a local CSV file. If the local file is not found,
    it downloads the data from Google Drive.

    Explanation:
    This function first attempts to read the airport code data from a local CSV file named 'city-mappings.csv'.
    If the file is not found, it catches the exception and proceeds to download the file from a specified
    Google Drive link. After downloading, it reads the data from the newly downloaded file and returns it
    as a DataFrame.

    Args:
    None

    Returns:
    pd.DataFrame: The airport code data loaded into a DataFrame.
    """
    try:
        df_airport_codes = pd.read_csv("city-mappings.csv")
        return df_airport_codes
    except:
        file_id = '11sqbXlS21wFF4fsxtfurReCvOncVDIpW'
        url = f'https://drive.google.com/uc?id={file_id}'
        output_path = 'city-mappings.csv'  # Change the extension if it's not a CSV
        gdown.download(url, output_path, quiet=False)
        df_airport_codes = pd.read_csv(output_path)
        return df_airport_codes

def add_city_columns(df_flight_input, df_airport_codes_input):
    """
    Adds city_of_departure and city_of_arrival columns to the flight data DataFrame based on airport codes.

    Explanation:
    This function merges the flight data DataFrame with the airport codes DataFrame to add columns indicating
    the city of departure and city of arrival. It first creates separate DataFrames for departure and arrival
    airport codes, merges these with the flight data, and then reorders the columns for readability.

    Args:
    df_flight_input (pd.DataFrame): The flight data DataFrame.
    df_airport_codes_input (pd.DataFrame): The airport codes DataFrame.

    Returns:
    pd.DataFrame: The flight data DataFrame with added city_of_departure and city_of_arrival columns.
    """
    df = df_flight_input.copy()
    df_airport_codes = df_airport_codes_input.copy()

    # Drop unnecessary columns from df_airport_codes
    df_airport_codes.drop(columns=["index", "Airport Name", "four_digit", "l1", "l2", "Country"], inplace=True)
    
    # Rename columns in df_airport_codes for city_of_departure
    df_airport_codes_departure = df_airport_codes.rename(columns={'three-digit code': 'from_airport_code', 'City': 'city_of_departure'})
    
    # Perform the merge to add city_of_departure
    df = pd.merge(df, df_airport_codes_departure[['from_airport_code', 'city_of_departure']], on='from_airport_code', how='left')
    
    # Rename columns in df_airport_codes for city_of_arrival
    df_airport_codes_arrival = df_airport_codes.rename(columns={'three-digit code': 'dest_airport_code', 'City': 'city_of_arrival'})
    
    # Perform the merge to add city_of_arrival
    df = pd.merge(df, df_airport_codes_arrival[['dest_airport_code', 'city_of_arrival']], on='dest_airport_code', how='left')
    
    # Reorder the columns to place city_of_departure and city_of_arrival next to their respective airport codes
    cols = df.columns.tolist()
    from_idx = cols.index('from_airport_code') + 1
    to_idx = cols.index('dest_airport_code') + 1
    
    cols.insert(from_idx, cols.pop(cols.index('city_of_departure')))
    cols.insert(to_idx, cols.pop(cols.index('city_of_arrival')))
    
    df = df[cols]
    
    return df

def clean_flight_data(df_input):
    """
    Cleans the flight data by performing several operations:
    1. Drops rows with layovers and with null co2 emissions values
    2. Renames the duration column to indicate it is measured in minutes.
    3. Fills null values in avg_co2_emission_for_this_route and co2_percentage.
    4. Manually inserts the city name for missing airport codes.

    Args:
    df_input (pd.DataFrame): The flight data DataFrame.

    Returns:
    pd.DataFrame: The cleaned flight data DataFrame.
    """
    df = df_input.copy()

    # 3.1 Drop rows with layovers

    df = df[df.stops == 0]

    # 3.2 Rename the duration column
    df.rename(columns={'duration': 'duration_minutes'}, inplace=True)

    df.dropna(subset=['co2_emissions'], inplace = True)

    # 3.4 Fill null values in avg_co2_emission_for_this_route and co2_percentage
    # Step 1: Identify routes with null values in 'avg_co2_emission_for_this_route'
    routes_with_null_avg_co2 = df[df['avg_co2_emission_for_this_route'].isnull()]

    # Step 2: Calculate the average CO2 emissions for these routes
    route_avg_co2 = routes_with_null_avg_co2.groupby(['from_airport_code', 'dest_airport_code'])['co2_emissions'].mean().reset_index()

    # Rename the 'co2_emissions' column to 'avg_co2_emission_for_this_route_new' for direct use
    route_avg_co2.rename(columns={'co2_emissions': 'avg_co2_emission_for_this_route_new'}, inplace=True)

    # Step 3: Merge the route averages back into the original DataFrame (df)
    df = pd.merge(df, route_avg_co2, on=['from_airport_code', 'dest_airport_code'], how='left')

    # Step 4: Fill the null values in 'avg_co2_emission_for_this_route' with the calculated route averages
    df['avg_co2_emission_for_this_route'].fillna(df['avg_co2_emission_for_this_route_new'], inplace=True)

    # Step 5: Recalculate the CO2 percentage based on the filled average CO2 emissions
    df['co2_percentage'] = (df['co2_emissions'] - df['avg_co2_emission_for_this_route']) / df['avg_co2_emission_for_this_route'] * 100

    # Drop the temporary 'avg_co2_emission_for_this_route_new' column as it is no longer needed
    df.drop(columns=['avg_co2_emission_for_this_route_new'], inplace=True)

    # 3.5 Insert the city name for Doha manually
    df.city_of_arrival.fillna("Doha", inplace=True)

    return df

def most_pollutant_routes(df_input):
    """
    Calculates the top 20 most pollutant routes by CO2 emissions and creates a bar graph.

    Args:
    df (pd.DataFrame): The flight data DataFrame.

    Returns:
    pd.DataFrame: The DataFrame containing the top 20 most pollutant routes.
    """
    df = df_input.copy()

    # Group by route and sum CO2 emissions
    pollutant_routes = df.groupby(['city_of_departure', 'city_of_arrival'])['co2_emissions'].sum().reset_index()
    
    # Sort by CO2 emissions in descending order
    pollutant_routes = pollutant_routes.sort_values(by='co2_emissions', ascending=False)
    
    # Display the top 20 most pollutant routes
    top_pollutant_routes = pollutant_routes.head(20)
    
    # Create a bar graph using Plotly
    fig = px.bar(top_pollutant_routes, 
                 x='co2_emissions', 
                 y='city_of_departure', 
                 color='city_of_arrival', 
                 orientation='h', 
                 title='Top 20 Most Pollutant Routes by CO2 Emissions',
                 labels={'co2_emissions': 'CO2 Emissions (kg)', 'city_of_departure': 'City of Departure'},
                 height=600)

    # Show the plot
    fig.show()
    
    return top_pollutant_routes

def most_polluting_aircraft_types(df_input):
    """
    Determines the top 20 most polluting aircraft types by total CO2 emissions and creates a bar graph.

    Args:
    df (pd.DataFrame): The flight data DataFrame.

    Returns:
    pd.DataFrame: The DataFrame containing the top 20 most polluting aircraft types.
    """
    df = df_input.copy()
    
    # Aggregate CO2 emissions by aircraft type
    polluting_aircraft = df.groupby('aircraft_type')['co2_emissions'].sum().reset_index()
    
    # Sort by CO2 emissions in descending order
    most_polluting_aircraft = polluting_aircraft.sort_values(by='co2_emissions', ascending=False)
    
    # Display the top 20 most polluting aircraft types
    top_polluting_aircraft = most_polluting_aircraft.head(20)
    
    # Create the bar plot using Plotly
    fig = px.bar(top_polluting_aircraft, x='aircraft_type', y='co2_emissions',
                 title='Top 20 Most Polluting Aircraft Types by Total CO2 Emissions',
                 labels={'aircraft_type': 'Aircraft Type', 'co2_emissions': 'Total CO2 Emissions'},
                 color='co2_emissions', color_continuous_scale='Viridis')

    # Customize the layout
    fig.update_layout(
        xaxis_title='Aircraft Type',
        yaxis_title='Total CO2 Emissions',
        title_x=0.5  # Center the title
    )

    # Show the plot
    fig.show()
    
    return top_polluting_aircraft

def correlation_price_co2_emissions(df_input):
    """
    Calculates the correlation between ticket price and CO2 emissions per flight and creates a scatter plot.

    Args:
    df (pd.DataFrame): The flight data DataFrame.

    Returns:
    float: The correlation coefficient between ticket price and CO2 emissions.
    """
    df = df_input.copy()

    # Calculate the correlation coefficient between ticket price and CO2 emissions
    correlation_price_co2 = df['price'].corr(df['co2_emissions'])
    print(f"Correlation between ticket price and CO2 emissions: {correlation_price_co2}")

    # Create a scatter plot with Plotly
    fig = px.scatter(df, x='price', y='co2_emissions', 
                     title='Scatter Plot: Ticket Price vs CO2 Emissions',
                     labels={'price': 'Ticket Price', 'co2_emissions': 'CO2 Emissions'},
                     trendline='ols',  # Add a trendline (OLS regression)
                     color='co2_emissions', color_continuous_scale='Viridis',  # Color points based on CO2 emissions
                     hover_name=df.index)  # Show index as hover name

    # Customize the layout
    fig.update_layout(
        xaxis_title='Ticket Price',
        yaxis_title='CO2 Emissions',
        title_x=0.5  # Center the title
    )

    # Show the plot
    fig.show()
    
    return correlation_price_co2

def most_popular_routes(df_input):
    """
    Identifies the top 10 most popular routes by number of flights and creates a funnel plot.

    Args:
    df_input (pd.DataFrame): The flight data DataFrame.

    Returns:
    pd.DataFrame: The DataFrame containing the top 10 most popular routes.
    """
    # Copy the input DataFrame
    df = df_input.copy()
    
    # Count the number of flights for each route
    popular_routes = df.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='num_flights')
    
    # Sort by number of flights in descending order
    most_popular_routes = popular_routes.sort_values(by='num_flights', ascending=False)
    
    # Display the top 10 most popular routes
    top_popular_routes = most_popular_routes.head(10)
    
    # Create a funnel plot using Plotly Express
    fig = px.funnel(
        top_popular_routes,
        x=top_popular_routes['from_airport_code'] + '-' + top_popular_routes['dest_airport_code'],
        y='num_flights',
        labels={'x': 'Routes (From - To)', 'num_flights': 'Number of Flights'},
        title='Top 10 Most Popular Routes'
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis_title='Routes (From - To)',
        yaxis_title='Number of Flights',
        xaxis_tickangle=-45
    )
    
    # Show the plot
    fig.show()
    
    return top_popular_routes

def shortest_and_longest_routes(df_input):
    """
    Identifies the top 10 shortest and longest routes by average duration and creates bar plots.

    Args:
    df_input (pd.DataFrame): The flight data DataFrame.

    Returns:
    tuple: DataFrames containing the top 10 shortest and longest routes.
    """
    # Copy the input DataFrame
    df = df_input.copy()
    
    # Calculate the average duration for each route
    df_routes_duration = df.groupby(["city_of_departure", "city_of_arrival"])["duration_minutes"].mean()
    
    # Identify the shortest routes
    shortest_routes = pd.DataFrame(df_routes_duration.sort_values(ascending=True).head(10))
    
    # Identify the longest routes
    longest_routes = pd.DataFrame(df_routes_duration.sort_values(ascending=False).head(10))
    
    # Plotting the shortest routes
    plt.figure(figsize=(10, 6))
    shortest_routes.plot(kind='bar', legend=False)
    plt.title('Top 10 Shortest Routes')
    plt.xlabel('Routes (Departure to Arrival)')
    plt.ylabel('Average Duration (minutes)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()  # Show the plot for shortest routes
    
    # Plotting the longest routes
    plt.figure(figsize=(10, 6))
    longest_routes.plot(kind='bar', legend=False, color='red')
    plt.title('Top 10 Longest Routes')
    plt.xlabel('Routes (Departure to Arrival)')
    plt.ylabel('Average Duration (minutes)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()  # Show the plot for longest routes
    
    return shortest_routes, longest_routes

def correlation_price_distance(df_input):
    """
    Examines the correlation between ticket price and travel duration, and creates a scatter plot.

    Args:
    df_input (pd.DataFrame): The flight data DataFrame.

    Returns:
    float: The correlation coefficient between ticket price and travel duration.
    """
    # Copy the input DataFrame
    df = df_input.copy()
    
    # Calculate the correlation coefficient between ticket price and travel duration
    correlation_price_duration = df['price'].corr(df['duration_minutes'])
    print(f"Correlation between ticket price and travel duration: {correlation_price_duration}")

    # Create a scatter plot using Plotly
    fig = px.scatter(df, x='duration_minutes', y='price', 
                     title='Correlation between Ticket Price and Travel Duration',
                     labels={'duration_minutes': 'Duration (minutes)', 'price': 'Ticket Price'},
                     trendline='ols',  # Add OLS regression trendline
                     color='price',  # Color points by 'price'
                     color_continuous_scale='Viridis')  # Set color scale

    # Customize the layout
    fig.update_layout(
        xaxis_title='Duration (minutes)',
        yaxis_title='Ticket Price',
        title_x=0.5  # Center the title
    )

    # Show the plot
    fig.show()
    
    return correlation_price_duration

def co2_emissions_by_airline(df_input):
    """
    Compares the CO2 emissions of different airlines and creates a bar chart.

    Args:
    df_input (pd.DataFrame): The flight data DataFrame.

    Returns:
    pd.DataFrame: The DataFrame containing the total CO2 emissions by airline.
    """
    # Copy the input DataFrame
    df = df_input.copy()
    
    # Aggregate CO2 emissions by airline
    aggregated_data = df.groupby('airline_name')['co2_emissions'].sum().reset_index()

    # Sort airlines based on total emissions
    aggregated_data = aggregated_data.sort_values(by='co2_emissions', ascending=False)

    # Display aggregated data
    print(aggregated_data)

    # Create a bar chart using Plotly Express
    fig = px.bar(aggregated_data, x='airline_name', y='co2_emissions', 
                 title='CO2 Emissions by Airline',
                 labels={'airline_name': 'Airline', 'co2_emissions': 'Total CO2 Emissions'},
                 color='co2_emissions', color_continuous_scale='Viridis')

    # Customize layout
    fig.update_layout(
        xaxis_title='Airline',
        yaxis_title='Total CO2 Emissions',
        xaxis_tickangle=-45  # Rotate x-axis labels for better readability
    )

    # Show the plot
    fig.show()
    
    return aggregated_data

def co2_emissions_by_airport(df_input):
    """
    Assesses the total CO2 emissions associated with each airport and creates bar plots using Seaborn and Plotly.

    Args:
    df_input (pd.DataFrame): The flight data DataFrame.

    Returns:
    pd.DataFrame: The DataFrame containing the total CO2 emissions by airport.
    """
    # Copy the input DataFrame
    df = df_input.copy()

    # Create separate dataframes for departures and arrivals with an indicator column
    departures = df[['from_airport_code', 'co2_emissions']].copy()
    departures['type'] = 'departure'
    departures.columns = ['airport', 'co2_emissions', 'type']
    
    arrivals = df[['dest_airport_code', 'co2_emissions']].copy()
    arrivals['type'] = 'arrival'
    arrivals.columns = ['airport', 'co2_emissions', 'type']

    # Concatenate the departures and arrivals dataframes
    combined_data = pd.concat([departures, arrivals])
    
    # Create a pivot table to sum CO2 emissions for each airport
    pivot_table = pd.pivot_table(combined_data, values='co2_emissions', index='airport', aggfunc='sum').reset_index()
    
    # Sort by total CO2 emissions
    pivot_table = pivot_table.sort_values(by='co2_emissions', ascending=False)
    
    # Select top 15 airports by total CO2 emissions
    top_airports = pivot_table.nlargest(15, 'co2_emissions')

    # Create the bar plot using Seaborn
    plt.figure(figsize=(12, 8))
    sns.barplot(x='airport', y='co2_emissions', data=top_airports, palette='viridis')

    # Customize the plot
    plt.title('Top 15 Airports by Total CO2 Emissions')
    plt.xlabel('Airport')
    plt.ylabel('Total CO2 Emissions')

    # Rotate x-axis labels for better readability if needed
    plt.xticks(rotation=45, ha='right')

    # Show plot
    plt.tight_layout()
    plt.show()
    
    # Create the bar chart using Plotly Express
    fig = px.bar(top_airports, x='airport', y='co2_emissions', 
                 title='Top 15 Airports by Total CO2 Emissions',
                 labels={'co2_emissions': 'Total CO2 Emissions', 'airport': 'Airport'},
                 text='co2_emissions',
                 color='co2_emissions')

    # Customize the chart layout
    fig.update_layout(
        title='Top 15 Airports by Total CO2 Emissions',
        xaxis_title='Airport',
        yaxis_title='Total CO2 Emissions',
        uniformtext_minsize=8, uniformtext_mode='hide'
    )
    
    # Display the bar chart
    fig.show()
    
    return top_airports

