import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { MaterialModule } from '../../material.module';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ConfirmService } from '../../services/confirm.service';
import { isPlatformBrowser } from '@angular/common';
import { Inject, PLATFORM_ID } from '@angular/core';

interface ConfirmForm {
  code: FormControl
}

@Component({
  selector: 'app-confirm',
  standalone: true,
  templateUrl: './confirm.component.html',
  styleUrls: ['./confirm.component.scss'],
  imports: [
    MaterialModule,
    ReactiveFormsModule
  ]
})
export class ConfirmComponent {
  confirmForm!: FormGroup<ConfirmForm>;

  constructor(
    private authService: AuthService,
    private confirmService: ConfirmService, 
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.confirmForm = new FormGroup({
      code: new FormControl('', [Validators.required, Validators.minLength(4)])
    })
  }

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      if (code) {
        this.confirmForm.patchValue({ code });
        this.sendCode();
      }
    }
  }

  sendCode(): void {
    this.confirmService.send({ code: this.confirmForm.value.code }).subscribe({
      next: () => {
        if (this.authService.isLoggedIn()) {
          this.router.navigate(['admin', 'dashboard']);
        }
        this.router.navigate(['login']);
      },
      error: (err) => {
        console.error('Login failed', err);
      }
    });
  }

  goLogin(): void {
    this.router.navigate(['login']);
  }
}