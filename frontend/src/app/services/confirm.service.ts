import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseResponse } from '../models/baseresponse.model';

@Injectable({
  providedIn: 'root'
})
export class ConfirmService {
  private apiUrl = 'confirm';

  constructor(private http: HttpClient) { }

  send(code: {code: string}) {
    return this.http.post<BaseResponse<any>>(`${this.apiUrl}`, code);
  }

}