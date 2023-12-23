import { Component } from '@angular/core';
import { FitnessService } from '../app-service.service';

@Component({
  selector: 'app-markdown-display',
  templateUrl: './markdown-display.component.html',
  styleUrls: ['./markdown-display.component.css']
})
export class MarkdownDisplayComponent {

  constructor(private fitnessService:FitnessService) { }

  markdown: string="";

  ngOnInit(): void {
    this.markdown=this.fitnessService.getgym_plan();
  }

  // markdown = `## 1-Week Training and Diet Plan for Male, Low-Fat, Muscle Building:

  // **Disclaimer:** This is a general plan and should be adjusted based on individual needs and preferences. It's recommended to consult a certified personal trainer and registered dietitian for a personalized plan, especially considering smoking cessation and weight gain goals.
  
  // **Training:**
  
  // * **Monday:** Heavy weightlifting (Legs, Core) - Squats, lunges, deadlifts, planks, crunches. 3 sets of 8-12 reps.
  // * **Tuesday:** Rest or light cardio (walking, swimming).
  // * **Wednesday:** Heavy weightlifting (Upper body, Back) - Pull-ups, rows, bench press, shoulder press. 3 sets of 8-12 reps.
  // * **Thursday:** Rest or light cardio.
  // * **Friday:** Heavy weightlifting (Legs, Core) - Different variations of exercises from Monday. 3 sets of 8-12 reps.
  // * **Saturday:** Active rest (hiking, cycling, sports).
  // * **Sunday:** Rest or light cardio.
  
  // **Diet:**
  
  // **Calories:** Aim for a slight calorie surplus, roughly 250-500 calories more than your maintenance intake. Use online calculators or consult a dietitian for a personalized estimate.
  
  // **Macronutrients:**
  
  // * **Protein:** 1.5-2 grams per kilogram of body weight. Aim for 105-140 grams per day.
  // * **Carbohydrates:** 40-50% of total calories. Prioritize whole grains, fruits, and vegetables. Aim for 200-250 grams per day.
  // * **Fats:** 20-30% of total calories. Choose healthy fats from sources like avocado, nuts, seeds, and fatty fish. Aim for 50-70 grams per day.
  
  // **Sample Meal Plan:**
  
  // **Breakfast (500-600 calories):**
  
  // * 3 scrambled eggs with spinach and mushrooms
  // * Oatmeal with berries and nuts
  // * Greek yogurt with fruit and granola
  
  // **Mid-Morning Snack (200-300 calories):**
  
  // * Protein shake with banana and almond milk
  // * Handful of mixed nuts and dried fruit
  // * Cottage cheese with pineapple or chopped vegetables
  
  // **Lunch (600-700 calories):**
  
  // * Grilled chicken breast or salmon with brown rice and roasted vegetables
  // * Lentil soup with whole-wheat bread and avocado
  // * Tuna salad sandwich on whole-wheat bread with lettuce and tomato
  
  // **Afternoon Snack (200-300 calories):**
  
  // * Apple with peanut butter
  // * Greek yogurt with honey and seeds
  // * Carrot sticks with hummus
  
  // **Dinner (600-700 calories):**
  
  // * Turkey chili with kidney beans and whole-wheat tortilla
  // * Beef stir-fry with brown rice and broccoli
  // * Baked cod with quinoa and roasted Brussels sprouts
  
  // **Evening Snack (optional, 200-300 calories):**
  
  // * Casein protein shake
  // * Cottage cheese with berries
  // * Small bowl of whole-grain cereal with milk
  
  // **Health Considerations:**
  
  // * **Smoking cessation:** Focus on supporting your body during quitting through stress management, hydration, and nutrient-rich foods. Consider seeking professional help for quitting.
  // * **Weight gain:** Prioritize nutrient-dense whole foods over processed options. Monitor your progress and adjust calorie intake as needed.
  // * **Hydration:** Drink plenty of water throughout the day, especially during exercise. Aim for 2-3 liters per day.
  // * **Supplements:** Consider consulting a doctor or registered dietitian about suitable supplements, such as vitamin D or a multivitamin.
  
  // Remember, consistency is key! Stick to your training and diet plan as much as possible, and make adjustments as needed based on your progress and preferences. Be sure to listen to your body and rest when needed.`;

}
