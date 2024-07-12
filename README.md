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

Step 1: Installation

    pip install ResiSim==1.0.6

Step 2: Import

    import ResiSim   

Step 3: Query

    epw, df, heat_wave = ResiSim.Main.query(city='Syracuse', time_span='Mid-term', sce='TMY') 
    
Step 4: You can save this file locally like this:

    with open('test.epw', 'wb') as file:
        file.write(epw) 
    
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
## **MODULE2: Modularized Neural Network Incorporating Physical Priors**
Import and run, you will get a data-driven building energy model, which can be used for dynamic modeling, control optimization, energy calculation, and retrofit. Local test ongoing...
![image](https://github.com/user-attachments/assets/537740b0-7bba-4223-b05e-a59fc61e92f7)
