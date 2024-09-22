export interface User {
  // User info
  id: number;
  email: string;
  fullname: string;
  newPassword: string;
  reTypePassword: string;

  // Address
  country: string;
  street: string;
  city: string;
  state: string;
  zip_code: string;

  // Avatar
  avatar: string;
}