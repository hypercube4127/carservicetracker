import { HttpEvent, HttpRequest, HttpResponse, HttpErrorResponse, HttpHandlerFn } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { inject } from '@angular/core';
import { BaseResponse, Level, Message } from '../models/baseresponse.model';
import { ToastrService } from 'ngx-toastr';

export function authTokenInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> {
  const authService = inject(AuthService);
  const toastr = inject(ToastrService);
  
  const token = authService.getToken();
  console.log('Token:', token);
  if (token) {
    req = req.clone({
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
        error.error.messages.forEach((message: Message) => {
          toastr.error(message.message);
        });
        console.error('Error:', error);
      }
    })
  );
}