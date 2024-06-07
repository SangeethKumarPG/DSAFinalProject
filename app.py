import tensorflow
import pandas as pd
import numpy as np
import sklearn
import joblib
from flask import Flask, render_template, request
# from transformer import label_encode_transformer
from sklearn.preprocessing import LabelEncoder

# Example of a label encoding transformer function
def label_encode_transformer(X):
    encoded_df = pd.DataFrame(X).copy()
    for col in encoded_df.columns:
        le = LabelEncoder()
        encoded_df[col] = le.fit_transform(encoded_df[col])
    return encoded_df


app = Flask(__name__)
@app.route("/")
def home():
    diaster_subgroups = ['Meteorological', 'Hydrological', 'Geophysical', 'Climatological']
    disaster_subtypes = ['Cold wave', 'Flood (General)', 'Ground movement', 'Forest fire',
       'Tornado', 'Storm (General)', 'Tropical cyclone', 'Flash flood',
       'Drought', 'Coastal flood', 'Severe weather', 'Tsunami', 'Hail',
       'Riverine flood', 'Heat wave', 'Blizzard/Winter storm',
       'Sand/Dust storm', 'Lightning/Thunderstorms',
       'Severe winter conditions']
    disaster_types = ['Extreme temperature', 'Flood', 'Earthquake', 'Wildfire', 'Storm',
       'Drought']
    iso_codes = ['IND', 'PHL', 'IDN', 'YMD', 'MMR', 'IRN', 'THA', 'NPL', 'JPN',
       'KOR', 'PAK', 'LKA', 'TUR', 'TWN', 'YMN', 'HKG', 'SAU', 'MYS',
       'ISR', 'CYP', 'CHN', 'MDV', 'BGD', 'JOR', 'IRQ', 'YEM', 'LAO',
       'MNG', 'MAC', 'BTN', 'AZE', 'GEO', 'KAZ', 'VNM', 'KHM', 'KGZ',
       'ARM', 'KWT', 'BRN', 'SYR', 'TJK', 'OMN', 'TLS', 'AFG', 'PSE',
       'UZB', 'LBN', 'ARE', 'QAT']
    sub_regions = ['Southern Asia', 'South-eastern Asia', 'Western Asia',
       'Eastern Asia', 'Central Asia']



    return render_template("index.html",params = {
        "subgroups":diaster_subgroups,
        "subtypes":disaster_subtypes,
        "types":disaster_types,
        "iso":iso_codes,
        "subregion":sub_regions
    })


@app.route("/predict", methods=["POST"])
def predict_cpi():
   if request.method == "POST":
      error_message = ""
      disaster_subgroup = request.form["disaster_subgroup"]
      disaster_subtype = request.form["disaster_subtype"]
      disaster_type = request.form["disaster_type"]
      disaster_subregion = request.form["disaster_subregion"]
      disaster_iso = request.form["disaster_iso"]
      disaster_year = int(request.form["disaster_year"])
      disaster_total_affected = int(request.form["disaster_total_affected"])
      disaster_total_deaths = int(request.form["disaster_total_deaths"])
      magnitude_scale = request.form["magnitude_scale"]
      if magnitude_scale == "degree":
         magnitude_degree_celcius = float(request.form["diaster_magnitude"])
         magnitude_km_square = 0.0
         magnitude_richter = 0.0
         magnitude_kph = 0.0
      elif magnitude_scale == "km2":
         magnitude_degree_celcius = 0.0
         magnitude_km_square = float(request.form["diaster_magnitude"])
         magnitude_richter = 0.0
         magnitude_kph = 0.0
      elif magnitude_scale == "kmph":
         magnitude_degree_celcius = 0.0
         magnitude_km_square = 0.0
         magnitude_richter = 0.0
         magnitude_kph = float(request.form["diaster_magnitude"])
      elif magnitude_scale == "richter":
         magnitude_degree_celcius = 0.0
         magnitude_km_square = 0.0
         magnitude_richter = float(request.form["diaster_magnitude"])
         magnitude_kph = 0.0
      else:
         error_message = "Invalid scale"
      loaded_model = tensorflow.keras.models.load_model("simple_dense_model_full_data.keras", compile=False)
      print("Model loaded")
      preprocessor = joblib.load("preprocessor.joblib")
      print("Loaded preprocessor")
      X = [disaster_subgroup,disaster_type, disaster_subtype,
            disaster_iso, disaster_subregion, disaster_year,
            disaster_total_deaths, disaster_total_affected,
            magnitude_degree_celcius, magnitude_km_square,
            magnitude_richter, magnitude_kph]
      prediction_features = pd.DataFrame([X], columns=["Disaster Subgroup", "Disaster Type","Disaster Subtype","ISO",
      "Subregion","Start Year","Total Deaths","Total Affected","magnitude_degree_celcius", "magnitude_km_square", "magnitude_richter","magnitude_kph"])
      prediction_features = prediction_features.astype({
        'Disaster Subgroup': 'object',
        'Disaster Type': 'object',
        'Disaster Subtype': 'object',
        'ISO': 'object',
        'Subregion': 'object',
        'Start Year': 'int64',
        'Total Deaths': 'int64',
        'Total Affected': 'int64',
        'magnitude_degree_celcius': 'float64',
        'magnitude_km_square': 'float64',
        'magnitude_richter': 'float64',
        'magnitude_kph': 'float64'
      })
      prediction_features_transformed = preprocessor.transform(prediction_features)
      prediction_features_transformed = np.array(prediction_features_transformed)
      y_pred = loaded_model.predict(prediction_features_transformed)
      print(f"Predicted CPI: {y_pred}")
      return render_template("prediction.html",prediction=y_pred[0][0])

if(__name__ =="__main__"):
    app.run(debug=True)