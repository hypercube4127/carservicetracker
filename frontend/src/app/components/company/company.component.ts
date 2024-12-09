import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CompanyService } from '../../services/company.service';
import { Company } from '../../models/company.model';
import { MaterialModule } from '../../material.module';

@Component({
  selector: 'app-company',
  standalone: true,
  templateUrl: './company.component.html',
  styleUrls: ['./company.component.scss'],
  imports: [
    MaterialModule
  ]
})
export class CompanyComponent implements OnInit {
  companyForm!: FormGroup;
  companies: Company[] = [];
  selectedCompany: Company | null = null;

  constructor(private companyService: CompanyService, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.companyForm = this.fb.group({
      id: [''],
      name: ['', Validators.required],
      address: [''],
      phone: ['']
    });
    this.loadCompanies();
    console.log('Company component initialized');
  }

  loadCompanies(): void {
    this.companyService.all().subscribe({
      next: (companies) => {
        this.companies = companies;
      },
      error: (err) => {
        console.error('Failed to load companies', err);
      }
    });
  }

  createCompany(): void {
    if (this.companyForm.valid) {
      this.companyService.register(this.companyForm.value).subscribe({
        next: () => {
          this.companyForm.reset();
        },
        error: (err) => {
          console.error('Failed to create company', err);
        }
      });
    }
  }

  updateCompany(): void {
    if (this.selectedCompany && this.companyForm.valid) {
      this.companyService.update(this.companyForm.value).subscribe({
        next: (result) => {
          var company = result.data
          const index = this.companies.findIndex(c => c.id === company.id);
          if (index !== -1) {
            this.companies[index] = company;
          }
          this.selectedCompany = null;
          this.companyForm.reset();
        },
        error: (err) => {
          console.error('Failed to update company', err);
        }
      });
    }
  }

  deleteCompany(id: number): void {
    this.companyService.delete(id).subscribe({
      next: () => {
        this.companies = this.companies.filter(c => c.id !== id);
      },
      error: (err) => {
        console.error('Failed to delete company', err);
      }
    });
  }

  selectCompany(company: Company): void {
    this.selectedCompany = company;
    this.companyForm.patchValue(company);
  }

  clearSelection(): void {
    this.selectedCompany = null;
    this.companyForm.reset();
  }
}