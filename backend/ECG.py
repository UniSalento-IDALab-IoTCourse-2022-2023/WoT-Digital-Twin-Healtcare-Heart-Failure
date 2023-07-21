import pymongo
import neurokit2 as nk

# Connessione al database MongoDB (assicurati di aver già avviato il server MongoDB)
client = pymongo.MongoClient("localhost", 27017)
db = client["HeartFailure"]  # Sostituisci "nome_del_tuo_database" con il nome del tuo database MongoDB
collection_patients = db["Patients"]  # Sostituisci "Patients" con il nome della tua collezione dei pazienti
collection_ecg = db["ECG"]  # Collezione per i dati ECG

# Ottieni i pazienti dalla collezione "Patients"
patients = collection_patients.find()

# Genera i documenti e inseriscili nella collezione "ECG" per ogni paziente
for patient_id, patient in enumerate(patients, start=1):
    ecg_signal = nk.data(dataset="ecg_1000hz")  # Genera l'array ecg_signal utilizzando NeuroKit2
    ecg_document = {"patient_id": patient["_id"], "ecg_signal": ecg_signal.tolist(), "id": patient_id, "name":patient["name"]}
    collection_ecg.insert_one(ecg_document)

# Chiudi la connessione al database
client.close()


