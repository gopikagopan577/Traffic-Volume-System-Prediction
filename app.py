import streamlit as st
import pandas as pd
import os
import joblib

if not os.path.exists("traffic_pipeline.pkl"):
    from train_model import train_and_save_model
    train_and_save_model()

model = joblib.load("traffic_pipeline.pkl")

st.set_page_config(page_title="Traffic Volume Prediction", layout="wide")

st.title("🚦 Traffic Volume Prediction System")



#extrat categories
preprocessor = model.named_steps["preprocessing"]
encoder = preprocessor.named_transformers_["cat"]

holiday_options = list(encoder.categories_[0])
weather_options = list(encoder.categories_[1])

#inputs
col1, col2 = st.columns(2)

with col1:
    date = st.date_input("📅 Select Date")
    hour = st.slider("🕒 Hour of Day", 0, 23, 8)

with col2:
    weather = st.selectbox("🌤 Weather Condition", weather_options)
    temp = st.number_input("🌡 Temperature (Kelvin)", value=290.0)

# date feature engineering
date = pd.to_datetime(date)
year = date.year
month = date.month
day = date.day
weekday = date.weekday()

st.info(f"📅 Day: {date.strftime('%A')}")

#auto holiday feature engineering
holiday_dict = {
    "01-01": "New Year's Day",
    "07-04": "Independence Day",
    "12-25": "Christmas Day",
    "11-11": "Veterans Day"
}

date_key = date.strftime("%m-%d")

if date_key in holiday_dict:
    holiday = holiday_dict[date_key]
else:
    holiday = "None"

st.info(f"🎉 Holiday: {holiday}")

#  weather feature engineering
if weather == "Rain":
    rain = 5
    snow = 0
    clouds = 90
elif weather == "Snow":
    rain = 0
    snow = 3
    clouds = 95
elif weather == "Clouds":
    rain = 0
    snow = 0
    clouds = 80
elif weather == "Clear":
    rain = 0
    snow = 0
    clouds = 10
else:
    rain = 0
    snow = 0
    clouds = 50



# prediction

predict_button = st.button("🚀 Predict Traffic Volume")


input_data = pd.DataFrame([{
        "temp": temp,
        "rain_1h": rain,
        "snow_1h": snow,
        "clouds_all": clouds,
        "Hour": hour,
        "Year": year,
        "Months": month,
        "day": day,
        "weekday": weekday,
        "holiday": holiday,
        "weather_main": weather
    }])
if predict_button:
    prediction = model.predict(input_data)[0]
    prediction_value = int(prediction)

    st.success(f"🚗 Predicted Traffic Volume: {prediction_value}")

    if prediction_value < 2000:
        st.success("🟢 Traffic Level: Low")
    elif prediction_value < 5000:
        st.warning("🟡 Traffic Level: Medium")
    else:
        st.error("🔴 Traffic Level: High")

import matplotlib.pyplot as plt
import numpy as np

if st.checkbox("📈 Show Feature Importance"):

    model_rf = model.named_steps["model"]

    importances = model_rf.feature_importances_

    feature_names = model.named_steps["preprocessing"].get_feature_names_out()

    indices = np.argsort(importances)[-10:]  # Top 10 features

    fig, ax = plt.subplots()
    ax.barh(range(len(indices)), importances[indices])
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels(np.array(feature_names)[indices])
    ax.set_title("Top 10 Feature Importances")

    st.pyplot(fig)        