import { HttpClient } from '@angular/common/http';
import { inject, Inject, Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RiotService {
  httpClient = inject(HttpClient);
  constructor() { }


  async getCurrentPatchVersion(): Promise<any> {
    return await lastValueFrom(this.httpClient.get("https://ddragon.leagueoflegends.com/api/versions.json"));
  }


}
