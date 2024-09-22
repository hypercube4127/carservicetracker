import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Token } from '../models/auth.model';
import { LocalStorageService } from './localstorage.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient, private localStorageService: LocalStorageService) { 
  }

  getDecodedToken(): Token | null {
    const token = this.getToken();
    if (token) {
      try {
        const payload = token.split('.')[1];
        const decodedPayload = atob(payload);
        return JSON.parse(decodedPayload) as Token;
      } catch (error) {
        console.error(error);
        return null;
      }
    }
    return null;
  }

  // FIXME Change any to a type
  login(credentials: { email: string, password: string }): Observable<any> {
    const endpointUrl = `${environment.backendUrl}/auth/login`;
    return this.http.post<any>(endpointUrl, credentials);
  }

  refreshToken(): Observable<any> {
    const endpointUrl = `${environment.backendUrl}/auth/refreshtoken`;
    return this.http.get(endpointUrl);
  }

  setToken(token: string): void {
    this.localStorageService.set('token', token);
  }

  getToken(): string | null {
    return this.localStorageService.get('token');
  }

  isLoggedIn(): boolean {
    const token = this.getDecodedToken();
    if (token) {
      return token.exp >= Date.now() / 1000;
    }
    return false;
  }

  logout(): void {
    console.log('Remove token');
    this.localStorageService.remove('token');
  }
}