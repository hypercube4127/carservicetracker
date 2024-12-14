import { Injectable } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { UrlPlaceholders } from '../constants/url.placeholders';

@Injectable({
  providedIn: 'root',
})
export class RouterService {

  constructor(private router: Router, private authService: AuthService) {}

  navigateToDashboard(): void {
    this.authService.availableCompanyAndSiteMap().subscribe({
      next: (response) => {
        var companyId = this.authService.getCurrentCompanyId();
        var siteId = this.authService.getCurrentSiteId();

        if (companyId && siteId) {
          const company = response.data.find((company) => company.id === companyId);
            if (company && siteId !== 0) {
              const site = company.sites.find((site) => site.id === siteId);
              if (site) {
                  this.router.navigate(['company', company.id, 'site', site.id, 'dashboard']);
                  return;
              }
            this.router.navigate(['company', company.id, 'site', 0, 'dashboard']);
            return;
          }
        }

        if (response.data.length === 1) {
          this.router.navigate(['company', response.data[0].id, 'site', 0, 'dashboard']);
          return;
        }
      },
      error: (err) => {
        console.error('Failed to get available companies and sites', err);
      }
    });
  }

  navigate(commands: any[], extras?: NavigationExtras): Promise<boolean> {
    commands = this.resolvePlaceholders(commands);
    return this.router.navigate(commands, extras);
  }

  private resolvePlaceholders(commands: any[]): any[] {
    return commands.map((command) => {
      if (typeof command === 'string') {
        return this.resolvePlaceholder(command);
      }
        return command;
      }
    );
  }

  private resolvePlaceholder(command: string): string {
    if(command.includes(UrlPlaceholders.COMPANY_ID)) {
      return this.authService.getCurrentCompanyId()?.toString() || command;
    } else if(command.includes(UrlPlaceholders.SITE_ID)) {
      return this.authService.getCurrentSiteId()?.toString() || command;
    }
    return command;
  }
}