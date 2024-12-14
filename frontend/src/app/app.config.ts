import { APP_INITIALIZER, ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideClientHydration } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { provideToastr } from 'ngx-toastr';
import { provideAnimations } from '@angular/platform-browser/animations';

import { routes } from './app.routes';
import { requestInterceptor } from './interceptors/request.interceptor';
import { ConfigService } from './services/config.service';
import { provideNativeDateAdapter } from '@angular/material/core';



export function initializeApp(configService: ConfigService): () => Promise<void> {

  return () => new Promise<void>((resolve) => {
    configService.load().then((config) => {
      resolve();
    })
  });
}

export const appConfig: ApplicationConfig = {
  providers: [
    {
      provide: APP_INITIALIZER,
      useFactory: initializeApp,
      deps: [ConfigService],
      multi: true
    },
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideClientHydration(),
    provideAnimations(),
    provideAnimationsAsync(),
    provideToastr(),
    provideHttpClient(withInterceptors([requestInterceptor]), withFetch()),
    provideNativeDateAdapter()
  ]};
