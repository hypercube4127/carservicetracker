import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatTooltipModule } from '@angular/material/tooltip';

@NgModule({
  exports: [
		MatButtonModule,
		MatInputModule,
		MatGridListModule,
		MatCardModule,
		MatIconModule,
		MatToolbarModule,
		MatSidenavModule,
		MatListModule,
		MatMenuModule,
		MatExpansionModule,
		MatTabsModule,
		MatFormFieldModule,
		MatSelectModule,
		MatTableModule,
		MatPaginatorModule,
		MatTooltipModule
	// Export other Angular Material modules as needed
  ]
})
export class MaterialModule { }