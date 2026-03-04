import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor

def train_and_save_model():

    df = pd.read_csv("Metro_Interstate_Traffic_Volume.csv")

    df["date_time"] = pd.to_datetime(df["date_time"])

    df["Hour"] = df["date_time"].dt.hour
    df["Year"] = df["date_time"].dt.year
    df["Months"] = df["date_time"].dt.month
    df["day"] = df["date_time"].dt.day
    df["weekday"] = df["date_time"].dt.weekday

    numeric_cols = ['temp','rain_1h','snow_1h','clouds_all','Hour','Year','Months','day','weekday']
    categorical_cols = ['holiday','weather_main']

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

    model = RandomForestRegressor(
        n_estimators=80,
        max_depth=15,
        random_state=42
    )

    pipeline = Pipeline([
        ('preprocessing', preprocessor),
        ('model', model)
    ])

    pipeline.fit(df[numeric_cols + categorical_cols], df['traffic_volume'])

    joblib.dump(pipeline, "traffic_pipeline.pkl", compress=3)

    print("Model trained and saved.")