import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class UrlParamsResolver implements Resolve<any> {
  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): any {
    const companyId = route.params['company_id'];
    console.log('ParamsResolver set company_id', companyId);
    if(companyId) {
      localStorage.setItem('company_id', companyId);
    } else {
      localStorage.removeItem('company_id');
    }

    const siteId = route.params['site_id'];
    console.log('ParamsResolver set site_id', siteId);
    if(siteId) {
      localStorage.setItem('site_id', siteId);
    } else {
      localStorage.removeItem('site_id');
    }
  }
}