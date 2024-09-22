import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';
import { StatModule } from '../shared/stat/stat.module';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  imports: [
    MaterialModule,
    StatModule
  ]
})
export class DashboardComponent {

  constructor() { }

  ngOnInit(): void {
    console.log('Dashboard component initialized');
  }


}