import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgbCarouselModule } from '@ng-bootstrap/ng-bootstrap';


import {
  AvatarModule,
  BadgeModule, BreadcrumbComponent, BreadcrumbItemComponent, ButtonGroupModule,
  ButtonModule,
  CardModule,
  FormModule,
  GridModule,
  NavModule,
  ProgressModule, TableModule,
  TabsModule, WidgetStatBComponent, WidgetStatCComponent, WidgetStatFComponent
} from '@coreui/angular';
import { ChartjsModule } from '@coreui/angular-chartjs';

import { UserChartsComponent } from './user-charts.component';
import { UserChartsRoutingModule } from './user-charts-routing.module';
import {IconModule} from "@coreui/icons-angular";
import {ReactiveFormsModule} from "@angular/forms";
import {WidgetsModule} from "../widgets/widgets.module";

@NgModule({
  declarations: [UserChartsComponent],
  imports: [
    UserChartsRoutingModule,
    CardModule,
    NavModule,
    IconModule,
    TabsModule,
    CommonModule,
    GridModule,
    ProgressModule,
    ReactiveFormsModule,
    ButtonModule,
    FormModule,
    ButtonModule,
    ButtonGroupModule,
    ChartjsModule,
    AvatarModule,
    TableModule,
    WidgetsModule,
    BreadcrumbItemComponent,
    BreadcrumbComponent,
    WidgetStatCComponent,
    WidgetStatFComponent,
    WidgetStatBComponent,
    NgbModule,
    NgbCarouselModule
    
  ]
})
export class UserChartsModule {
}
