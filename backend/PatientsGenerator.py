import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib

# Carica il modello addestrato
model = joblib.load('modello_logistic_regression.pkl')


data = pd.read_csv('Oxygen Dataset Final.csv')
print(data)

data = data[data['c/nc'] == 0]
data_oxy=data.loc[:,['spo2']]
data_oxy=data_oxy.dropna()
print(data_oxy)
#plt.hist(data_oxy,10)
#plt.show()

# pdf construction
counter_v = np.zeros(20)
for i in data_oxy['spo2']:
  if i<30:
    counter_v[5]+=1
  elif i<35:
    counter_v[6]+=1
  elif i<40:
    counter_v[7]+=1
  elif i<45:
    counter_v[8]+=1
  elif i<50:
    counter_v[9]+=1
  elif i<55:
    counter_v[10]+=1
  elif i<60:
    counter_v[11]+=1
  elif i<65:
    counter_v[12]+=1
  elif i<70:
    counter_v[13]+=1
  elif i<75:
    counter_v[14]+=1
  elif i<80:
    counter_v[15]+=1
  elif i<85:
    counter_v[16]+=1
  elif i<90:
    counter_v[17]+=1
  elif i<95:
    counter_v[18]+=1
  else:
    counter_v[19]+=1

prob_oxy = counter_v/len(data_oxy['spo2'])
print(prob_oxy)

# iter_value = how much value do you want?
# return: list of "iter_value" values
def generateSpo2Value(iter_value):
  spo2_list = []

  for i in range(0,iter_value):
    randomVal = np.random.choice(20, p=prob_oxy)
    spo2_list.append(round(np.random.uniform(randomVal*5,(randomVal+1)*5),1))
  return spo2_list


#print(generateSpo2Value(1440)) # 1440 minutes = 1 day

data_hr=data.loc[:,['pr']]
data_hr=data_hr.dropna()
data_hr

#plt.hist(data_hr)
#plt.show()

# pdf construction
counter_hr = np.zeros(21)
for i in data_hr['pr']:
  if i<30:
    counter_hr[5]+=1
  elif i<35:
    counter_hr[6]+=1
  elif i<40:
    counter_hr[7]+=1
  elif i<45:
    counter_hr[8]+=1
  elif i<50:
    counter_hr[9]+=1
  elif i<55:
    counter_hr[10]+=1
  elif i<60:
    counter_hr[11]+=1
  elif i<65:
    counter_hr[12]+=1
  elif i<70:
    counter_hr[13]+=1
  elif i<75:
    counter_hr[14]+=1
  elif i<80:
    counter_hr[15]+=1
  elif i<85:
    counter_hr[16]+=1
  elif i<90:
    counter_hr[17]+=1
  elif i<95:
    counter_hr[18]+=1
  elif i<100:
    counter_hr[19]+=1
  else:
    counter_hr[20]+=1


prob_hr = counter_hr/len(data_hr['pr'])


def generateHartRateValue(iter_value):
  hartrate_list = []

  for i in range(0,iter_value):
    randomVal = np.random.choice(21, p=prob_hr)
    hartrate_list.append(round(np.random.uniform(randomVal*5,(randomVal+1)*5),1))
  return hartrate_list


#print(generateHartRateValue(1440)) # 1440 minutes = 1 day


import neurokit2 as nk
import numpy as np
import pandas as pd

import names

#pretty json print
import json
data = pd.read_csv('heart.csv')


def generate_people_noECG(target_desire):  #target_desire ->  0 = no disease, 1 = disease
  found = False

  people = {}
  while not found:
    rand_extration = int(np.random.uniform(0, len(data['target'])))
    if data['target'][rand_extration]== target_desire:
      #print(data.loc[rand_extration,['age','sex','cp','trestbps']])
      age = int(data.loc[rand_extration,['age']][0])
      sex = int(data.loc[rand_extration,['sex']][0])
      cp = int(data.loc[rand_extration,['cp']][0]) #chest pain
      trestbps = int(data.loc[rand_extration,['trestbps']][0]) #maximum heart rate achieved
      chol = int(data.loc[rand_extration, ['chol']][0])  # chest pain
      fbs = int(data.loc[rand_extration, ['fbs']][0])  # chest pain
      restecg = int(data.loc[rand_extration, ['restecg']][0])  # chest pain
      thalach = int(data.loc[rand_extration, ['thalach']][0])  # chest pain
      exang = int(data.loc[rand_extration, ['exang']][0])  # chest pain
      oldpeak = data.loc[rand_extration, 'oldpeak']
      if isinstance(oldpeak, float):
        oldpeak = float(oldpeak)
      elif isinstance(oldpeak, int):
        oldpeak = int(oldpeak)

      slope = int(data.loc[rand_extration, ['slope']][0])  # chest pain
      ca = int(data.loc[rand_extration, ['ca']][0])  # chest pain
      thal = int(data.loc[rand_extration, ['thal']][0])  # chest pain
      heart_history = generateHartRateValue(1440)  # daily

      spo2_history = generateSpo2Value(1440)  # daily


      if sex == 0:
        sexA = 'male'
      else:
        sexA = 'female'

      name = names.get_full_name(gender=sexA)


      people.update({"name":name, "age": age, "sex":sex,"cp":cp,"trestbps":trestbps,"chol":chol,"fbs":fbs,"restecg":restecg,"thalach":thalach,"exang":exang,"oldpeak":oldpeak,"slope":slope,"ca":ca,"thal":thal,"heart_history":heart_history, "spo2_history":spo2_history})

      found = True
      return people




patients = []
target_0_count = 0
target_1_count = 0

patient_0=generate_people_noECG(0)
patient_1=generate_people_noECG(0)
patient_2=generate_people_noECG(0)
patient_3=generate_people_noECG(1)
patient_4=generate_people_noECG(1)
patient_5=generate_people_noECG(1)


patients.append(patient_0)
patients.append(patient_1)
patients.append(patient_2)
patients.append(patient_3)
patients.append(patient_4)
patients.append(patient_5)


for patient in patients:
    input_data = [
        int(patient['sex']),int(patient['age']),  int(patient['cp']),int(patient['thalach'])]

    # Converti i dati di input in un array numpy e riformatta per la previsione
    input_data_as_numpy_array = np.asarray(input_data, dtype=np.float64)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = model.predict(input_data_reshaped)

    if prediction[0] == 0:
      patient['target'] = 0
      print("Il paziente", patient['name'], "non ha una malattia cardiaca.")
    else:
      patient['target'] = 1
      print("Il paziente", patient['name'], "ha una malattia cardiaca.")

    prediction_proba = model.predict_proba(input_data_reshaped)
    prob_target_0 = prediction_proba[0][0]
    prob_target_1 = prediction_proba[0][1]

    patient['PBS'] = round(prob_target_1 * 100, 2)

    if patient['target'] == 0:
      print("Probabilità di avere una malattia cardiaca:", prob_target_1)
    else:
      print("Probabilità di avere una malattia cardiaca:", prob_target_1)



for patient in patients:
  print(patient)
print("\n")
# Ordina i pazienti in base alla probabilità scompenso cardiaco (probabilità associata alla classe 1)
# Ordina i pazienti in base alla probabilità scompenso cardiaco (prob_target_1) in ordine decrescente
patients_sorted = sorted(patients, key=lambda x: x['PBS'], reverse=True)

# Stampa i 5 pazienti con il valore più alto di probabilità scompenso cardiaco
for patient in patients_sorted:
  print(patient)

import pymongo

# Connetti al database MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["HeartFailure"]  # Sostituisci con il nome del tuo database

# Seleziona la collezione
collection = database["Patients"]  # Sostituisci con il nome della tua collezione

# Inserisci i pazienti nella collezione
for i, patient in enumerate(patients_sorted):
    patient["id"] = i + 1
    collection.insert_one(patient)

# Stampa un messaggio di conferma
print("Inserimento completato.")




#aumentare valori hear_rate primi 3 pazienti

# Connetti al database MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["HeartFailure"]  # Sostituisci con il nome del tuo database
collection = database["Patients"]  # Sostituisci con il nome della tua collezione

# Trova i primi 3 pazienti nel database
patients_to_update = collection.find().limit(3)

# Aggiorna i valori dell'array heart_history per i pazienti trovati
for patient in patients_to_update:
    patient_id = patient["_id"]  # ID del paziente nel database
    heart_history = patient["heart_history"]  # Array heart_history da aggiornare

    # Aumenta tutti i valori dell'array heart_history di 35
    updated_heart_history = [value + 35 for value in heart_history]

    # Aggiorna il paziente nel database con i nuovi valori dell'array heart_history
    collection.update_one({"_id": patient_id}, {"$set": {"heart_history": updated_heart_history}})

# Stampa un messaggio di conferma
print("Aggiornamento completato.")