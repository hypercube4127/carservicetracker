import { CompanySites } from "./companysites.model";

export type Token = {
  jti: string;
  sub: number;
  iss: string;
  iat: number;
  exp: number;
};

export type Login = {
  availableCompanySites: CompanySites[];
}
