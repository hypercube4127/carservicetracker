import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { CompanyService } from '../../../services/company.service';
import { MaterialModule } from '../../../material.module';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

interface RegisterCompanyForm {
  name: FormControl,
  email: FormControl,
  password: FormControl,
  reTypePassword: FormControl
  companyName: FormControl
}

@Component({
  selector: 'app-register-company',
  standalone: true,
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  imports: [
    MaterialModule,
    ReactiveFormsModule
  ]
})
export class RegisterCompanyComponent {
  registerForm!: FormGroup<RegisterCompanyForm>;

  constructor(
    private authService: AuthService,
    private companyService: CompanyService, 
    private router: Router
  ) {
    this.registerForm = new FormGroup({
      name: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(6)]),
      reTypePassword: new FormControl('', [Validators.required, Validators.minLength(6)]),
      companyName: new FormControl('', [Validators.required])
    })
  }

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      console.log('Already logged in');
      this.router.navigate(['admin', 'dashboard']);
    }
  }

  register(): void {
    var company = {
      name: this.registerForm.value.name,
      email: this.registerForm.value.email,
      password: this.registerForm.value.password,
      reTypePassword: this.registerForm.value.reTypePassword,
      companyName: this.registerForm.value.companyName
    };
    this.companyService.register(company).subscribe({
      next: () => {
        this.router.navigate(['login']);
      },
      error: (err) => {
        console.error('Register failed', err);
      }
    });
  }

  goLogin(): void {
    this.router.navigate(['login']);
  }
}