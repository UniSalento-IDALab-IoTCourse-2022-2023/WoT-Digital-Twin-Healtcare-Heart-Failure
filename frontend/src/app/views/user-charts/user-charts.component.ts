import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import UsersData from "./user-charts.json";
import { UntypedFormControl, UntypedFormGroup } from "@angular/forms";
import { PatientService } from 'src/app/servizi/patient.service';
import { IChartProps, UserChartsData } from "src/app/views/user-charts/user-charts-data.component";
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { saveAs } from 'file-saver'; // Importa la funzione saveAs da 'file-saver'



interface IUserData {
  name: string;
  userId: number;
  age: number;
  PBS: number;
  sex: number;
  heart_history: number[];
  spo2_history: number[];
  cp : number;
  max720 : number;
  max300 : number;
  max60 : number;

}

@Component({
  selector: 'app-user-charts',
  templateUrl: './user-charts.component.html',
  styleUrls: ['./user-charts.component.scss']
})
export class UserChartsComponent implements OnInit {
  userId: number = 0;
  usersData = UsersData;
  userData: IUserData = this.usersData[this.userId];
  trafficRadio1Value: string = '5 hours';
  trafficRadio2Value: string = '5 hours';
  public chart1: IChartProps = {};
  public chart2: IChartProps = {};
  public trafficRadioGroup = new UntypedFormGroup({
    trafficRadio1: new UntypedFormControl(this.trafficRadio1Value),
    trafficRadio2: new UntypedFormControl(this.trafficRadio2Value)
  });

  public maxHeartRate: number;
  public maxHeartRateLocal: number;

  constructor(private route: ActivatedRoute, private patientService: PatientService, private userChartData: UserChartsData) {
    this.maxHeartRate = 0
    this.maxHeartRateLocal=0
  }

  ngOnInit() {
    this.route.paramMap.subscribe((params) => {
      this.userId = Number(params.get('id'));
      this.fetchPatientData();
      this.initCharts();
    });

    this.userData = this.usersData.find((u: IUserData) => {
      return u.userId === this.userId;
    });
    
  }

  fetchPatientData(): void {
    this.patientService.getPatientById(this.userId).subscribe((patient) => {
      const last720HeartHistory = patient.heart_history.slice(-720);
      this.userData = {
        userId: patient.id,
        age: patient.age,
        name: patient.name,
        PBS: patient.PBS,
        sex: patient.sex,
        heart_history: patient.heart_history.slice(-720),
        spo2_history : patient.spo2_history,
        cp : patient.cp,
        max720 : patient.max720,
        max300 : patient.max300,
        max60 : patient.max60,

      };
      this.userChartData.setChart1Data(patient.heart_history.slice(-720));
      this.userChartData.initChart1(this.trafficRadio1Value);
      this.userChartData.setChart2Data(patient.spo2_history.slice(-720));
      this.userChartData.initChart2(this.trafficRadio2Value);

      this.maxHeartRate = Math.max(...patient.heart_history);
      this.maxHeartRateLocal = Math.max(...patient.heart_history.slice(-300));
      
    });
  }

  initCharts(): void {
    this.chart1 = this.userChartData.chart1;
    this.chart2 = this.userChartData.chart2;
  }
  downloadDataset(): void {
    this.patientService.downloadPatientDataset(this.userId).subscribe(
      (response: any) => {
        // Scarica il file utilizzando la libreria "file-saver"
        saveAs(response, 'patient_dataset.csv');
      },
      (error) => {
        console.error('Errore durante il download del dataset', error);
  
      }
    );
  }
  downloadECG(): void {
    this.patientService.downloadPatientECG(this.userId).subscribe(
      (response: Blob) => {
        // Converti la risposta in un oggetto Blob e scarica il file utilizzando la libreria "file-saver"
        saveAs(response, `ecg_patient_${this.userId}.csv`);
      },
      (error) => {
        console.error('Errore durante il download dell\'ECG', error);

      }
    );
  }

  setTrafficPeriod(chartNumber: number, value: string): void {
    if (chartNumber === 1) {
      this.trafficRadio1Value = value;
      this.trafficRadioGroup.setValue({ trafficRadio1: value, trafficRadio2: this.trafficRadio2Value });
      this.userChartData.initChart1(this.trafficRadio1Value);
      if (this.trafficRadio1Value === '1 hour') {
        this.maxHeartRateLocal= this.userData.max60;
      }
      if (this.trafficRadio1Value === '5 hours') {
        this.maxHeartRateLocal = this.userData.max300;
      }
      if (this.trafficRadio1Value === '12 hours') {
        this.maxHeartRateLocal = this.userData.max720;
      } 

    } else {
      this.trafficRadio2Value = value;
      this.trafficRadioGroup.setValue({ trafficRadio1: this.trafficRadio1Value, trafficRadio2: value });
      this.userChartData.initChart2(this.trafficRadio2Value);
    }
  }
}


