import { Company } from "./company.model";
import { Site } from "./site.model";

export interface CompanySites extends Company {
  selected: boolean;
  sites : CompanySite[];
}

export interface CompanySite extends Site {
  selected: boolean;
}