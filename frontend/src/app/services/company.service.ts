import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Company } from '../models/company.model';
import { BaseResponse } from '../models/baseresponse.model';

@Injectable({
  providedIn: 'root'
})
export class CompanyService {
  private apiUrl = 'company';

  constructor(private http: HttpClient) { }

  all() {
    return this.http.get<BaseResponse<Company[]>>(`${this.apiUrl}`);
  }

  get(id: number) {
    return this.http.get<BaseResponse<Company>>(`${this.apiUrl}/${id}`);
  }

  update(company: Company) {
    return this.http.put<BaseResponse<Company>>(`${this.apiUrl}/${company.id}`, company);
  }

  register(company: {name: string, email: string, password: string, reTypePassword: string, companyName: string}) {
    return this.http.post<BaseResponse<Company>>(`${this.apiUrl}`, company);
  }

  delete(id: number) {
    return this.http.delete<BaseResponse<any>>(`${this.apiUrl}/${id}`);
  }
}