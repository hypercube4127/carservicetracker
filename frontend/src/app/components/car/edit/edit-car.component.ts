import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { CarService } from '../../../services/car.service';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../../material.module';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { debounceTime, distinctUntilChanged, filter, Subject } from 'rxjs';

@Component({
  selector: 'app-car-edit',
  standalone: true,
  templateUrl: './edit-car.component.html',
  styleUrls: ['./edit-car.component.scss'],
  imports: [
    MaterialModule,
    CommonModule
  ]
})
export class EditCarComponent {

  private vinDecodeSubject = new Subject<string>();

  protected carForm!: FormGroup;

  constructor(private router: Router, private route: ActivatedRoute, private carService: CarService) {
    this.carForm = new FormGroup({
      id: new FormControl(''),
      vin: new FormControl('', [Validators.required]),
      plate: new FormControl('', [Validators.required]),
      make: new FormControl('', [Validators.required]),
      model: new FormControl('', [Validators.required]),
      year: new FormControl('', [Validators.required]),
      engineNumber: new FormControl('', [Validators.required]),
      engineCode: new FormControl('', [Validators.required]),
      power: new FormControl('', [Validators.required]),
      technicalExamExpiration: new FormControl('', [Validators.required])
    })
  }

  ngOnInit(): void {
    this.carForm.reset();

    this.route.params.subscribe(params => {
      const id = Number(params['car_id']);
      if (isNaN(id)) {
        return;
      }
      console.log('Car ID: ', id);
      this.carService.get(id).subscribe(response => {

      });
    });

    this.vinDecodeSubject.pipe(
      debounceTime(500),
      distinctUntilChanged(),
      filter(text => text.length >= 3)
    ).subscribe(searchText => {
      this.performVinDecode(searchText);
    });
  }

  onModifyVin(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.vinDecodeSubject.next(input.value);
  }

  performVinDecode(vin: string): void {
    this.carService.vinDecode(vin).subscribe((results) => {
      console.log('Decoded VIN:', results);
    });
  }

  saveCar() {
    this.router.navigate(['/car']);
  }

}