import tensorflow
import pandas
import numpy
import sklearn
import joblib
from flask import Flask, render_template

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




if(__name__ =="__main__"):
    app.run(debug=True)