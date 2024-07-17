# **RESI: One Click for Future Building Energy Simulation**

**Welcome to the RESI: RESIlient Community!**

Seven years ago, when I was a master student and read my first journal article in our field. Most paper began with the statement “building accounts for **30%** of energy consumption in the world”, however, this number has not decreased until now. I was always curious about the reasons behind this and realized that scalability is one of the major barriers, not just in modeling, but also in data acquisition, control optimization, retrofit, and implementation.

I was always wondering if there was anything I could do to simplify these processes. This motivated me to develop RESI, a modular-oriented platform where everything is modularized, allowing users to create a pipeline like Lego plug-and-play easily.

--------------------------------------------------------------------------------------------------------------------------
## **MODULE1: Future Weather Data Module**
![image](https://github.com/Bugs-Owner/RESI-One-click-for-future-building-energy-simulation/assets/155193713/df75571b-f3e5-4e84-82f8-aeb42d1d90df)

This module provides future weather data for the years 2045-2054 and 2085-2094. It includes:

    Typical Meteorological Year (TMY)

    Extreme Warm Year (EWY)

    Extreme Cold Year (ECY)

    Specific Heat Wave Events

The data is available in both EPW format and as a pandas DataFrame.

Here's how to use it:

Step 1: Installation <The latest version has been updated to 2.0.9>

    pip install ResiSim==2.0.9

Step 2: Import

    import ResiSim   

Step 3: Query

    epw, df, heat_wave, Spic, Sdeb, Sint = ResiSim.Main.weather_query(city='Syracuse', time_span='Mid-term', sce='TMY') 
    
Step 4: You can save this file locally like this:

    with open('test.epw', 'wb') as file:
        file.write(epw) 
        
Step 5: Detection, you can use this function to find heat wave events for your own dataset

    heat_wave = ResiSim.Main.find_heat_wave_events(df) 

    
For *city*:

I integrated Google Geocoding, so ideally, you can type any location in the U.S., and you will get weather data for the nearest city.

For *time_span*, use:

"Mid-term" for 2045-2054
"Long-term" for 2085-2094

For *sce*, we have:

"TMY" (Typical Meteorological Year)
"EWY" (Extreme Warm Year)
"ECY" (Extreme Cold Year)
"All" (All raw data)

Citation:

Jiang, Z., & Dong, B. (2024). RESI: A Power Outage Event and Typical Weather File Generator For Future RESIlient Building Design and Operation.

## **MODULE2: Power Outage Module**
![image](https://github.com/user-attachments/assets/39390072-3fa7-48df-a6eb-a3aa29d7bd70)
![image](https://github.com/user-attachments/assets/79def810-30df-4032-ace9-287e8dc24d72)
![image](https://github.com/user-attachments/assets/0af72099-70cf-4b60-90fa-492c99f6c927)

This module provides Power Outage data for U.S. from 2002 to 2023.

Step 1: Query

    Outage_df = ResiSim.Main.outage_query()
    Outage_mcmc = ResiSim.Main.outage_mcmc(Outage_df, sample_size=1500, time_window=5)

For *sample_size*:

MCMC sample size

For *time_window*:

the time range you want to sample

## **MODULE3: Modularized Neural Network Incorporating Physical Priors**
Import and run, you will get a data-driven building energy model, which can be used for dynamic modeling, control optimization, energy calculation, and retrofit. Local test ongoing...
![image](https://github.com/user-attachments/assets/537740b0-7bba-4223-b05e-a59fc61e92f7)
