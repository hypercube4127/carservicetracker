import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseResponse } from '../models/baseresponse.model';
import { Site } from '../models/site.model';
import { UrlPlaceholder } from '../models/shared.model';

@Injectable({
  providedIn: 'root'
})
export class SiteService {
  private apiUrl = 'company/' + UrlPlaceholder.COMPANY + '/site';

  constructor(private http: HttpClient) { }

  all() {
    return this.http.get<BaseResponse<Site[]>>(`${this.apiUrl}`);
  }

  get(id: number) {
    return this.http.get<BaseResponse<Site>>(`${this.apiUrl}/${id}`);
  }
  
  update(site: Site) {
    return this.http.put<BaseResponse<Site>>(`${this.apiUrl}/${site.id}`, site);
  }

  save(site: {name: string, email: string, password: string, reTypePassword: string, companyName: string}) {
    return this.http.post<BaseResponse<Site>>(`${this.apiUrl}`, site);
  }

  delete(id: number) {
    return this.http.delete<BaseResponse<any>>(`${this.apiUrl}/${id}`);
  }

}