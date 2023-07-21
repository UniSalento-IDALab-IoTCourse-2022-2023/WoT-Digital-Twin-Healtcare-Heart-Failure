import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { UserChartsComponent } from './user-charts.component';

const routes: Routes = [
  {
    path: '',
    component: UserChartsComponent,
    data: {
      title: 'User Charts',
    },
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class UserChartsRoutingModule {}

