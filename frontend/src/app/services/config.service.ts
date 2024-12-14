import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

export type AppConfig = {
  production: boolean;
  backendUrl: string;
  locales: string[];
  defaultLocale: string;
}

@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  private _http = inject(HttpClient);
  private _config!: AppConfig;
  
  get config(): any {
    return this._config;
  }

  load(): Promise<AppConfig> {
    return new Promise<AppConfig>((resolve, reject) => {
      const url = `./assets/config.json?donotcache=${new Date().getTime()}`;
      firstValueFrom(this._http.get(url))
        .then((response) => {
          this._config = <AppConfig>response;
          resolve(this._config);
        })
        .catch(() => {
          reject('Could not load the config file');
        });
    });
  }

}