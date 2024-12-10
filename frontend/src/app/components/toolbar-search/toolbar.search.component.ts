import { Component, OnInit } from '@angular/core';
import { MaterialModule } from '../../material.module';
import { debounceTime, distinctUntilChanged, filter, Subject } from 'rxjs';
import { CarService } from '../../services/car.service';
import { Car } from '../../models/car.model';

@Component({
  selector: 'toolbar-search',
  standalone: true,
  templateUrl: './toolbar.search.component.html',
  styleUrls: ['./toolbar.search.component.scss'],
  imports: [
    MaterialModule
  ]
})
export class ToolbarSearchModule implements OnInit {

  private searchSubject = new Subject<string>();

  protected carHits: Car[] = [];

  constructor(
    private carService: CarService
  ) { }


  ngOnInit(): void {
    this.searchSubject.pipe(
      debounceTime(750),
      distinctUntilChanged(),
      filter(text => text.length >= 3)
    ).subscribe(searchText => {
      this.performSearch(searchText);
    });
  }

  onSearch(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.searchSubject.next(input.value);
  }

  performSearch(query: string): void {
    this.carService.search(query).subscribe((results) => {
      console.log('Search results:', results);
    });
    console.log('Search for:', query);
  }

  openCarDetails(car: Car): void {
    console.log('Open car details:', car);
  }
}