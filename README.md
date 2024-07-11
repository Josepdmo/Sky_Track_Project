# Sky Track

## Overview
**Sky Track** is a data analytics project aimed at providing insights into the aviation industry's flight routes, CO2 emissions, and other relevant metrics. This project analyzes flight data from April to August 2022 to identify the most pollutant routes, aircraft types, and more. 

## Table of Contents
1. [Project Setup](#project-setup)
2. [Data Sources](#data-sources)
3. [Data Preparation](#data-preparation)
4. [Data Cleaning](#data-cleaning)
5. [Hypotheses and Analyses](#hypotheses-and-analyses)
6. [Exploratory Data Analysis](#exploratory-data-analysis)
7. [Results](#results)
8. [Conclusions](#conclusions)
9. [How to Use](#how-to-use)
10. [Future Work](#future-work)

## Project Setup

1. **Create and Activate the Environment**
    ```bash
    conda create --name sky_track_2022 python=3.8
    conda activate sky_track_2022
    ```

2. **Install Required Libraries**
    ```bash
    pip install pandas seaborn matplotlib plotly requests beautifulsoup4 gdown
    ```

## Data Sources

- **Flight Data**: CSV file containing information on 1 million flights between April and August 2022 (sourced from Kaggle).
- **Airport Code Data**: CSV document listing airport codes and their corresponding cities.
- **Aircraft Fuel Consumption**: Table detailing the fuel used per aircraft model from the 930km to the 1267km range.

## Data Preparation

### Merging Dataframes:
- Merge columns 'city' and 'three-digit code' from the Airport Codes Dataframe into the main dataframe.
- Merge the two dataframes to display the city corresponding to each airport code.

## Data Cleaning

1. **Remove Layover Flights**
    - Drop rows with layovers to ensure accurate analysis of flight duration and emissions.

2. **Rename Columns**
    - Rename the duration column to indicate it is measured in minutes.

3. **Handle Missing Data**
    - Remove rows without CO2 emissions data and fill null values in `avg_co2_emission_for_this_route` and `co2_percentage`.

4. **Manual Data Entry**
    - Insert the missing airport code for Doha (DOH) into the dataframe.

## Hypotheses and Analyses

1. **Most Pollutant Routes in Summer 2022**
    - **Analysis**: Calculate and rank total CO2 emissions for each route.

2. **Most Polluting Aircraft Types**
    - **Analysis**: Aggregate CO2 emissions by aircraft type to identify the highest emitters.

7. **CO2 Emissions by Airline**
    - **Analysis**: Aggregate and compare CO2 emissions by airline.
  
8. **CO2 Emissions by Airport**
    - **Analysis**: Sum CO2 emissions for all departures and arrivals at each airport.

4. **Most Popular Routes**
    - **Analysis**: Count and rank the number of flights for each route.

5. **Shortest and Longest Routes**
    - **Analysis**: Identify routes with minimum and maximum distances.

6. **Correlation Between Price and Distance**
    - **Analysis**: Calculate the correlation coefficient between ticket price and distance.

3. **Correlation Between Ticket Price and CO2 Emissions**
    - **Analysis**: Calculate the correlation coefficient between ticket price and CO2 emissions.

9. **Fuel Consumption by Aircraft Type**
    - **Additional Data Required**: Fuel consumption rates for different aircraft types.
    - **Analysis**: Combine fuel consumption data with distance traveled to calculate fuel efficiency and emissions.

## Exploratory Data Analysis

- Generate summary statistics and visualizations to understand the distributions and relationships in the data.

### Detailed Analyses:

1. **Most Pollutant Routes in Summer 2022**:
    - **Approach**: Sum CO2 emissions for all flights on each route, then rank them to find the most polluting routes.
![Top 20 Most Pollutant Routes by CO2 Emissions](images/top_pollutant_routes.png)

This graph shows the top 20 most pollutant routes by CO2 emissions.


2. **Most Polluting Aircraft Types**:
    - **Approach**: Aggregate CO2 emissions by aircraft type and identify which types have the highest emissions.

3. **CO2 Emissions by Airline**:
    - **Approach**: Aggregate CO2 emissions data by airline and analyze their relative environmental impact.

4. **CO2 Emissions by Airport**:
    - **Approach**: Sum the CO2 emissions for all departures and arrivals at each airport.

5. **Most Popular Routes**:
    - **Approach**: Count the number of flights for each route and rank them.

6. **Shortest and Longest Routes**:
    - **Approach**: Use the distance data to identify the shortest and longest routes.

7. **Correlation Between Price and Distance**:
    - **Approach**: Calculate the correlation coefficient between ticket price and distance traveled.

8. **Correlation Between Ticket Price and CO2 Emissions**:
    - **Approach**: Calculate the correlation coefficient between ticket price and CO2 emissions.

9. **Fuel Consumption by Plane Type**:
    - **Approach**: Use the additional fuel consumption data to calculate the fuel consumption for each flight based on its aircraft type and distance, then analyze the results.

## Results

- Present the findings from each analysis, supported by graphs and charts created for each hypothesis.

## Conclusions

- Summarize the key insights and recommendations derived from the analyses. Why Both Metrics Are Important
Operational Efficiency: Fuel consumption helps in optimizing flight operations and reducing costs.
Environmental Impact: CO2 emissions are crucial for understanding and mitigating the environmental impact, and for complying with environmental regulations.
Different Focuses: While fuel consumption is more about operational efficiency, CO2 emissions focus on environmental sustainability.
Practical Example
Fuel Consumption Data: If an aircraft consumes 5 liters of fuel per kilometer, this data is used for calculating operational costs and planning refueling needs.
CO2 Emissions Data: If burning 1 liter of fuel produces 2.5 kg of CO2, then the aircraft emits 12.5 kg of CO2 per kilometer (5 liters * 2.5 kg CO2/liter). This data is used for reporting environmental impact and adhering to carbon regulations.
Conclusion
While fuel consumption and CO2 emissions are closely related and one can be derived from the other, they serve different purposes. Fuel consumption focuses on operational and cost efficiency, while CO2 emissions are critical for environmental impact assessment and sustainability goals. Therefore, they are not redundant but complementary metrics.

1. Data Analytics Service for Aviation Industry
Pros:

Comprehensive Scope: Involves various types of analyses such as route popularity, route optimization, pricing strategies, and market trends.
High Impact: Provides actionable insights for airlines, airports, and travel agencies to make data-driven decisions.
Technical Depth: Likely to involve sophisticated data analysis techniques and tools, including possibly machine learning for route optimization.
Versatility: Demonstrates a wide range of data analytics skills, from exploratory data analysis to predictive modeling.
  
## How to Use

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/sky-track.git
    cd sky-track
    ```

2. **Install Required Libraries**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Analysis**:
    - Execute the Python scripts or Jupyter Notebook to reproduce the analysis.

## Future Work

- Integrate real-time data analysis.
- Develop predictive models for flight delays and pricing.
- Expand the scope to include additional environmental impact metrics.

## Visualizations

![Popular Routes](images/popular_routes.png)
![Price Distance Correlation](images/price_distance_correlation.png)

---

**Sky Track** demonstrates the use of data analytics to derive meaningful insights and provide actionable recommendations for the aviation industry.


