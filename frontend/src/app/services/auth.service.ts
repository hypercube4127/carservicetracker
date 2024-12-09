import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, firstValueFrom, map, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { Login, Token } from '../models/auth.model';
import { LocalStorageService } from './localstorage.service';
import { Site } from '../models/site.model';
import { Company } from '../models/company.model';
import { CompanySites } from '../models/companysites.model';
import { BaseResponse } from '../models/baseresponse.model';
import { CompanyService } from './company.service';
import { resolve } from 'path';
import { SiteService } from './site.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = environment.backendUrl + '/auth';

  private currentSite: Site | null = null;
  private currentCompany: Company | null = null;

  constructor(private http: HttpClient, private localStorageService: LocalStorageService, private companyService: CompanyService, private siteService: SiteService) { 
    this.getCurrentCompany();
    this.getCurrentSite();
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

  login(credentials: { email: string, password: string }): Observable<BaseResponse<Login>> {
    const endpointUrl = `${this.apiUrl}/login`;
    return this.http.post<any>(endpointUrl, credentials);
  }

  availableCompanyAndSiteMap(): Observable<BaseResponse<CompanySites[]>> {
    const endpointUrl = `${this.apiUrl}/available-sites`;
    return this.http.get<any>(endpointUrl);
  }

  refreshToken(): Observable<any> {
    const endpointUrl = `${this.apiUrl}/refreshtoken`;
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

  getCurrentCompanyId(): number | null {
    return this.localStorageService.get<number>('company_id');
  }

  getCurrentSiteId(): number | null {
    return this.localStorageService.get<number>('site_id');
  }

  getCurrentCompany(): Observable<Company | null> {
    const companyId = this.localStorageService.get<number>('company_id');
    if (companyId) {
      if (this.currentCompany?.id === companyId) {
        return of(this.currentCompany);
      }
  
      return this.companyService.get(companyId).pipe(
        map((response) => {
          this.currentCompany = response.data;
          return this.currentCompany;
        }),
        catchError((error) => {
          console.error('Failed to load company', error);
          return of(null);
        })
      );
    }

    return of(null);
  }

  getCurrentSite(): Observable<Site | null> {
    const siteId = this.localStorageService.get<number>('site_id');
    if (siteId && siteId !== 0) {
      if (this.currentSite?.id === siteId) {
        return of(this.currentSite);
      }
    
      return this.siteService.get(siteId).pipe(
        map((response) => {
          this.currentSite = response.data;
          return this.currentSite;
        }),
        catchError((error) => {
          console.error('Failed to load site', error);
          return of(null);
        })
      );
    }

    return of(null);
  }


}