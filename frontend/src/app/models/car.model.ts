export interface Car {

  id: number;

  vin: string;
  model: string;
  make: string;
  year: number;

  plate: string;
  plate_normalized: string;
  engine_number: string;
  engine_code: string;
  power: number;
  technical_exam_expiration: Date;

  company_id: number;
}
