import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import { DataDataService } from 'src/app/services/data-data.service';
import { Chart, ChartDataset, ChartOptions } from 'chart.js';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.css']
})
export class LineChartComponent implements OnInit {
  @ViewChild(BaseChartDirective)
  chart!: BaseChartDirective;
  private sub!: Subscription;

  public chartData: ChartDataset[] = [
    { data: [], label: 'data1', backgroundColor: '#8B5E83', borderRadius: 20 }
  ]

  public options: ChartOptions = {};

  public lables: string[] = ["odp1"];

  constructor(private _dataDataService: DataDataService) { }

  ngOnInit() {
    this.sub = this._dataDataService.Get().subscribe((data: any) => {
    });
  }
  ngOnDestroy() {
  }
}
