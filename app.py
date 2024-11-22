import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

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
    # API parametreleri
    params = {
        "key": API_KEY,
        "q": selected_city,
        "days": 7,  # 7 günlük tahmin
        "lang": "en"  # Dil: İngilizce
    }

    try:
        # API isteği
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            # Hava durumu tahminlerini işleme
            forecast_days = data["forecast"]["forecastday"]
            weather_data = []

            for day in forecast_days:
                date = day["date"]
                day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")  # Haftanın günü
                condition = day["day"]["condition"]["text"]
                icon_url = day["day"]["condition"]["icon"]  # Hava durumu ikonu
                max_temp = round(day["day"]["maxtemp_c"], 1)  # En yüksek sıcaklık
                min_temp = round(day["day"]["mintemp_c"], 1)  # En düşük sıcaklık

                weather_data.append({
                    "Date": date,
                    "Day": day_name,  # Haftanın günü
                    "Condition": f"<img src='{icon_url}' width='30' style='vertical-align:middle;'> {condition}",
                    "Max Temp (°C)": max_temp,
                    "Min Temp (°C)": min_temp
                })

            # DataFrame'e dönüştürme
            df = pd.DataFrame(weather_data)

            # Tabloyu HTML ile gösterme
            def render_html_table(dataframe):
                return dataframe.to_html(escape=False, index=False)

            st.subheader(f"Weekly Weather Forecast for {selected_city}")
            st.markdown(render_html_table(df), unsafe_allow_html=True)

            # Plotly ile grafik oluşturma
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df["Day"],  # X ekseni haftanın günleri
                    y=df["Max Temp (°C)"],
                    mode="lines+markers",
                    name="Max Temp (°C)"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df["Day"],  # X ekseni haftanın günleri
                    y=df["Min Temp (°C)"],
                    mode="lines+markers",
                    name="Min Temp (°C)"
                )
            )

            # Ekseni yatay olarak etiketleme
            fig.update_layout(
                title="Temperature Trends",
                xaxis_title="Day",
                yaxis_title="Temperature (°C)",
                xaxis=dict(tickangle=0),  # X ekseni etiketlerini yatay göster
                template="simple_white"
            )

            # Grafiği Streamlit'te göster
            st.plotly_chart(fig)
        else:
            st.error(f"Error: {data.get('error', {}).get('message', 'Unknown error occurred')}")
    except Exception as e:
        st.error(f"An error occurred: {e}")