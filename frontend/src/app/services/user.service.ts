import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from '../models/user.model';
import { BaseResponse } from '../models/baseresponse.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'user';

  constructor(private http: HttpClient) { }

  all() {
    return this.http.get<User[]>(`${this.apiUrl}`);
  }

  get(id: number) {
    return this.http.get<BaseResponse<User>>(`${this.apiUrl}/${id}`);
  }

  update(user: User) {
    return this.http.put<BaseResponse<User>>(`${this.apiUrl}/${user.id}`, user);
  }

  delete(id: number) {
    return this.http.delete<BaseResponse<any>>(`${this.apiUrl}/${id}`);
  }
}