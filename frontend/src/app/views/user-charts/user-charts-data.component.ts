import { Injectable } from '@angular/core';
import { getStyle, hexToRgba } from '@coreui/utils';
import UsersData from "./user-charts.json"

export interface IChartProps {
  data?: any;
  labels?: any;
  options?: any;
  colors?: any;
  type?: any;
  legend?: any;

  [propName: string]: any;
}

@Injectable({
  providedIn: 'any'
})
export class UserChartsData {

  plugins = {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        labelColor: function(context: any) {
          return {
            backgroundColor: context.dataset.borderColor
          };
        }
      }
    }
  };

  options = {
    maintainAspectRatio: false,
    plugins: this.plugins,
    scales: {
      x: {
        grid: {
          drawOnChartArea: false
        }
      },
      y: {
        beginAtZero: true,
        max: 180,
        ticks: {
          maxTicksLimit: 5,
          stepSize: Math.ceil(180 / 20)
        }
      }
    },
    elements: {
      line: {
        tension: 0.4
      },
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
        hoverBorderWidth: 3
      }
    }
  };
  public data1 : number[]
  public data2 : number[]

  constructor() {
    this.initAllCharts();
    this.data1 = []
    this.data2 = []
  }
  setChart1Data(data1: number[]) {
    this.chart1['data'] = data1;
    this.data1 = data1
  }
  setChart2Data(data2: number[]) {
    this.chart2['data'] = data2;
    this.data2 = data2
  }
  

  public chart1: IChartProps = {};
  public chart2: IChartProps = {};

  initAllCharts(period1: string = '5 hours', period2: string = '5 hours') {
    this.initChart1(period1);
    this.initChart2(period2);
  }
  
  
  
  initChart1(period: string = '5 hours') {
    const brandInfo = '#20a8d8';
    const brandInfoBg = hexToRgba(brandInfo, 10);

  
    let labels: number[] = [];
    if (period === '5 hours') {
      if (this.data1) {
        this.chart1['data'] = this.data1.slice(-300);
        for (let i: number = 0; i < 303; i++) {
          labels.push(i);
        }
      }
    } else if (period === '1 hour') {
      if (this.data1) {
        this.chart1['data'] = this.data1.slice(-60);
        for (let i: number = 0; i < 60; i++) {
          labels.push(i);
        }
      }
    } else if (period === '12 hours') {
      if (this.data1) {
        this.chart1['data'] = this.data1.slice(-720);
        for (let i: number = 0; i < 725; i++) {
          labels.push(i);
        }
      }
    }
  
    const color = {
      // brandInfo
      backgroundColor: brandInfoBg,
      borderColor: brandInfo,
      pointHoverBackgroundColor: brandInfo,
      borderWidth: 2,
      fill: true
    };
  
    const datasets = [
      {
        data: this.chart1['data'],
        label: 'Current',
        ...color
      }
    ];
  
    this.chart1.type = 'line';
    this.chart1.options = this.options;
    this.chart1.data = {
      datasets,
      labels
    };
  };

  initChart2(period: string = '5 hours') {
    const brandInfo = '#16eebb';
    const brandInfoBg = hexToRgba(brandInfo, 10);

    
  

    let labels: number[] = [];
    if (period === '5 hours') {
      if(this.data2) {
      this.chart2['data'] = this.data2.slice(-300);
      for (let i = 0; i < 303; i++) {
        labels.push(i);
      }
    }
    } else if (period === '1 hour') {
      if (this.data2) {
      this.chart2['data'] = this.data2.slice(-60);
      for (let i = 0; i < 60; i++) {
        labels.push(i);
      }
    }
    } else if (period === '12 hours') {
      if(this.data2) {
      this.chart2['data'] = this.data2.slice(-720);
      for (let i = 0; i < 725; i++) {
        labels.push(i);
      }
    }
    }

    const color = {
      // brandInfo
      backgroundColor: brandInfoBg,
      borderColor: brandInfo,
      pointHoverBackgroundColor: brandInfo,
      borderWidth: 2,
      fill: true
    };

    const datasets = [
      {
        data: this.chart2['data'],
        label: 'Current',
        ...color
      }
    ];


    this.chart2.type = 'line';
    this.chart2.options = this.options;
    this.chart2.data = {
      datasets,
      labels
    };
  };

}
