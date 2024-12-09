import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Company } from '../models/company.model';
import { environment } from '../../environments/environment';
import { BaseResponse } from '../models/baseresponse.model';

@Injectable({
  providedIn: 'root'
})
export class ConfirmService {
  private apiUrl = environment.backendUrl + '/confirm';

  constructor(private http: HttpClient) { }

  send(code: {code: string}) {
    return this.http.post<BaseResponse<any>>(`${this.apiUrl}`, code);
  }

}