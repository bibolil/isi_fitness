import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
    providedIn: 'root'
  })
  export class FitnessService {
    private apiUrl = 'http://localhost:5000/api'; // Replace with your API endpoint
  
    constructor(private http: HttpClient) { }
    gym_plan:string="";
  
    
    setgym_plan(gym_plan:string){
      this.gym_plan=gym_plan;
    }
    
    getgym_plan(){  
      return this.gym_plan;
    }
    
  }
  