# Sky Track

## Overview
**Sky Track**offers advanced data analytics services to the aviation industry, focusing on the environmental impacts of CO2 emissions. Our insights, derived from detailed flight data analysis, help identify the most pollutant routes, aircraft types, and airports, enabling more sustainable decision-making.

## Table of Contents
1. [Project Setup](#project-setup)
2. [Data Sources](#data-sources)
3. [Data Preparation](#data-preparation)
4. [Data Cleaning](#data-cleaning)
5. [Core Analyses](#core-analyses)
6. [Results](#results)
7. [Exploratory Data Analysis](#exploratory-data-analysis)
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

## Core Analyses

1. **Most Pollutant Routes**
    - **Analysis**: Long haul routes produce significantly more CO2 emissions compared to others.

2. **Most Polluting Aircraft Types**
    - **Analysis**: Larger aircraft types emit more CO2 compared to smaller aircraft types.

3. **CO2 Emissions by Airline**
    - **Analysis**: Low-cost airlines emit less CO2 per flight compared to premium airlines.
  
4. **CO2 Emissions by Airport**
    - **Analysis**: Major international airports contribute more to CO2 emissions compared to regional airports.

## Results:

1. **Most Pollutant Routes**:
    - **Approach**: Sum CO2 emissions for all flights on each route, then rank them to find the most polluting routes.
    - The table reveals that routes between Mumbai and Delhi top the list with over 51 million kg of CO2 emissions each. Other significant routes include Melbourne to Sydney, Delhi to Bangalore, and Sydney to Melbourne, each with emissions around 47-48 million kg. Major hubs such as Mumbai, Delhi, Melbourne, Sydney, and Shanghai are key contributors to high CO2 emissions, indicating substantial environmental impact from flights originating there. Frequent destination cities with high emissions include Delhi, Sydney, Singapore, and London, highlighting significant air traffic between these hubs and various departure cities.
![Top 20 Most Pollutant Routes by CO2 Emissions](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/Top%2020%20most%20pollutant%20routes%20.png)

2. **Most Polluting Aircraft Types**:
    - **Approach**: Aggregate CO2 emissions by aircraft type and identify which types have the highest emissions.
    - The bar graph reveals that the Boeing 777 is the most polluting aircraft type, with CO2 emissions exceeding 600 million kg. It is followed closely by the Boeing 787 and Airbus A320, both of which also have high emissions. Other significant contributors include the Boeing 737 and Airbus A330. The data indicates that Boeing and Airbus aircraft dominate the list of top 20 most polluting aircraft types, highlighting the substantial environmental impact of these widely used models. Notably, aircraft like the Airbus A350, Airbus A319, and Airbus A380 also appear in the top ranks, suggesting that larger, long-haul aircraft are significant contributors to CO2 emissions in the aviation industry.
![Top 20 Most Polluting Aircrafts](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/Top%2020%20most%20polluting%20aircraft%20types.png)

3. **CO2 Emissions by Airline**:
    - **Approach**: Aggregate CO2 emissions data by airline and analyze their relative environmental impact.
    - The bar graph indicates that Lufthansa is the airline with the highest CO2 emissions, exceeding 300 million kg. Following Lufthansa, China Southern, China Eastern, and Delta also exhibit significant CO2 emissions, with each airline emitting over 200 million kg. Other notable contributors include Qantas, Hainan, and Xiamen Air. The data suggests that large, international airlines are major contributors to aviation-related CO2 emissions, with a sharp drop-off in emissions among smaller or regional airlines. Addressing emissions in these top airlines could have a substantial impact on reducing the overall carbon footprint of the aviation industry.
![Top 20 Most Polluting Aircrafts](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/C02%20emissions%20by%20airline.png)

4. **CO2 Emissions by Airport**:
    - **Approach**: Sum the CO2 emissions for all departures and arrivals at each airport.
    - The bar graph reveals that Charles de Gaulle Airport (CDG) in Paris has the highest total CO2 emissions, followed closely by Frankfurt Airport (FRA) and Delhi Airport (DEL), each emitting over 400 million kg of CO2. Other notable airports with high emissions include Toronto Pearson Airport (YYZ), São Paulo–Guarulhos Airport (GRU), and Sydney Airport (SYD). This data indicates that major international hubs, particularly in Europe, Asia, and South America, are significant contributors to aviation-related CO2 emissions. Efforts to mitigate emissions at these key airports could have a substantial impact on reducing the overall carbon footprint of global air travel.
![Top 20 Most Polluting Aircrafts](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/Top%2010%20most%20polluting%20airports.png)

## Exploratory Data Analysis

1. **Most Popular Routes**
    - **Analysis**: The most popular routes are typically short-haul flights.
    - **Approach**: Count the number of flights for each route and rank them.
    - The funnel chart shows that the most popular flight routes are primarily domestic, with Melbourne to Sydney (488 flights) and Sydney to Melbourne (485 flights) leading, highlighting significant air traffic between these Australian cities. Other highly trafficked routes include Mumbai to Delhi and Delhi to Mumbai (each with 364 flights), reflecting major domestic travel within India. Additionally, routes such as Delhi to Bangalore (252 flights) and several routes within China, like Shanghai to Beijing and Shanghai to Shenzhen, indicate strong connectivity and frequent travel between these key cities.
![Top 20 Most Polluting Aircrafts](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/Top%2010%20most%20populat%20routes.png)

2. **Shortest and Longest Routes**
    - **Analysis**: Identify routes with minimum and maximum distances.
    - **Approach**: Use the distance data to identify the shortest and longest routes.
    -  The bar graphs show the average duration of the shortest and longest flight routes. The shortest routes, such as Frankfurt to Munich, Brussels to Paris, and Frankfurt to Zurich, have an average duration of around 50-60 minutes, indicating quick domestic or short international hops within Europe. Conversely, the longest routes, such as Delhi to Chicago, Delhi to New York, and Delhi to Toronto, have average durations close to 1,000 minutes, reflecting extensive long-haul flights primarily between major cities in different continents. This contrast highlights the significant variation in travel times and distances between short-haul and long-haul flights.
![Top 20 Most Polluting Aircrafts](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/Top%2010%20shortest%20routes.png)
![Top 20 Most Polluting Aircrafts](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/Top%2010%20longest%20routes.png)

3. **Correlation Between Price and Distance**
    - **Analysis**: Ticket prices increase with the distance traveled.
    - **Approach**: Calculate the correlation coefficient between ticket price and distance traveled.
    - The scatter plot demonstrates a positive correlation between ticket price and travel duration, with a correlation coefficient of approximately 0.71. This indicates a moderate to strong relationship, suggesting that as the duration of a flight increases, the ticket price tends to increase as well. While there is some variability, with a few outliers showing high prices for shorter durations, the overall trend line confirms that longer flights generally cost more, reflecting factors such as increased fuel consumption, operational costs, and possibly higher demand for longer routes. 
![Top 20 Most Polluting Aircrafts](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/Correlation%20between%20price%20and%20duration.png)

4. **Correlation Between Ticket Price and CO2 Emissions**
    - **Analysis**: Flights with higher ticket prices are associated with higher CO2 emissions.
    -  **Approach**: Calculate the correlation coefficient between ticket price and CO2 emissions.
    -  The scatter plot indicates a positive correlation between ticket price and CO2 emissions, with a correlation coefficient of approximately 0.75. This suggests a strong relationship, where higher ticket prices are associated with higher CO2 emissions. The trend line shows that as ticket prices increase, CO2 emissions also tend to increase, which may reflect that longer or more premium flights, which typically cost more, also result in greater CO2 emissions due to increased fuel consumption and operational factors. This relationship underscores the environmental impact of higher-priced, likely longer-distance air travel.
![Top 20 Most Polluting Aircrafts](https://github.com/Josepdmo/big-project-number-1/blob/main/Images/Correlation%20between%20Price%20and%20CO2%20Emissions.png)

5. **Fuel Consumption by Aircraft Type**
    - **Additional Data Required**: Fuel consumption rates for different aircraft types.
    - **Analysis**: Combine fuel consumption data with distance traveled to calculate fuel efficiency and emissions.
    - **Approach**: Use the additional fuel consumption data to calculate the fuel consumption for each flight based on its aircraft type and distance, then analyze the results.

## Conclusions

- Overall, the Sky Track project highlights the critical need for the aviation industry to adopt sustainable practices and technologies. By focusing on the most pollutant routes, aircraft, airlines, and airports, stakeholders can make informed decisions to reduce CO2 emissions, contributing to a more sustainable future for air travel. The insights derived from this analysis provide a foundation for ongoing efforts to minimize the environmental impact of aviation, ensuring that growth in air travel does not come at the expense of our planet's health.

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


