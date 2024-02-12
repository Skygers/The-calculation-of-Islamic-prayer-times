# The-calculation-of-Islamic-prayer-times

The IslamicPrayerTimesCalculator repository a calculation for accurately calculating Islamic prayer times. This repository houses advanced algorithms and methods designed to precisely determine the five daily prayer timings based on geographical, astronomical coordinates and calendar dates.

**The Method Contain:**

1. **Conversion of Calendar Gregorian (Anno Domini) to Julian Day:**
   Our repository provides robust functions for seamlessly converting dates from the Gregorian (Anno Domini) calendar to Julian Day format. This crucial conversion facilitates precise astronomical calculations necessary for determining prayer times. You can see the conversion in `KonversiJD.py`

2. **Transformation Coordinate system:**
   The calculation of tansformation of celestial coordinates between various coordinate systems.
   1. **Ecliptic to Equatorial Transformation**: Algorithms for converting celestial coordinates from the Geocentric Ecliptical Coordinate system to the Geocentric Equatorial coordinate system.
   ![alt text](https://github.com/Skygers/The-calculation-of-Islamic-prayer-times/blob/b50118095e5fa2e70501076f84dcb7552d88aa37/Images/Geosentris%20eklip.PNG)
   2. **Equatorial to Ecliptic Transformation**: convert celestial coordinates from the equatorial system to the ecliptic system.
   ![alt text](https://github.com/Skygers/The-calculation-of-Islamic-prayer-times/blob/b50118095e5fa2e70501076f84dcb7552d88aa37/Images/Geosentris%20ekuator.PNG)
   3. **Equatorial to Horizon Transformation**: This conversion facilitates practical observation and navigation by providing the apparent positions of celestial objects as they appear from a specific location on Earth's surface, accounting for local observer parameters such as latitude, longitude, and time.
![alt text](https://github.com/Skygers/The-calculation-of-Islamic-prayer-times/blob/b50118095e5fa2e70501076f84dcb7552d88aa37/Images/Horizon.PNG)
3. **Calculation of Sun Declination Angle:**
   The sun's declination angle plays a pivotal role in establishing the position of the sun relative to the Earth's equator. Our repository includes advanced methods for computing the sun's declination angle, considering factors such as the Earth's axial tilt and orbital position.

4. **Accurate Prayer Time Calculation:**
   Leveraging the calculated day angle and sun declination angle, our repository employs precise formulas endorsed by leading Islamic scholars and institutions to determine the five daily prayer times: Fajr (Pre-Dawn), Dhuhr (Noon), Asr (Afternoon), Maghrib (Evening), and Isha (Night).

5. **Graphical User Interface (GUI) Prayer Time Calculation:**
   GUI toolset offers flexibility for users to input their geographical coordinates, enabling personalized calculations tailored to specific locations worldwide.
   ![alt text](https://github.com/Skygers/The-calculation-of-Islamic-prayer-times/blob/b50118095e5fa2e70501076f84dcb7552d88aa37/Images/GUI.PNG)
