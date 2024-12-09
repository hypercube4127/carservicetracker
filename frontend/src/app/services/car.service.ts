import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Car } from '../models/car.model';
import { environment } from '../../environments/environment';
import { BaseResponse } from '../models/baseresponse.model';
import { UrlPlaceholder } from '../models/shared.model';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CarService {
  private apiUrl = environment.backendUrl + '/company/' + UrlPlaceholder.COMPANY + '/car';

  constructor(private http: HttpClient) {
  }

  all() {
    return this.http.get<BaseResponse<Car[]>>(`${this.apiUrl}`);
  }

  get(id: number) {
    return this.http.get<BaseResponse<Car>>(`${this.apiUrl}/${id}`);
  }

  update(car: Car) {
    return this.http.put<BaseResponse<Car>>(`${this.apiUrl}/${car.id}`, car);
  }

  save(car: {name: string, email: string, password: string, reTypePassword: string, companyName: string}) {
    return this.http.post<BaseResponse<Car>>(`${this.apiUrl}`, car);
  }

  delete(id: number) {
    return this.http.delete<BaseResponse<any>>(`${this.apiUrl}/${id}`);
  }

  search(search: string) {
    const params = new HttpParams().set('query', search);
    return this.http.get<BaseResponse<Car[]>>(`${this.apiUrl}/search`, {params});
  }
}