import { Injectable } from '@angular/core';
import packageJson from '../../../package.json';

type PackageInfo = {
  version: string;
  build: string;
  commit: string;
};

@Injectable({
    providedIn: 'root'
  })
export class PackageInfoService {
  private _packageInfo: PackageInfo = {
    version: packageJson.version,
    build: packageJson.build,
    commit: packageJson.commit,
  };

  get packageInfo() {
    return this._packageInfo;
  }
}
