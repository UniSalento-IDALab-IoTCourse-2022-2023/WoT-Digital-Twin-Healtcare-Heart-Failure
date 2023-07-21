import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

interface IPatient {
  name: string;
  id: number;
  age: number;
  PBS: number;
  sex: number;
  heart_history: number[];
  spo2_history: number[];
  cp: number;
  max720 : number;
  max300 : number;
  max60 : number;
  // Altre proprietà dei pazienti...
}

@Injectable({
  providedIn: 'root'
})
export class PatientService {
  private apiUrl = 'http://127.0.0.1:5000/Patients/';

  constructor(private http: HttpClient) {}

  getPatientById(id: number): Observable<IPatient> {
    return this.http.get<IPatient>(`${this.apiUrl}${id}`);
  }
  downloadPatientDataset(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}${id}/download`, { responseType: 'blob' as 'json' });
  }
  downloadPatientECG(id: number): Observable<Blob> {
    // Imposta il tipo di contenuto nella richiesta HTTP come "text/csv"
    return this.http.get(`${this.apiUrl}${id}/downloadECG`, { responseType: 'blob', headers: { 'Content-Type': 'text/csv' } });
  }
  downloadDataset(): Observable<any> {
    // Invia una richiesta GET al server Flask per scaricare il dataset per tutti i pazienti
    return this.http.get(`${this.apiUrl}downloadDataset`);
  }
}
