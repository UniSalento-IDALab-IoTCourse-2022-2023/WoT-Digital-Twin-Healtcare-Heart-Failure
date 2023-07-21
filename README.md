# Preview
On each page of the site, it is possible to download the csv of the dataset by simply clicking on the respective button.
## Patients list
The frontend provides a main dashboard, where the doctor can get an overview of the patients' status.
![dashboard](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WoT-Digital-Twin-Healtcare-Heart-Failure-Frontend/assets/60972885/4582c670-93b1-4a3a-9e60-5b07aea7ee16)

The doctor can switch the display mode to the patient-specific dashboard using the button in the last column.
## Patient Digital Twin
Through the use of graphs and visual tools, the patient's status can be monitored in this section.
![user1](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WoT-Digital-Twin-Healtcare-Heart-Failure/assets/60972885/2904a339-7fa6-411e-a345-56071496dd82)
![user2](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WoT-Digital-Twin-Healtcare-Heart-Failure/assets/60972885/59d3aa1d-ec40-440f-9419-8c4300694831)
The patient's heartbeat values, which were recorded every minute, are displayed on a graph. The default display is set to 5 hours, meaning that the patient's values recorded during this time are displayed. However, a function was implemented that allows the doctor to change how the values are displayed in the graph. The doctor has the option to adjust this time limit at any time to 1 hour or 12 hours.
On the other hand, the second graph shows the spO2 measurements taken for each patient. The same logic that was used to create the previous graph was also used to create this one. 


The patient's ECG is be viewed on a carousel. As you scroll through the images, the same graph is visible, but with important features like the R, P, Q, S, and T peaks highlighted.
![ecg1](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WoT-Digital-Twin-Healtcare-Heart-Failure/assets/60972885/22943f8b-7542-48d2-be27-713502dad01d)
![ecg2](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WoT-Digital-Twin-Healtcare-Heart-Failure/assets/60972885/69067771-1914-4274-8a25-73f1c081b500)
![ecg3](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WoT-Digital-Twin-Healtcare-Heart-Failure/assets/60972885/cbf182d6-db3e-4040-84c5-521474021115)
