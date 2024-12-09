import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';
import { Car } from '../../models/car.model';
import { CarService } from '../../services/car.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-car',
  standalone: true,
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.scss'],
  imports: [
    MaterialModule
  ]
})
export class CarComponent {

  displayedColumns: string[] = ['make', 'model', 'year', 'plate', 'vin', 'actions'];
  carList: Car[] = [];

  constructor(private carService: CarService, private router: Router) { }

  ngOnInit(): void {
    this.carService.all().subscribe({
      next: (cars) => {
        this.carList = cars.data;
      },
      error: (err) => {
        console.error('Failed to load cars', err);
      }
    });
  }

  editCar(car: Car): void {
    console.log('Editing car:', car);
    this.router.navigate(['admin', 'car', car.id]);
  }

  deleteCar(car: Car): void {
    console.log('Deleting car:', car);
  }

  addCar(): void {
    console.log('Adding new car');
  }

  viewWorksheets(car: Car): void {
    console.log('Viewing worksheets for car:', car);
  }
}