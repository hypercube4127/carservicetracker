import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export const passwordMatchValidator: ValidatorFn = (control: AbstractControl): null => {
  
  const newPassword = control.get('newPassword');
  const reTypePassword = control.get('reTypePassword');

  if (newPassword && reTypePassword && newPassword.value !== reTypePassword.value) {
    reTypePassword.setErrors({...reTypePassword.errors, 'passwordMismatch': true });
  } else if (reTypePassword) {
    const filteredErrors = Object.keys(reTypePassword.errors || {}).filter(key => key !== 'passwordMismatch');
    if(filteredErrors.length !== 0) {
      reTypePassword.setErrors(filteredErrors);
    } else {
      reTypePassword.setErrors(null);
    }
  }
  return null
};