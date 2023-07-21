import { Injectable } from '@angular/core';
import { getStyle, hexToRgba } from '@coreui/utils';

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
export class DashboardChartsData {
  constructor() {
    this.initMainChart();
  }

  public mainChart: IChartProps = {};

  public random(min: number, max: number) {
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  initMainChart(period: string = 'Month') {
    const brandSuccess = getStyle('--cui-success') ?? '#4dbd74';
    const brandInfo = getStyle('--cui-info') ?? '#20a8d8';
    const brandInfoBg = hexToRgba(brandInfo, 10);
    const brandDanger = getStyle('--cui-danger') || '#f86c6b';

    // mainChart
    // mainChart
    this.mainChart['elements'] = period === 'Month' ? 12 : 27;
    this.mainChart['Data1'] = [104.2,
      103.4,
      103.2,
      69.5,
      97.5,
      101.6,
      78.1,
      48.0,
      103.0,
      103.1,
      103.4,
      101.3,
      105.0,
      102.3,
      90.9,
      95.4,
      63.2,
      80.6,
      101.8,
      84.6,
      97.6,
      102.7,
      101.1,
      90.0,
      102.2,
      92.4,
      103.8,
      104.6,
      105.0,
      93.7,
      88.2,
      92.4,
      101.3,
      100.6,
      66.8,
      74.3,
      87.7,
      77.4,
      86.1,
      93.0,
      59.5,
      100.1,
      57.6,
      89.8,
      91.2,
      100.6,
      40.8,
      63.8,
      68.1,
      104.3,
      102.4,
      103.9,
      74.4,
      89.6,
      91.2,
      100.8,
      100.0,
      91.4,
      91.4,
      68.0,
    ];
    // this.mainChart['Data2'] = [];
    this.mainChart['Data3'] = [];

    // generate random values for mainChart
    for (let i = 0; i <= this.mainChart['elements']; i++) {
      // this.mainChart['Data1'].push(57.0, 88.1, 95.8);
      // this.mainChart['Data2'].push(this.random(20, 160));
      this.mainChart['Data3'].push(80);
    }

    let labels: string[] = [];
    if (period === 'Month') {
      labels = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
      ];
    } else {
      /* tslint:disable:max-line-length */
      const week = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
      ];
      labels = week.concat(week, week, week, week, week, week);
    }

    const colors = [
      {
        // brandInfo
        backgroundColor: brandInfoBg,
        borderColor: brandInfo,
        pointHoverBackgroundColor: brandInfo,
        borderWidth: 2,
        fill: true
      },
      {
        // brandSuccess
        backgroundColor: 'transparent',
        borderColor: brandSuccess || '#4dbd74',
        pointHoverBackgroundColor: '#fff'
      },
      {
        // brandDanger
        backgroundColor: 'transparent',
        borderColor: brandDanger || '#f86c6b',
        pointHoverBackgroundColor: brandDanger,
        borderWidth: 1,
        borderDash: [8, 5]
      }
    ];

    const datasets = [
      {
        data: this.mainChart['Data1'],
        label: 'Current',
        ...colors[0]
      },
      {
        data: this.mainChart['Data2'],
        label: 'Previous',
        ...colors[1]
      },
      {
        data: this.mainChart['Data3'],
        label: 'BEP',
        ...colors[2]
      }
    ];

    const plugins = {
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

    const options = {
      maintainAspectRatio: false,
      plugins,
      scales: {
        x: {
          grid: {
            drawOnChartArea: false
          }
        },
        y: {
          beginAtZero: true,
          max: 200,
          ticks: {
            maxTicksLimit: 5,
            stepSize: Math.ceil(200 / 5)
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

    this.mainChart.type = 'line';
    this.mainChart.options = options;
    this.mainChart.data = {
      datasets,
      labels
    };
  }
  getRiskScorePercentage(riskScore: string): number {
    const percentage = parseFloat(riskScore.replace('%', ''));
    return Math.min(percentage, 100);
  }
  

}
