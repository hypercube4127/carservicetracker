import { CommonModule } from '@angular/common';
import { Component, ViewChild } from '@angular/core';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MaterialModule } from '../../material.module';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';
import { MatSidenav } from '@angular/material/sidenav';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user.model';
import { BaseResponse } from '../../models/baseresponse.model';
import { SessionCountdownModule } from '../session-countdown/session-countdown.component';

@Component({
  selector: 'app-admin-layout',
  standalone: true,
  templateUrl: './admin-layout.component.html',
  styleUrls: ['./admin-layout.component.scss'],
  imports: [
    MaterialModule,
    RouterModule,
    CommonModule,
    SessionCountdownModule
  ]
})
export class AdminLayoutComponent {

  @ViewChild(MatSidenav)
  sidenav!: MatSidenav;
  isMobile= true;

  currentUser: User | null = null;

  constructor(private authService: AuthService, private userService: UserService, private router: Router, private observer: BreakpointObserver) { }

  ngOnInit() {

    this.observer.observe(['(max-width: 800px)']).subscribe((screenSize) => {
      if(screenSize.matches){
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    });

    const token = this.authService.getDecodedToken();
    if(!token) {
      this.router.navigate(['login']);
      return;
    }

    this.userService.get(token.sub).subscribe((response: BaseResponse<User>) => {
      console.log('Current user', response.data);
      this.currentUser = response.data;
    });
  }

  profile(): void {
    this.router.navigate(['admin', 'profile']);
  }

  dashboard(): void {
    this.router.navigate(['admin', 'dashboard']);
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['login']);
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    console.log('Filter value', filterValue);
  }

}