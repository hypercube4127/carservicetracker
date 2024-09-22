import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user.model';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../material.module';
import { AuthService } from '../../services/auth.service';
import { passwordMatchValidator } from '../../validators/password-match.validator';
import { CommonModule } from '@angular/common';
import { BaseResponse } from '../../models/baseresponse.model';
import { state } from '@angular/animations';

@Component({
  selector: 'app-profile',
  standalone: true,
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
  imports: [
    MaterialModule,
    ReactiveFormsModule,
    CommonModule
  ]
})
export class ProfileComponent implements OnInit {

  profileForm!: FormGroup;

  constructor(private userService: UserService, private authService: AuthService) { }

  ngOnInit(): void {
    this.profileForm = new FormGroup({
      id: new FormControl(''),
      fullname: new FormControl('', [Validators.required, Validators.minLength(4)]),
      email: new FormControl('', [Validators.required, Validators.email]),
      phone: new FormControl(''),

      newPassword: new FormControl('', [Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$|^$/)]),
      reTypePassword: new FormControl('', [Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$|^$/)]),
      
      country: new FormControl(''),
      state: new FormControl(''),
      city: new FormControl(''),
      street: new FormControl(''),
      address: new FormControl(''),
      zip_code: new FormControl('')
    }, { validators: passwordMatchValidator });

    this.load();
  }

  load(): void {
    const token = this.authService.getDecodedToken();

    if(!token) {
      throw new Error('No token found');
    }

    this.userService.get(token.sub).subscribe((response: BaseResponse<User>) => {
      this.profileForm.patchValue(response.data);
    });
  }

  update(): void {
    this.userService.update(this.profileForm.value).subscribe({
      next: () => {
        this.load();
        console.log('Profile updated');
      },
      error: (err) => {
        console.error('Profile update failed', err);
      }
    });
  }
}