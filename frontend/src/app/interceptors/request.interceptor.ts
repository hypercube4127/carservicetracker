import { HttpResponse, HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { tap } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { inject } from '@angular/core';
import { BaseResponse, Level, Message } from '../models/baseresponse.model';
import { ToastrService } from 'ngx-toastr';
import { UrlPlaceholder } from '../models/shared.model';
import { ConfigService } from '../services/config.service';

export const requestInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.url.startsWith('./')) {
    return next(req);
  }

  const configService = inject(ConfigService);
  const authService = inject(AuthService);
  const toastr = inject(ToastrService);
  const token = authService.getToken();

  var url = `${configService.config.backendUrl}${req.url}`;
  var headers = req.headers;

  if (token) {
    // Add token to headers
    headers = headers.set('Authorization', `Bearer ${token}`);

    // Replace placeholders in URL
    const companyId = authService.getCurrentCompanyId();
    if (url.includes(UrlPlaceholder.COMPANY) && companyId) {
      url = url.replace(UrlPlaceholder.COMPANY, companyId.toString());
    }

    const siteId = authService.getCurrentSiteId();
    if (req.url.includes(UrlPlaceholder.SITE) && siteId) {
      url = url.replace(UrlPlaceholder.SITE, siteId.toString());
    }    
  }

  req = req.clone({
    url: url,
    headers: headers
  });

  if (req.method === 'OPTIONS') {
    return next(req);
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