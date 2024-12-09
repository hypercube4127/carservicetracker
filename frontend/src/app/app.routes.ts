import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

// Without authentication
import { LoginComponent } from './components/login/login.component';
import { RegisterCompanyComponent } from './components/register/company/register.component';
import { ConfirmComponent } from './components/confirm/confirm.component';

// Layouts
import { AdminLayoutComponent } from './components/admin-layout/admin-layout.component';

// Common components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { ProfileComponent } from './components/profile/profile.component';

// Car components
import { CarComponent } from './components/car/car.component';
import { EditCarComponent } from './components/car/edit/edit-car.component';
import { UrlParamsResolver } from './resolvers/url.param.resolver';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'registercompany', component: RegisterCompanyComponent },
  { path: 'confirm', component: ConfirmComponent },
  { 
    path: 'company/:company_id/site/:site_id', 
    component: AdminLayoutComponent,
    resolve: { params: UrlParamsResolver},
    children: [
      { path: 'dashboard', component: DashboardComponent, pathMatch: 'full', canActivate: [AuthGuard] },
      { path: 'profile', component: ProfileComponent, pathMatch: 'full', canActivate: [AuthGuard] },
      { path: 'car', component: CarComponent, pathMatch: 'full', canActivate: [AuthGuard] },
      { path: 'car/:car_id', component: EditCarComponent, pathMatch: 'full', canActivate: [AuthGuard] },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }