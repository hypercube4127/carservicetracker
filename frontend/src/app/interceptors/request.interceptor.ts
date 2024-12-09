import { HttpEvent, HttpRequest, HttpResponse, HttpErrorResponse, HttpHandlerFn } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { inject } from '@angular/core';
import { BaseResponse, Level, Message } from '../models/baseresponse.model';
import { ToastrService } from 'ngx-toastr';
import { UrlPlaceholder } from '../models/shared.model';
import { LocalStorageService } from '../services/localstorage.service';

export function requestInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> {
  if (req.method === 'OPTIONS') {
    return next(req);
  }

  const authService = inject(AuthService);
  const localStorageService = inject(LocalStorageService);
  const toastr = inject(ToastrService);
  const token = authService.getToken();
  const companyId = localStorageService.get<number>('company_id');
  const siteId = localStorageService.get<number>('site_id');

  console.debug('Token:', token);
  if (token) {

    //console.debug('AppContext Site:', contextHolder.getSiteId());
  
    var newUrl = req.url;

    if (req.url.includes(UrlPlaceholder.COMPANY) && companyId) {
      newUrl = req.url.replace(UrlPlaceholder.COMPANY, companyId.toString());
    }

    if (req.url.includes(UrlPlaceholder.SITE) && siteId) {
      newUrl = req.url.replace(UrlPlaceholder.SITE, siteId.toString());
    }
    
    req = req.clone({
      url: newUrl,
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }
  return next(req).pipe(
    tap(event => {
      if (event instanceof HttpResponse) {
        
        const body = event.body as BaseResponse<any>;
        if (body.token) {
            authService.setToken(body.token);
        }
        const messages = body.messages;
        if (messages) {
          messages.forEach((message: Message) => {
            console.log('Message:', message);
            switch (message.level) {
              case Level.ERROR:
                toastr.error(message.message);
                break;
              case Level.WARNING:
                toastr.warning(message.message);
                break;
              case Level.SUCCESS:
                toastr.success(message.message);
                break;
              default:
                toastr.info(message.message);
                break;
            }
          });
        }
      }
      // Handle successful responses here if needed
      console.log('Response event:', event);
    }),
    tap({
      error: (error: HttpErrorResponse) => {
        if(error.error.messages) {
          error.error.messages.forEach((message: Message) => {
            toastr.error(message.message);
          });
        }
        console.error('Error:', error);
      }
    })
  );
}