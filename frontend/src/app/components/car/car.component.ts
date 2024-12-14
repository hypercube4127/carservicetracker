import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';
import { Car } from '../../models/car.model';
import { CarService } from '../../services/car.service';
import { AuthService } from '../../services/auth.service';
import { RouterService } from '../../services/router.service';
import { UrlPlaceholders } from '../../constants/url.placeholders';

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

  protected currentSiteId: number | null = null;
  protected currentCompanyId: number | null = null;

  displayedColumns: string[] = ['make', 'model', 'year', 'plate', 'vin', 'actions'];
  carList: Car[] = [];

  constructor(private authService: AuthService, private carService: CarService, private router: RouterService) { }

  ngOnInit(): void {
    this.currentCompanyId = this.authService.getCurrentCompanyId();
    this.currentSiteId = this.authService.getCurrentSiteId();
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
    this.router.navigate([...UrlPlaceholders.COMPANY_SITE_PATH, 'car', 'new']);
  }

  viewWorksheets(car: Car): void {
    console.log('Viewing worksheets for car:', car);
  }
}