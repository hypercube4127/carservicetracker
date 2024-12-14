import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { MaterialModule } from '../../material.module';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterService } from '../../services/router.service';
import { PackageInfoService  } from '../../services/package.info.service';

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
  packageInfo = this.packageInfoService.packageInfo;
  
  constructor(
    private authService: AuthService, 
    private router: RouterService,
    private packageInfoService: PackageInfoService
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
        console.log('Login success');
        this.router.navigateToDashboard();
      },
      error: (err) => {
        console.error('Login failed', err);
      }
    });
  }

}