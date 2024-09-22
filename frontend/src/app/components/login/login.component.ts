import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { MaterialModule } from '../../material.module';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

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
  ],
  providers: [
    AuthService
  ]
})
export class LoginComponent {
  loginForm!: FormGroup<LoginForm>;

  constructor(
    private authService: AuthService, 
    private router: Router
  ) {
    this.loginForm = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(6)])
    })
  }

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      console.log('Already logged in');
      this.router.navigate(['admin', 'dashboard']);
    }
  }

  login(): void {
    this.authService.login({ email: this.loginForm.value.email, password: this.loginForm.value.password }).subscribe({
      next: () => {
        console.log('Login success');
        this.router.navigate(['admin', 'dashboard']);
      },
      error: (err) => {
        console.error('Login failed', err);
      }
    });
  }
}