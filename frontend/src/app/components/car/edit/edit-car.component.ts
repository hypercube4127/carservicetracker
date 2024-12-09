import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { CarService } from '../../../services/car.service';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../../material.module';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

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

  carForm!: FormGroup;

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
    this.route.params.subscribe(params => {
      const id = params['id'];
      console.log('Car ID: ', id);
      this.carService.get(id).subscribe(response => {

      });
    });
  }

  saveCar() {
    this.router.navigate(['/car']);
  }

}