import streamlit as st
import requests

# Sekme başlığı ve simgesi ayarları
st.set_page_config(
    page_title="Weather of the World",
    page_icon=":umbrella_with_rain_drops:"
)

# WeatherAPI bilgileri
API_KEY = "f57182df55a24880b18120822242211"  # WeatherAPI'den aldığınız API Key
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

# Şehir listesi (örnek olarak bazı şehirler)
cities = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Trabzon", "Diyarbakır"]

# Streamlit başlık ve seçim menüsü
st.title("Haftalık Hava Durumu Tahmini")
st.write("Aşağıdaki listeden bir şehir seçerek hava durumu tahminini görebilirsiniz.")

# Şehir seçimi
selected_city = st.selectbox("Bir şehir seçin:", cities)

if selected_city:
    # API isteği için parametreler
    params = {
        "key": API_KEY,
        "q": selected_city,
        "days": 7,  # 7 günlük tahmin
        "lang": "tr"
    }
    
    try:
        # API isteği
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            # Hava durumu tahminlerini göster
            st.subheader(f"{selected_city} için Haftalık Hava Durumu Tahmini")
            forecast_days = data["forecast"]["forecastday"]
            
            for day in forecast_days:
                date = day["date"]
                condition = day["day"]["condition"]["text"]
                max_temp = day["day"]["maxtemp_c"]
                min_temp = day["day"]["mintemp_c"]
                
                st.write(f"📅 **{date}**")
                st.write(f"- Durum: {condition}")
                st.write(f"- En Yüksek Sıcaklık: {max_temp}°C")
                st.write(f"- En Düşük Sıcaklık: {min_temp}°C")
                st.write("---")  # Bölme çizgisi
        else:
            st.error(f"Hata: {data.get('error', {}).get('message', 'Bilinmeyen bir hata oluştu')}")
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")

