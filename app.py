import streamlit as st
import requests
import pandas as pd

# Sekme başlığı ve simgesi ayarları
st.set_page_config(
    page_title="Weather of the World",
    page_icon=":umbrella_with_rain_drops:"
)

# WeatherAPI bilgileri
API_KEY = "f57182df55a24880b18120822242211"  # WeatherAPI'den aldığınız API Key
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

# City list
cities = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana", "Trabzon", "Diyarbakir"]

# Streamlit title and dropdown menu
st.title("Weekly Weather Forecast")
st.write("Select a city from the dropdown menu to see the weekly weather forecast in a table and a graph.")

# City selection
selected_city = st.selectbox("Choose a city:", cities)

if selected_city:
    # API request parameters
    params = {
        "key": API_KEY,
        "q": selected_city,
        "days": 7,  # 7-day forecast
        "lang": "en"  # English language
    }
    
    try:
        # API request
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            # Prepare weather forecast data
            forecast_days = data["forecast"]["forecastday"]
            weather_data = []

            for day in forecast_days:
                date = day["date"]
                condition = day["day"]["condition"]["text"]
                icon_url = day["day"]["condition"]["icon"]  # Weather icon
                max_temp = day["day"]["maxtemp_c"]
                min_temp = day["day"]["mintemp_c"]

                weather_data.append({
                    "Date": date,
                    "Condition": f"{condition} ![icon]({icon_url})",
                    "Max Temp (°C)": max_temp,
                    "Min Temp (°C)": min_temp
                })

            # Convert to DataFrame
            df = pd.DataFrame(weather_data)

            # Display table
            st.subheader(f"Weekly Weather Forecast for {selected_city}")
            st.table(df)  # Display as a table

            # Display line chart
            st.subheader("Temperature Trends")
            st.line_chart(df[["Max Temp (°C)", "Min Temp (°C)"]])
        else:
            st.error(f"Error: {data.get('error', {}).get('message', 'Unknown error occurred')}")
    except Exception as e:
        st.error(f"An error occurred: {e}")