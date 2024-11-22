import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Sekme başlığı ve simgesi ayarları
st.set_page_config(
    page_title="Weather of Turkey",
    page_icon=":umbrella_with_rain_drops:"
)

# WeatherAPI bilgileri
API_KEY = "f57182df55a24880b18120822242211"  # WeatherAPI'den aldığınız API Key
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

# City list
# Türkiye'deki tüm şehirler ve plaka kodları
cities = [
    "01 Adana", "02 Adıyaman", "03 Afyonkarahisar", "04 Ağrı", "05 Amasya",
    "06 Ankara", "07 Antalya", "08 Artvin", "09 Aydın", "10 Balıkesir",
    "11 Bilecik", "12 Bingöl", "13 Bitlis", "14 Bolu", "15 Burdur",
    "16 Bursa", "17 Çanakkale", "18 Çankırı", "19 Çorum", "20 Denizli",
    "21 Diyarbakır", "22 Edirne", "23 Elazığ", "24 Erzincan", "25 Erzurum",
    "26 Eskişehir", "27 Gaziantep", "28 Giresun", "29 Gümüşhane", "30 Hakkari",
    "31 Hatay", "32 Isparta", "33 Mersin", "34 İstanbul", "35 İzmir",
    "36 Kars", "37 Kastamonu", "38 Kayseri", "39 Kırklareli", "40 Kırşehir",
    "41 Kocaeli", "42 Konya", "43 Kütahya", "44 Malatya", "45 Manisa",
    "46 Kahramanmaraş", "47 Mardin", "48 Muğla", "49 Muş", "50 Nevşehir",
    "51 Niğde", "52 Ordu", "53 Rize", "54 Sakarya", "55 Samsun",
    "56 Siirt", "57 Sinop", "58 Sivas", "59 Tekirdağ", "60 Tokat",
    "61 Trabzon", "62 Tunceli", "63 Şanlıurfa", "64 Uşak", "65 Van",
    "66 Yozgat", "67 Zonguldak", "68 Aksaray", "69 Bayburt", "70 Karaman",
    "71 Kırıkkale", "72 Batman", "73 Şırnak", "74 Bartın", "75 Ardahan",
    "76 Iğdır", "77 Yalova", "78 Karabük", "79 Kilis", "80 Osmaniye", "81 Düzce"
]

# Şehir seçimi
selected_city = st.selectbox("Choose a city (with plate number):", cities)

# Şehir adını seçmek için plaka numarasını kaldırma
selected_city_name = " ".join(selected_city.split(" ")[1:])  # "01 Adana" -> "Adana"


# Streamlit title and dropdown menu
st.title("Weekly Weather Forecast")
st.write("Select a city from the dropdown menu to see the weekly weather forecast in a table and a graph.")

# City selection
selected_city = st.selectbox("Choose a city:", cities)

if selected_city:
    # API parametreleri
    params = {
        "key": API_KEY,
        "q": selected_city_name,
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