import { Component, OnInit, ViewChild } from '@angular/core';
import { DataDataService } from 'src/app/services/data-data.service';
import { Subscription, timeout } from 'rxjs';

declare const L: any;

@Component({
  selector: 'app-section-tracing',
  templateUrl: './section-tracing.component.html',
  styleUrls: ['./section-tracing.component.css']
})

export class SectionTracingComponent implements OnInit {

  sub: Subscription;

  public numerSesji: any;

  public lat : any;

  public led :any;

  public map: any;

  public marker: any;

  constructor(private _dataDataService: DataDataService) { }

  ngOnInit(): void {
    this.map = L.map('map').setView([50.06, 22.49], 13);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoidmFrdG9yIiwiYSI6ImNreXVoaDg4NDA3YjUyb21wODJ6Nm81cWQifQ.Jv5pqzp0x44cD_QFo_TU6Q', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'your.mapbox.access.token'
    }).addTo(this.map);

  }

  setSesja(liczba) {
    this.numerSesji = liczba;
  }

  update() {
    this.sub = this._dataDataService.Get().subscribe((res: any) => {
      var arr1 = new Array;
      var arr2 = new Array;
      var varr1: any;
      var id: any = 0;
      for (var i = 0; i < res.length; i++) {
        if (res[i].sessionid == this.numerSesji) {
          arr1[id] = res[i].polozenie_n;
          arr2[id] = res[i].polozenie_e;
          id++;
        }
      }
      this.lat = arr1[arr1.length - 1];
      this.led = arr2[arr2.length - 1]
      if (this.marker) { this.marker.remove(); }
      this.marker = L.marker([this.lat, this.led]).addTo(this.map);

    })

  }

  ngOnDestroy() {
  }

}
