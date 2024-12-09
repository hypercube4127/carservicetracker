import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { MaterialModule } from '../../material.module';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { LocalStorageService } from '../../services/localstorage.service';

interface LoginForm {
  email: FormControl,
  password: FormControl
}

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  imports: [
    MaterialModule,
    ReactiveFormsModule
  ]
})
export class LoginComponent {
  loginForm!: FormGroup<LoginForm>;

  constructor(
    private authService: AuthService, 
    private router: Router,
    private localStorageService: LocalStorageService
  ) {
    this.loginForm = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(6)])
    })
  }

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      console.log('Already logged in');
      this.router.navigate(['workspace']);
    }
  }

  registercompany(): void {
    this.router.navigate(['registercompany']);
  }

  login(): void {
    this.authService.login({ email: this.loginForm.value.email, password: this.loginForm.value.password }).subscribe({
      next: (response) => {
        console.log('Login success', response);
        this.autoSelectCompanyAndSite();
      },
      error: (err) => {
        console.error('Login failed', err);
      }
    });
  }

  private autoSelectCompanyAndSite(): void {
    const companyId = this.localStorageService.get<number>('company_id')
    const siteId = this.localStorageService.get<number>('site_id');

    this.authService.availableCompanyAndSiteMap().subscribe({
      next: (response) => {
        console.log('Available companies and sites', response);
        if (companyId && siteId) {
          const company = response.data.find((company) => company.id === companyId);
          if (company && siteId !== 0) {
            const site = company.sites.find((site) => site.id === siteId);
            if (site) {
              this.router.navigate(['company', company.id, 'site', site.id, 'dashboard']);
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

}