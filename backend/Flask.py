from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import json
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import requests
from pymongo import UpdateOne
import neurokit2 as nk
import csv
import os

app = Flask(__name__)
CORS(app)
# Configurazione del client MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['HeartFailure']
collection = db['Patients']
ecg_collection = db['ECG']


@app.route('/Patients', methods=['GET'])
def get_patients():
    patients = list(collection.find().limit(6))
    patients_json = []
    for patient in patients:
        patient['_id'] = str(patient['_id'])            # Converti l'ObjectID in una stringa
        patients_json.append(patient)
    return jsonify(patients_json), 200


@app.route('/Patients/<string:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = collection.find_one({'id': int(patient_id)})
    if patient:
        heart_history = patient.get('heart_history', [])  # Ottieni l'array heart_history dal documento del paziente o una lista vuota se non esiste

        # Calcola i massimi dei valori negli ultimi 720, 300 e 60 elementi dell'array heart_history
        max720 = max(heart_history[-720:]) if heart_history else None
        max300 = max(heart_history[-300:]) if heart_history else None
        max60 = max(heart_history[-60:]) if heart_history else None

        # Aggiungi gli attributi al dizionario del paziente
        patient['max720'] = max720
        patient['max300'] = max300
        patient['max60'] = max60

        # Converti l'ObjectID in una stringa
        patient['id'] = str(patient['id'])

        # Ritorna il JSON del paziente con i nuovi attributi, utilizzando indent=4 per il JSON formattato
        return json.dumps(patient, default=str, indent=4), 200
    else:
        return jsonify({'error': 'Patient not found'}), 404




# Funzione per generare il grafico ECG e convertirlo in immagine base64


def generate_ecg_image(ecg_signal):
    plt.figure(figsize=(12, 4))
    plt.plot(ecg_signal)
    plt.title('ECG Signal')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Converti l'immagine in base64
    waves_image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return waves_image_base64
# Funzione per generare il secondo grafico
def generate_rpeaks_image(rpeaks, ecg_signal):

    plt.figure(figsize=(20, 4))
    nk.events_plot(rpeaks['ECG_R_Peaks'][:5], ecg_signal[:6000])
    plt.title('R-Peaks Detection')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Converti l'immagine in base64
    rpeaks_image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return rpeaks_image_base64
def generate_waves_image(waves_peak, ecg_signal):
    plt.figure(figsize=(20, 4))
    nk.events_plot([waves_peak['ECG_T_Peaks'][:3],
                    waves_peak['ECG_P_Peaks'][:3],
                    waves_peak['ECG_Q_Peaks'][:3],
                    waves_peak['ECG_S_Peaks'][:3]], ecg_signal[:4000])
    plt.title('ECG Waves Delineation')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Converti l'immagine in base64
    waves_image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return waves_image_base64

@app.route('/ECG/<string:patient_id>', methods=['GET'])
def get_ECG(patient_id):
    ecg_data = ecg_collection.find_one({'id': int(patient_id)})
    if ecg_data:
        ecg_data['id'] = int(ecg_data['id'])  # Converti l'ObjectID in una stringa
        # Recupera i segnali ECG dal documento
        ecg_signal = ecg_data.get('ecg_signal')
        # Prendi solo gli ultimi 30000 valori del segnale ECG
        last_30000_ecg_signal = ecg_signal[-30000:]
        # Genera il primo grafico ECG con gli ultimi 30000 valori
        ecg_image_base64 = generate_ecg_image(last_30000_ecg_signal)
        # Genera il secondo grafico con i rilevamenti dei R-Peaks
        _, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=1000)
        rpeaks_image_base64 = generate_rpeaks_image(rpeaks, ecg_signal)
        # Delinea le onde dell'ECG
        _, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=1000, method="peak")
        # Genera il terzo grafico con la delineazione delle onde dell'ECG
        waves_image_base64 = generate_waves_image(waves_peak, ecg_signal)
        # Aggiungi le immagini ECG al documento
        ecg_data['ECG_Image'] = ecg_image_base64
        ecg_data['RPeaks_Image'] = rpeaks_image_base64
        ecg_data['Waves_Image'] = waves_image_base64
        # Aggiorna il documento nella collezione "ECG" con le immagini generate
        ecg_collection.update_one({'id': int(patient_id)}, {"$set": ecg_data})
        # Restituisci il documento JSON e lo status code 200
        return json.dumps(ecg_data, default=str, indent=4), 200
    # Restituisci un messaggio di errore se il paziente non è stato trovato
    return "Patient not found.", 404



@app.route('/ECG/<string:patient_id>/ECG_Image', methods=['POST'])



@app.route('/ECG_IMG/<string:patient_id>', methods=['GET'])
def get_ECG_IMG(patient_id):
    ecg_data = ecg_collection.find_one({'id': int(patient_id)})
    if ecg_data:
        ecg_data['id'] = int(ecg_data['id'])

        if 'ECG_Image' in ecg_data:
            image_base64 = ecg_data['ECG_Image']
            buffer = io.BytesIO(base64.b64decode(image_base64))
            temp_image_path = 'temp_ecg_image.jpg'
            with open(temp_image_path, 'wb') as file:
                file.write(buffer.getvalue())
            return send_file(temp_image_path, mimetype='image/jpeg', as_attachment=True)
        return json.dumps(ecg_data, default=str, indent=4), 200
    else:
        return jsonify({'error': 'ECG data not found'}), 404

@app.route('/ECG_RPeaks_Image/<string:patient_id>', methods=['GET'])
def get_ECG_RPeaks_Image(patient_id):
    ecg_data = ecg_collection.find_one({'id': int(patient_id)})
    if ecg_data:
        ecg_data['id'] = int(ecg_data['id'])  # Converti l'ObjectID in una stringa

        if 'RPeaks_Image' in ecg_data:
            image_base64 = ecg_data['RPeaks_Image']
            buffer = io.BytesIO(base64.b64decode(image_base64))
            temp_image_path = 'temp_ecg_image1.jpg'
            with open(temp_image_path, 'wb') as file:
                file.write(buffer.getvalue())

            return send_file(temp_image_path, mimetype='image/jpeg', as_attachment=True)

        return json.dumps(ecg_data, default=str, indent=4), 200
    else:
        return jsonify({'error': 'ECG data not found'}), 404

@app.route('/ECG_Waves_Image/<string:patient_id>', methods=['GET'])
def get_ECG_Waves_Image(patient_id):
    ecg_data = ecg_collection.find_one({'id': int(patient_id)})
    if ecg_data:
        ecg_data['id'] = int(ecg_data['id'])
        if 'Waves_Image' in ecg_data:
            image_base64 = ecg_data['Waves_Image']
            buffer = io.BytesIO(base64.b64decode(image_base64))
            temp_image_path = 'temp_ecg_image2.jpg'
            with open(temp_image_path, 'wb') as file:
                file.write(buffer.getvalue())
            return send_file(temp_image_path, mimetype='image/jpeg', as_attachment=True)
        return json.dumps(ecg_data, default=str, indent=4), 200
    else:
        return jsonify({'error': 'ECG data not found'}), 404

@app.route('/update_patient_data', methods=['POST'])
def update_patient_data():
    patient_data = request.json

    patient_id = patient_data['id']
    pbs = patient_data.get('PBS')
    target = patient_data.get('target')

    result = collection.update_one(
        {'_id': ObjectId(patient_id)},
        {'$set': {'PBS': pbs, 'target': target}}
    )

    if result.modified_count > 0:
        return jsonify({'message': f'Patient {patient_id} data updated successfully.'}), 200
    else:
        return jsonify({'error': f'Failed to update data for patient {patient_id}.'}), 500
@app.route('/Patients/<string:patient_id>/download', methods=['GET'])
def download_patient_dataset(patient_id):
    patient = collection.find_one({'id': int(patient_id)})
    if patient:
        # Genera il nome del file CSV utilizzando l'ID del paziente
        file_name = f'patient_dataset_{patient_id}.csv'

        # Apri un file CSV in modalità scrittura
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = ['id','name', 'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak',
                          'slope', 'ca', 'thal',  'target', 'PBS', ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Scrivi l'intestazione nel file CSV
            writer.writeheader()

            # Scrivi i dati del paziente nel file CSV
            writer.writerow({
                'id': patient['id'],
                'name': patient['name'],
                'age': patient['age'],
                'sex': patient['sex'],
                'cp': patient['cp'],
                'trestbps': patient['trestbps'],
                'chol': patient['chol'],
                'fbs': patient['fbs'],
                'restecg': patient['restecg'],
                'thalach': patient['thalach'],
                'exang': patient['exang'],
                'oldpeak': patient['oldpeak'],
                'slope': patient['slope'],
                'ca': patient['ca'],
                'thal': patient['thal'],
                'target': patient['target'],
                'PBS': patient['PBS'],

            })

        # Dopo aver generato il dataset, utilizza send_file per restituire il file al client.
        response = send_file(file_name, as_attachment=True)
        response.headers["Content-Disposition"] = f"attachment; filename={os.path.basename(file_name)}"
        return response, 200
    else:
        return jsonify({'error': 'Patient not found'}), 404
@app.route('/Patients/<string:patient_id>/downloadECG', methods=['GET'])
def download_patient_ecg(patient_id):
    patient = ecg_collection.find_one({'id': int(patient_id)})
    if patient:
        # Genera il nome del file CSV utilizzando l'ID del paziente
        file_name = f'ecg_patient_{patient_id}.csv'

        # Apri il file CSV in modalità scrittura
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = ['id_Patient', 'name', 'ecg_signal']  # Definisci gli intesestazioni delle colonne
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Scrivi l'intestazione nel file CSV
            writer.writeheader()

            # Scrivi i dati del paziente nel file CSV
            writer.writerow({
                'id_Patient': patient['id'],
                'name': patient['name'],
                'ecg_signal': patient['ecg_signal'],
            })

        # Dopo aver generato il dataset, utilizza send_file per restituire il file al client.
        response = send_file(file_name, as_attachment=True)
        response.headers["Content-Disposition"] = f"attachment; filename={os.path.basename(file_name)}"
        return response, 200
    else:
        return jsonify({'error': 'Patient not found'}), 404
@app.route('/Patients/downloadDataset', methods=['GET'])
def download_dataset():
    patients = collection.find({})
    dataset = []

    for patient in patients:
        ecg_data = {
            'id': patient['id'],
            'name': patient['name'],
            'age': patient['age'],
            'sex': patient['sex'],
            'cp': patient['cp'],
            'trestbps': patient['trestbps'],
            'chol': patient['chol'],
            'fbs': patient['fbs'],
            'restecg': patient['restecg'],
            'thalach': patient['thalach'],
            'exang': patient['exang'],
            'oldpeak': patient['oldpeak'],
            'slope': patient['slope'],
            'ca': patient['ca'],
            'thal': patient['thal'],
            'target': patient['target']
        }
        dataset.append(ecg_data)

    # Genera il nome del file CSV
    file_name = 'dataset.csv'

    # Scrivi i dati del dataset in un file CSV
    with open(file_name, mode='w', newline='') as csv_file:
        fieldnames = ['id','name','age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak',
                      'slope', 'ca', 'thal', 'target']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Scrivi l'intestazione nel file CSV
        writer.writeheader()

        # Scrivi i dati dei pazienti nel file CSV
        for patient in dataset:
            writer.writerow(patient)

    # Dopo aver generato il dataset, utilizza send_file per restituire il file al client.
    response = send_file(file_name, as_attachment=True)
    response.headers["Content-Disposition"] = f"attachment; filename={os.path.basename(file_name)}"
    return response, 200



if __name__ == '__main__':
    app.run(debug=True)



