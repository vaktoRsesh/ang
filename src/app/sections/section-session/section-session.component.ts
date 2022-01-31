import { DataDataService } from 'src/app/services/data-data.service';
import { Component, OnDestroy, OnInit, Injectable } from '@angular/core';

@Component({
  selector: 'app-section-session',
  templateUrl: './section-session.component.html',
  styleUrls: ['./section-session.component.css']
})
export class SectionSessionComponent implements OnInit {
  public sessions;
  constructor(private _dataDataService: DataDataService) { }
  sub = this._dataDataService.GetSession().subscribe((res: any) => {
    this.sessions = res;
    console.warn(this.sessions);
    for (var i = 0; i < res.length; i++) {
      console.log(res[i]);
    }
  })
  ngOnInit(): void {
  }
  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
