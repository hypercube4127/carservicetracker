import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../material.module';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { Company } from '../../models/company.model';
import { Site } from '../../models/site.model';
import { CompanySite, CompanySites } from '../../models/companysites.model';

@Component({
  selector: 'workspace-selector',
  standalone: true,
  templateUrl: './workspace-selector.component.html',
  styleUrls: ['./workspace-selector.component.scss'],
  imports: [
    MaterialModule,
    CommonModule
  ]
})
export class WorkspaceChangerModule implements OnInit {

  @Input() isMobile = false;
  protected availableCompaniesAndSites: CompanySites[] = [];
  protected currentCompany: Company | null = null;
  protected currentSite: Site | null = null;

  constructor(
    private authService: AuthService, 
    private router: Router
  ) {}

  ngOnInit(): void {
    console.log("Load Workspace selector");

    // Get current company and site
    this.authService.getCurrentCompany().subscribe((company: Company | null) => {
      this.currentCompany = company;
      this.setSelected();
      console.log('WS Current company', company);
    });

    this.authService.getCurrentSite().subscribe((site: Site | null) => {
      this.currentSite = site;
      this.setSelected();
      console.log('WS Current site', site);
    });

    // Get available companies and sites
    this.authService.availableCompanyAndSiteMap().subscribe({
      next: (response) => {
        this.availableCompaniesAndSites = response.data;
        this.setSelected();
        console.log('Available companies and sites', response);
      },
      error: (err) => {
        console.error('Failed to get available companies and sites', err);
      }
    });
  }

  setSelected(): void {
    console.log('Set selected', this.currentCompany, this.currentSite);
    if (this.currentCompany) {
      this.availableCompaniesAndSites.forEach((companySites: CompanySites) => {
        if (companySites.id === this.currentCompany?.id) {
          if (this.currentSite) {
            companySites.sites.forEach((site: CompanySite) => {
              if (site.id === this.currentSite?.id) {
                site.selected = true;
              }
            });
          } else {
            companySites.selected = true;
          }
        }
      });
    }
  }

  changeWorkspace(companyId: number, siteId: number | null): void {
    this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
      if (siteId) {
        this.router.navigate(['company', companyId, 'site', siteId, 'dashboard']);
      } else {
        this.router.navigate(['company', companyId, 'site', 0, 'dashboard']);
      }
    });

  }
}