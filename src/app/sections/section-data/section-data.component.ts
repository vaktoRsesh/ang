import { Component, OnInit, ViewChild } from '@angular/core';
import { DataDataService } from 'src/app/services/data-data.service';
import { Chart } from 'chart.js';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-section-data',
  templateUrl: './section-data.component.html',
  styleUrls: ['./section-data.component.css']
})

export class SectionDataComponent implements OnInit {

  sub: Subscription;
  sub2: Subscription;
  sub3: Subscription;

  public numerSesji: any;

  public customSesja: any = 4;

  constructor(private _dataDataService: DataDataService) { }

  setSesja(liczba) {
    this.numerSesji = liczba;
  }

  public myChart1: Chart;

  public myChart2: Chart;

  update() {
    this.sub = this._dataDataService.Get().subscribe((res: any) => {
      var arr1 = new Array;
      var arr2 = new Array;
      var id: any = 0;
      var date: any;
      var time: string;
      if (this.myChart1) { this.myChart1.destroy(); }
      for (var i = 0; i < res.length; i++) {
        if (res[i].sessionid == this.numerSesji) {
          date = new Date(res[i].czas);
          time = date.getHours().toString() + ":" + date.getMinutes().toString() + ":" + date.getSeconds().toString();
          arr1[id] = res[i].wilgotnosc;
          arr2[id] = time;
          id++;
        }

      }

      this.myChart1 = new Chart('myChart', {
        type: 'line',
        data: {
          labels: arr2,
          datasets: [{
            label: 'Wilgotność otoczenia (%)',
            data: arr1,
            borderColor: '#77a0a9',
            backgroundColor: '#6f7d8c',
            fill: true,
          }]
        }
      });
    });

    this.sub2 = this._dataDataService.Get().subscribe((res: any) => {
      var arr3 = new Array;
      var arr4 = new Array;
      var id: any = 0;
      var date: any;
      var time: string;
      if (this.myChart2) { this.myChart2.destroy(); }
      for (var i = 0; i < res.length; i++) {
        if (res[i].sessionid == this.numerSesji) {
          date = new Date(res[i].czas);
          time = date.getHours().toString() + ":" + date.getMinutes().toString() + ":" + date.getSeconds().toString();
          arr3[id] = res[i].temperaturaot;
          arr4[id] = time;
          id++;
        }
      }

      this.myChart2 = new Chart("myChart2", {
        type: 'line',
        data: {
          labels: arr4,
          datasets: [{
            label: 'Temperatura otoczenia (°C)',
            data: arr3,
            borderColor: '#77a0a9',
            backgroundColor: '#6f7d8c',
            fill: true,
          }]
        }
      });
    });

  }
  ngOnInit() {
  }

  ngOnDestroy() {
  }
}


