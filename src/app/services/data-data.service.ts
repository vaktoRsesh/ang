import { Injectable } from "@angular/core";
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http'
import { map } from 'rxjs';

@Injectable()
export class DataDataService{

    readonly ROOT_URL_DATA = 'http://localhost:5000/api/Data';
    readonly ROOT_URL_SESSION = 'http://localhost:5000/api/Session';
    datas: any;

    constructor(public _http: HttpClient){}
    Get(){
       return this._http.get(this.ROOT_URL_DATA).pipe(map(res => res));
    }
    GetSession(){
        return this._http.get(this.ROOT_URL_SESSION).pipe(map(res => res));
     }
}