import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../material.module';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'session-countdown',
  standalone: true,
  templateUrl: './session-countdown.component.html',
  styleUrls: ['./session-countdown.component.scss'],
  imports: [
    MaterialModule,
    CommonModule
  ]
})
export class SessionCountdownModule implements OnInit, OnDestroy {
  totalSeconds: number = 600;
  timeLeftFormatted: string = '';
  private intervalId: any;

  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit(): void {
    this.refreshTokenExpirationTime();
    this.startTimer();
  }

  ngOnDestroy(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  extendSession(): void {
    this.authService.refreshToken().subscribe({
      next: (response) => {
        console.log('Token refreshed', response);
        this.refreshTokenExpirationTime();
      },
      error: (err) => {
        console.error('Token refresh failed', err);
      }
    });
  }

  refreshTokenExpirationTime(): void { 
    const token = this.authService.getDecodedToken();
    if(!token) {
      this.router.navigate(['login']);
      return;
    }
    this.totalSeconds = token.exp - Date.now() / 1000;
  }

  startTimer(): void {
    this.updateTime();
    this.intervalId = setInterval(() => {
      if (this.totalSeconds >= 0) {
        this.totalSeconds--;

        this.updateTime();
      } else {
        this.authService.logout();
        this.router.navigate(['login']);
        clearInterval(this.intervalId);
      }
    }, 1000);
  }

  updateTime(): void {
    var unit = 'h';
    var number = 0;
    if (this.totalSeconds >= 3600) {
      number = Math.floor(this.totalSeconds / 3600);
    } else if (this.totalSeconds >= 60) {
      number = Math.floor(this.totalSeconds / 60);
      unit = 'm';
    } else {
      number = Math.floor(this.totalSeconds);
      unit = 's';
    }
    this.timeLeftFormatted = number + unit;
  }

}