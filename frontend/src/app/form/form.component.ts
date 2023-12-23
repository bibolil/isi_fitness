import { Component,ElementRef  } from '@angular/core';
import { FitnessService } from '../app-service.service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.css']
})
export class FormComponent {

  constructor(private http: HttpClient,private router: Router,private fitnessService: FitnessService) {}
  

  name: string = "";

  iteration = 0;
  progressValue: number = 0;

  isAllergiesChecked: boolean = false;
  isIntolerancesChecked: boolean = false;
  isChronicConditionsChecked: boolean = false;
  isMedicationsChecked: boolean = false;
  isSurgeriesChecked: boolean = false;
  smoking_state:string="";
  allergies_string:string="";
  intolerances_string:string="";
  chronic_conditions_string:string="";
  medications_string:string="";
  surgeries_string:string="";
  checked: string="";
  loading:boolean=false;
  //variables for request
  weight_management: string="";
  strength_goal: boolean = false; 
  flexibility_goal: boolean = false;
  endurance_goal: boolean = false;
  height: number = 0;
  weight: number = 0;
  age: number = 0;
  gender: string = "";
  occupation: string = "";
  sleep_hours: number = 0;
  stress_level: string = "";
  smoking: boolean = false;
  diet_type:string="";
  activity_level:string="";
  allergies:string[]=[];
  intolerances:string[]=[];
  current_physical_health:string="";
  chronic_conditions:string[]=[];
  medications:string[]=[];
  recent_surgeries_or_injuries:string[]=[];





  setname(name: string) {
    this.name = name;
  }

  stringToList(input: string): string[] {
    return input.split(',');
}

  continue() {
      switch(this.iteration) {
      case 0:
        break;
      case 1:
        this.setname((<HTMLInputElement>document.getElementById("FullName")).value);
        break;
      case 2:
        switch(this.checked)
        {
          case "1":
            this.weight_management="gain weight"
            break;
          case "2":
            this.weight_management="lose weight"
            break;
          case "3":
            this.weight_management="maintain weight"
            break;
        }

        break;
      case 3:
        if(this.smoking_state==="smoker")
        {
          this.smoking=true;
        }
        break;
      case 4:
        if(this.isAllergiesChecked)
        {
          this.allergies=this.stringToList(this.allergies_string);
        }
        if(this.isIntolerancesChecked)
        {
          this.intolerances=this.stringToList(this.intolerances_string);
        }
        break;
      case 5:
        if(this.isChronicConditionsChecked)
        {
          this.chronic_conditions=this.stringToList(this.chronic_conditions_string);
        }
        if(this.isMedicationsChecked)
        {
          this.medications=this.stringToList(this.medications_string);
        }
        if(this.isSurgeriesChecked)
        {
          this.recent_surgeries_or_injuries=this.stringToList(this.surgeries_string);
        }
        break;
    }
    this.iteration++;
    this.progressValue = this.progressValue + 20;
  }


  return() {
    this.iteration--;
    this.progressValue = this.progressValue - 20;
  }

  sendData() {
    const fitnessData = {
      weight_management: this.weight_management,
      strength_goal: this.strength_goal,
      flexibility_goal: this.flexibility_goal,
      endurance_goal: this.endurance_goal,
      height: this.height,
      weight: this.weight,
      age: this.age,
      gender: this.gender,
      occupation: this.occupation,
      sleep_hours: this.sleep_hours,
      stress_level: this.stress_level,
      smoking: this.smoking,
      diet_type: this.diet_type,
      activity_level: this.activity_level,
      allergies: this.allergies,
      intolerances: this.intolerances,
      current_physical_health: this.current_physical_health,
      chronic_conditions: this.chronic_conditions,
      medications: this.medications,
      recent_surgeries_or_injuries: this.recent_surgeries_or_injuries
    };
    console.log(fitnessData);
    this.loading=true;
    this.http.post("http://localhost:5000/api", fitnessData).subscribe(
      {
      next: (data: any) => {
        console.log(data);
        this.fitnessService.setgym_plan(data["response"] as string);
        this.loading=false;
        this.router.navigate(['/plan']);
      },
      error: (error: any) => {
        console.error('There was an error!', error);
      }
    });

  }

}
