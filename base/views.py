from django.shortcuts import render
from .pickle_models import *
import os

# Create your views here.

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pickle_models_folder = os.path.join(base_dir, 'base/pickle_models')
model_path = os.path.join(pickle_models_folder, 'fraud_detect.sav')
scaler_path = os.path.join(pickle_models_folder, 'scaler.sav')


def getPredictions(hour, day, month, year, category_encoded, city_encoded, state_encoded, job_encoded, age, amt, city_pop, encoded_F, encoded_M):
    import pickle
    model = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
    prediction = model.predict(scaler.transform(
        [[hour, day, month, year, category_encoded, city_encoded, state_encoded, job_encoded, age, amt, city_pop, encoded_F, encoded_M]]))

    if prediction == 0:
        return "Fraudulent Transaction detected"
    elif prediction == 1:
        return "transaction Passed"
    else:
        return "error"


def index(request):
    return render(request, 'index.html', {})


def result(request):
    hour = int(request.GET['hour'])
    day = int(request.GET['day'])
    month = int(request.GET['month'])
    year = int(request.GET['year'])
    category_encoded = int(request.GET['category_encoded'])
    city_encoded = int(request.GET['city_encoded'])
    state_encoded = int(request.GET['state_encoded'])
    job_encoded = int(request.GET['job_encoded'])
    age = int(request.GET['age'])
    amt = int(request.GET['amt'])
    city_pop = int(request.GET['city_pop'])
    encoded_F = int(request.GET['encoded_F'])
    encoded_M = int(request.GET['encoded_M'])

    result = getPredictions(hour, day, month, year, category_encoded, city_encoded,
                            state_encoded, job_encoded, age, amt, city_pop, encoded_F, encoded_M)

    return render(request, 'result.html', {'result': result})
