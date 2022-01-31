import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { DataDataService } from './services/data-data.service';
import { BaseChartDirective } from 'ng2-charts';

import * as $ from 'jquery';

import { appRoutes } from '../routes';

import { NgModule } from '@angular/core';
import { NgChartsModule } from 'ng2-charts';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { SectionSessionComponent } from './sections/section-session/section-session.component';
import { SectionDataComponent } from './sections/section-data/section-data.component';
import { SectionTracingComponent } from './sections/section-tracing/section-tracing.component';
import { LineChartComponent } from './charts/line-chart/line-chart.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SidebarComponent,
    SectionSessionComponent,
    SectionDataComponent,
    SectionTracingComponent,
    LineChartComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    NgChartsModule
  ],
  providers: [DataDataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
