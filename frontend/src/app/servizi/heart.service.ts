import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface IHeartData {
  name: string;
  id: number;
  age: number;
  ca: number;
  chol: number;
  cp: number;
  exang: number;
  fbs: number;
  oldpeak: number;
  target: number;
  restecg: number;
  PBS: string;
  sex: number;
  slope: number;
  thal: number;
  thalach: number;
  trestbps: number;
}

@Injectable({
  providedIn: 'root'
})
export class HeartService {
  private apiUrl = 'http://127.0.0.1:5000/Patients';

  constructor(private http: HttpClient) {}

  getHeartData(): Observable<IHeartData[]> {
    return this.http.get<IHeartData[]>(this.apiUrl);
  }
  downloadDataset(): Observable<any> {
    // Imposta il tipo di risposta come "text"
    return this.http.get(`${this.apiUrl}/downloadDataset`, { responseType: 'text' });
  }
}

