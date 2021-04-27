from flask import Flask, render_template, request, url_for
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('Random_Forest_Regression_Model.pkl', 'rb'))

@app.route('/',methods=['GET', 'POST'])
def index_page():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year_of_the_Car'])
        No_of_Years = 2021 - Year
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        No_of_Owners = int(request.form['No_of_Owners'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type_Petrol == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Manual = request.form['Transmission_Manual']
        if Transmission_Manual == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        prediction = model.predict([[Present_Price,Kms_Driven,No_of_Owners,No_of_Years,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output = round(prediction[0],2)
        if output<0:
            return render_template('index.html', prediction_text = "Sorry you cant sell this car")
        else:
            return render_template('index.html', prediction_text= "The selling price of the car is : {} lacs".format(output))
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)