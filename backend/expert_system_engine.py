from experta import *
from bardapi import Bard
import bardapi
from flask import *
from flask_cors import CORS

#flask init
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

#Helper functions

def calculate_bmi(height, weight):
    """ Calculate BMI based on height and weight if not provided. """
    if height > 0:
        return weight / (height ** 2)
    else:
        return None

def calculate_body_fat(height, weight, age, gender):
    # Calculate BMI
    bmi = weight / (height ** 2)
    
    if gender.lower() == 'male':
        body_fat_percentage = (1.20 * bmi) + (0.23 * age) - 16.2
    elif gender.lower() == 'female':
        body_fat_percentage = (1.20 * bmi) + (0.23 * age) - 5.4
    else:
        return "Invalid gender. Please enter 'male' or 'female'."

    return body_fat_percentage
#facts classes
class PersonalInfo(Fact):
    """
    Basic personal injsonation.
    Includes age, gender, occupation, sleep patterns, stress levels, and known medical conditions.
    """
    age = Field(int, mandatory=True)
    gender = Field(str, mandatory=True)  # could be 'male', 'female', 'other'
    occupation = Field(str, mandatory=True)  # type of job, which might affect activity level
    sleep_hours = Field(float, mandatory=True)  # average number of hours of sleep per night
    stress_level = Field(str, mandatory=True)  # could be 'low', 'medium', 'high'
    medical_conditions = Field(list, default=list)  # list of known medical conditions

class PhysicalAttributes(Fact):
    """
    Physical attributes relevant to fitness and nutrition.
    Includes height, weight, body mass index (BMI), body fat percentage, and waist circumference.
    """
    height = Field(float, mandatory=True)  # Height in meters
    weight = Field(float, mandatory=True)  # Weight in kilograms
    bmi = Field(float, default=None)  # Body Mass Index
    body_fat_percentage = Field(float, default=None)  # Body fat percentage

class Lifestyle(Fact):
    """
    Lifestyle injsonation including activity level, exercise habits, work environment, 
    daily routine, and habits like smoking and alcohol consumption.
    """
    activity_level = Field(str, mandatory=True)  # e.g., 'sedentary', 'moderately active', 'very active'
    smoking = Field(bool, default=False)  # Smoking habits
    stress_level = Field(str, default='medium')  # e.g., 'low', 'medium', 'high'

class DietaryPreferences(Fact):
    """
    Dietary preferences and restrictions including specific diet types, allergies, 
    and other dietary considerations.
    """
    diet_type = Field(str, default='omnivore')  # e.g., 'omnivore', 'vegetarian', 'vegan', 'pescatarian'
    allergies = Field(list, mandatory=True)  # List of known food allergies
    intolerances = Field(list, mandatory=True)  # List of known food intolerances


class HealthState(Fact):
    """
    Health state including current physical health, chronic conditions, recent surgeries or injuries,
    mental health status, and medications.
    """
    current_physical_health = Field(str, default='good')  # e.g., 'good', 'fair', 'poor'
    chronic_conditions = Field(list, mandatory=True)  # List of chronic conditions, if any
    recent_surgeries_or_injuries = Field(list, mandatory=True)  # List of recent surgeries or injuries
    medications = Field(list, mandatory=True)  # List of current medications

class FitnessGoals(Fact):
    """
    Specific fitness goals, including weight management, strength, endurance, 
    flexibility, and sport-specific training.
    """
    weight_management = Field(str, default=None)  # e.g., 'lose weight', 'gain weight', 'maintain weight'
    strength_goal = Field(bool, default=False)  # Goal to increase strength
    endurance_goal = Field(bool, default=False)  # Goal to increase endurance
    flexibility_goal = Field(bool, default=False)  # Goal to increase flexibility

class FitnessExpertSystem(KnowledgeEngine):
    def __init__(self,recommandation=None):
        super().__init__()
        self.recommandation = []
    

    #rules for gender
    @Rule(PersonalInfo(gender='male'), PhysicalAttributes(body_fat_percentage=P(lambda body_fat_percentage: body_fat_percentage > 20)))  # Example threshold for higher body fat in males
    def males_recommendation_high_fat(self):
        self.recommandation.append("Type: male high fat")
        self.recommandation.append("Training: Emphasize cardio and moderate weights.")
        self.recommandation.append("Diet: Slight calorie deficit, focus on lean proteins and complex carbs.")


    @Rule(PersonalInfo(gender='male'), PhysicalAttributes(body_fat_percentage=P(lambda body_fat_percentage: body_fat_percentage <= 20)))  # Example threshold for lower body fat in males
    def males_recommendation_low_fat(self):
        self.recommandation.append("Type: male low fat")
        self.recommandation.append("Training: Prioritize heavy weights, lower reps for muscle building.")
        self.recommandation.append("Diet: Maintenance or slight calorie surplus, balanced macronutrients.")


    @Rule(PersonalInfo(gender='female'), PhysicalAttributes(body_fat_percentage=P(lambda body_fat_percentage: body_fat_percentage > 30)))  # Example threshold for higher body fat in females
    def females_recommendation_high_fat(self):
        self.recommandation.append("Type: female high fat")
        self.recommandation.append("Training: Include strength training and varied workouts.")
        self.recommandation.append("Diet: Focus on a slight calorie deficit, emphasize protein for muscle retention.")
     

    @Rule(PersonalInfo(gender='female'), PhysicalAttributes(body_fat_percentage=P(lambda body_fat_percentage: body_fat_percentage <= 30)))  # Example threshold for lower body fat in females
    def females_recommendation_low_fat(self):
        self.recommandation.append("Type : female low fat")
        self.recommandation.append("Training: Incorporate strength training, adjust intensity for muscle definition.")
        self.recommandation.append("Diet: Maintenance calories or slight surplus, prioritize lean proteins and healthy fats.")

                


    #rules for weight management
    @Rule(FitnessGoals(weight_management='lose weight'),
          PhysicalAttributes(bmi=P(lambda bmi: bmi >= 25)))
    def weight_loss_recommendation(self):
        self.recommandation.append("Training Plan: Cardio-focused exercises, like running or cycling, 3-5 times a week.")
        self.recommandation.append("Diet Plan: Calorie deficit diet, focus on whole foods with high protein and fiber.")
        self.recommandation.append("Note: Adjust calorie intake based on activity level and weight loss goals.")


    @Rule(FitnessGoals(weight_management='gain weight'),
          PhysicalAttributes(bmi=P(lambda bmi: bmi < 18.5)))
    def weight_gain_recommendation(self):
        self.recommandation.append("Training Plan: Strength training with progressive overload, 3-4 times a week.")
        self.recommandation.append("Diet Plan: Calorie surplus with a focus on lean protein, complex carbs, and healthy fats.")
        self.recommandation.append("Note: Adjust calorie intake based on activity level and weight gain goals.")

    @Rule(AND(FitnessGoals(weight_management='maintain weight'),
          PhysicalAttributes(bmi=P(lambda bmi: 18.5 <= bmi <= 24.9))))
    def weight_maintenance_recommendation(self):
        self.recommandation.append("Training Plan: Aim for a balanced mix of cardiovascular and strength training exercises.")
        self.recommandation.append("Diet Plan: Focus on a balanced diet where caloric intake matches expenditure to maintain current weight.")
        self.recommandation.append("Note: Adjust calorie intake based on activity level and weight management goals.")

    #rules for goal specific training
    @Rule(FitnessGoals(endurance_goal=True))
    def endurance_training_recommendation(self):
        self.recommandation.append("Training Plan: Regular aerobic exercises like running, swimming, or cycling.")
        self.recommandation.append("Diet Plan: Balanced diet with adequate carbohydrates for energy.")

    @Rule(FitnessGoals(flexibility_goal=True))
    def flexibility_training_recommendation(self):
        self.recommandation.append("Training Plan: Daily stretching routines, yoga or pilates classes.")
        self.recommandation.append("Diet Plan: Well-balanced diet, stay hydrated.")

    @Rule(FitnessGoals(strength_goal=True))
    def strength_training_recommendation(self):
        self.recommandation.append("Training Plan: Focus on weightlifting and resistance training exercises.")
        self.recommandation.append("Diet Plan: Increase protein intake to support muscle growth and repair.")

    
    #rules taking into account age and health conditions

    #Children (Ages 6-12)
    @Rule(AND(PersonalInfo(age=P(lambda age: 6 <= age < 13)),
          HealthState(current_physical_health=MATCH.current_physical_health,
                      chronic_conditions=MATCH.chronic_conditions,
                      recent_surgeries_or_injuries=MATCH.recent_surgeries_or_injuries,
                      medications=MATCH.medications)
                      )
          )
    def children_fitness(self,current_physical_health,chronic_conditions,recent_surgeries_or_injuries,medications):
        self.recommandation.append("For children (6-12 years):")
        self.recommandation.append("Training Plan: Encourage active play and participation in sports.")
        self.recommandation.append("Diet Plan: Balanced diet with focus on calcium and iron for healthy growth.")
        if chronic_conditions or recent_surgeries_or_injuries or medications or current_physical_health != 'good':
            self.recommandation.append("Special considerations may be needed for children with specific health conditions or recent surgeries/injuries.")
            if chronic_conditions:
                self.recommandation.append("Chronic conditions:", ",".join(chronic_conditions))
            if recent_surgeries_or_injuries:
                self.recommandation.append("Recent surgeries or injuries:", ",".join(recent_surgeries_or_injuries))
            if medications:
                self.recommandation.append("Medications:", ",".join(medications))


    #Adolescents (Ages 13-17)
    @Rule(AND(PersonalInfo(age=P(lambda age: 13 <= age < 18)),
           HealthState(current_physical_health=MATCH.current_physical_health,
                      chronic_conditions=MATCH.chronic_conditions,
                      recent_surgeries_or_injuries=MATCH.recent_surgeries_or_injuries,
                      medications=MATCH.medications)))
    def adolescent_fitness(self,current_physical_health,chronic_conditions,recent_surgeries_or_injuries,medications):
        self.recommandation.append("For adolescents (13-17 years):")
        self.recommandation.append("Training Plan: Emphasis on physical activities for overall development; avoid heavy weightlifting.")
        self.recommandation.append("Diet Plan: Nutrient-rich diet to support growth, including fruits, vegetables, whole grains, and lean proteins.")
        if chronic_conditions or recent_surgeries_or_injuries or medications or current_physical_health != 'good':
            self.recommandation.append("Special considerations may be needed for adolescents with specific health conditions or recent surgeries/injuries.")
            if chronic_conditions:
                self.recommandation.append("Chronic conditions:", ",".join(chronic_conditions))
            if recent_surgeries_or_injuries:
                self.recommandation.append("Recent surgeries or injuries:", ",".join(recent_surgeries_or_injuries))
            if medications:
                self.recommandation.append("Medications:", ",".join(medications))

    #Young Adults (Ages 18-30)
    @Rule(AND(PersonalInfo(age=P(lambda age: 18 <= age < 30)),
           HealthState(current_physical_health=MATCH.current_physical_health,
                      chronic_conditions=MATCH.chronic_conditions,
                      recent_surgeries_or_injuries=MATCH.recent_surgeries_or_injuries,
                      medications=MATCH.medications)))
    def young_adult_fitness(self,current_physical_health,chronic_conditions,recent_surgeries_or_injuries,medications):
        self.recommandation.append("For young adults (18-29 years):")
        self.recommandation.append("Training Plan: A mix of cardiovascular and strength training exercises.")
        self.recommandation.append("Diet Plan: A balanced diet with a good mix of protein, carbohydrates, and healthy fats.")
        if chronic_conditions or recent_surgeries_or_injuries or medications or current_physical_health != 'good':
            self.recommandation.append("Special considerations may be needed for young adults with specific health conditions or recent surgeries/injuries.")
            if chronic_conditions:
                self.recommandation.append("Chronic conditions:", ",".join(chronic_conditions))
            if recent_surgeries_or_injuries:
                self.recommandation.append("Recent surgeries or injuries:", ",".join(recent_surgeries_or_injuries))
            if medications:
                self.recommandation.append("Medications:", ",".join(medications))

    
    #Middle-aged Adults (Ages 31-50)
    @Rule(AND(PersonalInfo(age=P(lambda age: 30<= age < 50)),
          HealthState(current_physical_health=MATCH.current_physical_health,
                      chronic_conditions=MATCH.chronic_conditions,
                      recent_surgeries_or_injuries=MATCH.recent_surgeries_or_injuries,
                      medications=MATCH.medications)))
    def middle_aged_adult_fitness(self,current_physical_health,chronic_conditions,recent_surgeries_or_injuries,medications):
        self.recommandation.append("For middle-aged adults (30-49 years):")
        self.recommandation.append("Training Plan: Include moderate-intensity exercises like brisk walking, cycling.")
        self.recommandation.append("Diet Plan: Heart-healthy foods, limit saturated fats, and maintain a balanced diet.")
        if chronic_conditions or recent_surgeries_or_injuries or medications or current_physical_health != 'good':
            self.recommandation.append("Special considerations may be needed for middle-aged adults with specific health conditions or recent surgeries/injuries.")
            if chronic_conditions:
                self.recommandation.append(("Chronic conditions:", ",".join(chronic_conditions)))
            if recent_surgeries_or_injuries:
                self.recommandation.append(("Recent surgeries or injuries:", ",".join(recent_surgeries_or_injuries)))
            if medications:
                self.recommandation.append(("Medications:", ",".join(medications)))

    #Seniors (Ages 50+)
    @Rule(AND(PersonalInfo(age=P(lambda age: age >= 50)),
              HealthState(current_physical_health=MATCH.current_physical_health,
                      chronic_conditions=MATCH.chronic_conditions,
                      recent_surgeries_or_injuries=MATCH.recent_surgeries_or_injuries,
                      medications=MATCH.medications)))
    def senior_health_considerations(self,current_physical_health,chronic_conditions,recent_surgeries_or_injuries,medications):
        self.recommandation.append("For seniors (50+ years):")
        self.recommandation.append("Training Plan: Focus on low-impact exercises like walking and swimming.")
        self.recommandation.append("Diet Plan: Ensure sufficient calcium intake and maintain a balanced diet.")
        if chronic_conditions or recent_surgeries_or_injuries or medications or current_physical_health != 'good':
            self.recommandation.append("Special considerations may be needed for seniors with specific health conditions or recent surgeries/injuries.")
            if chronic_conditions:
                self.recommandation.append("Chronic conditions:", ",".join(chronic_conditions))
            if recent_surgeries_or_injuries:
                self.recommandation.append("Recent surgeries or injuries:", ",".join(recent_surgeries_or_injuries))
            if medications:
                self.recommandation.append("Medications:", ",".join(medications))


    #rules taking in cosideration the lifestyle and dietary preferences

    @Rule(AND(Lifestyle(activity_level=W('activity_level'), 
                       stress_level=W('stress_level')),
              DietaryPreferences(diet_type=W('diet_type'),allergies=MATCH.allergies, intolerances=MATCH.intolerances)))
    def combined_recommendation(self, activity_level, exercise_freq, stress_level, diet_type):
        # Determine the training plan
        if activity_level == 'sedentary':
            training_plan = 'Start with light exercises like walking or yoga.'
        elif activity_level == 'moderately active':
            training_plan = 'Incorporate regular moderate exercise like jogging or swimming.'
        else:  # very active
            training_plan = 'Continue your active routine, consider adding strength training.'

        # Adjust training plan based on stress level
        if stress_level == 'high':
            training_plan += ' Include stress-reducing activities like yoga or meditation.'

        # Determine the diet plan
        if diet_type == 'vegan':
            diet_plan = 'Ensure adequate protein from plant sources. Focus on whole grains, legumes, and nuts.'
        elif diet_type == 'vegetarian':
            diet_plan = 'Include a variety of vegetables, fruits, whole grains, and dairy.'
        else:  # omnivore or others
            diet_plan = 'Balance your diet with a mix of lean meats, vegetables, grains, and fruits.'

        # Print the combined plan
        self.recommandation.append("Training Plan: "+training_plan)
        self.recommandation.append("Diet Plan: "+diet_plan)
      

    # Rule to adjust diet plan for food intolerances
    @Rule(DietaryPreferences(intolerances=W('intolerances'),allergies=W('allergies')))
    def adjust_for_intolerances(self, intolerances,allergies):
        if intolerances:
            intolerance_advice = 'Adjust your diet to avoid: ' + ', '.join(intolerances) + '.'
            self.recommandation.append("Intolerance Adjustment: "+intolerance_advice)
        else:
            self.recommandation.append("Intolerance Adjustment: No food intolerance reported.")
        if allergies:
            allergies_advice = 'Adjust your diet to avoid: ' + ', '.join(allergies) + '.'
            self.recommandation.append("allergies Adjustment: "+allergies_advice)
        else:
            self.recommandation.append("allergies Adjustment: No food allergies reported.")


    # rules taking into consideration smoking
    @Rule(AND(Lifestyle(smoking=True),
              FitnessGoals(weight_management='lose weight')))
    def smoker_looking_to_lose_weight(self):
        self.recommandation.append("As a smoker looking to lose weight:")
        self.recommandation.append("Training Plan: Start with moderate cardio activities to improve lung capacity.")
        self.recommandation.append("Diet Plan: Focus on calorie control and nutrient-rich foods.")


    @Rule(AND(Lifestyle(smoking=True),
              FitnessGoals(weight_management='gain weight')))
    def smoker_looking_to_gain_weight(self):
        self.recommandation.append("As a smoker looking to gain weight:")
        self.recommandation.append("Training Plan: Incorporate strength training to build muscle mass.")
        self.recommandation.append("Diet Plan: Increase calorie intake with nutrient-dense foods, focusing on proteins and healthy fats.")


    @Rule(AND(Lifestyle(smoking=True),
              FitnessGoals(weight_management='maintain weight')))
    def smoker_looking_to_maintain_weight(self):
        self.recommandation.append("As a smoker looking to maintain weight:")
        self.recommandation.append("Training Plan: Combine cardio and strength training for a balanced approach.")
        self.recommandation.append("Diet Plan: Maintain a balanced diet with appropriate portion sizes to sustain your current weight.")

    
    #rules for sleeping hours
    @Rule(PersonalInfo(sleep_hours=P(lambda hours: hours < 6)))
    def strength_training_with_poor_sleep(self):
        self.recommandation.append("Training Plan: Avoid overtraining. Ensure adequate rest and recovery.")
        self.recommandation.append("Diet Plan: Include foods that promote sleep, like cherries, milk, and almonds.")


def expert_system_init():
    engine = FitnessExpertSystem()
    engine.reset()  
    return engine

class UserAttributes:
    def __init__(self, engine, height, weight, age, gender, occupation, sleep_hours, stress_level, chronic_conditions,
                 recent_surgeries_or_injuries, medications, current_physical_health, allergies, intolerances,
                 weight_management, endurance_goal, flexibility_goal, strength_goal, smoking, activity_level,
                 diet_type):

        self.engine = engine
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.sleep_hours = sleep_hours
        self.stress_level = stress_level
        self.chronic_conditions = chronic_conditions
        self.recent_surgeries_or_injuries = recent_surgeries_or_injuries
        self.medications = medications
        self.current_physical_health = current_physical_health
        self.allergies = allergies
        self.intolerances = intolerances
        self.weight_management = weight_management
        self.endurance_goal = endurance_goal
        self.flexibility_goal = flexibility_goal
        self.strength_goal = strength_goal
        self.smoking = smoking
        self.activity_level = activity_level
        self.diet_type = diet_type


def expert_systeme_output(userAttributes):
    bmi = calculate_bmi(userAttributes.height, userAttributes.weight)
    bodyfat= calculate_body_fat(userAttributes.height, userAttributes.weight, userAttributes.age, userAttributes.gender)
    engine.recommandation.append("Person physique: height : "+str(userAttributes.height)+ " weight :"+str(userAttributes.weight)+" gender: "+str(userAttributes.gender))
    
    #declaring variables
    engine = userAttributes.engine
    height = userAttributes.height
    weight = userAttributes.weight
    age = userAttributes.age
    gender = userAttributes.gender
    occupation = userAttributes.occupation
    sleep_hours = userAttributes.sleep_hours
    stress_level = userAttributes.stress_level
    chronic_conditions = userAttributes.chronic_conditions
    recent_surgeries_or_injuries = userAttributes.recent_surgeries_or_injuries
    medications = userAttributes.medications
    current_physical_health = userAttributes.current_physical_health
    allergies = userAttributes.allergies
    intolerances = userAttributes.intolerances
    weight_management = userAttributes.weight_management
    endurance_goal = userAttributes.endurance_goal
    flexibility_goal = userAttributes.flexibility_goal
    strength_goal = userAttributes.strength_goal
    smoking = userAttributes.smoking
    activity_level = userAttributes.activity_level
    diet_type = userAttributes.diet_type

    #Declaring personalinfo
    engine.declare(PersonalInfo(age=age, gender=gender, occupation=occupation, 
                                    sleep_hours=sleep_hours, stress_level=stress_level, 
                                    ))
    # Declaring phyiscal attributes
    engine.declare(PhysicalAttributes(height=height, weight=weight,bmi=bmi,body_fat_percentage=bodyfat))
    # Declaring a HealthState 
    engine.declare(HealthState(current_physical_health=current_physical_health,chronic_conditions=chronic_conditions,
    recent_surgeries_or_injuries=recent_surgeries_or_injuries,medications=medications))  
    #Declaring fitness goal
    engine.declare(FitnessGoals(weight_management=weight_management,endurance_goal=endurance_goal,flexibility_goal=flexibility_goal,strength_goal=strength_goal))
    #declaring lifestyle
    engine.declare(Lifestyle(activity_level=activity_level,smoking=smoking))
    #declaring dietary preferences
    engine.declare(DietaryPreferences(diet_type=diet_type,allergies=allergies,intolerances=intolerances))
    engine.run()
    return engine.recommandation
    
    
def bard_output(recommandation):    
    file_path = 'query.txt'  
    with open(file_path, 'r') as file:
        query_header = file.read()
    Bard_query=""
    for i in range(len(recommandation)):
        Bard_query+=str(recommandation[i])+"\n"
    token="xxxxxxxxxxxxx"
    try:
        bard = Bard(token=token)
    except Exception as e:
        print(e)
        return "Error: Token expired"
    input_text=query_header+"\n"+Bard_query
    # Send an API request and get a response.
    try:
        response = bardapi.core.Bard(token).get_answer(input_text)
    except Exception as e:
        print(e)
        return "Error: Token expired"
    # Print the response.
    return response["content"]

@app.route('/api', methods=['POST'])
def api():
    height = float(request.json['height'])  # in meters
    weight = float(request.json['weight'])    # in kilograms
    age = int(request.json['age'])
    gender = request.json['gender']
    occupation=request.json['occupation']
    sleep_hours=request.json['sleep_hours']
    stress_level=request.json['stress_level']
    chronic_conditions=request.json['chronic_conditions']
    recent_surgeries_or_injuries=request.json['recent_surgeries_or_injuries']
    medications=request.json['medications']
    current_physical_health=request.json['current_physical_health']
    allergies=request.json['allergies']
    intolerances=request.json['intolerances']
    weight_management=request.json['weight_management']
    endurance_goal=request.json['endurance_goal']
    flexibility_goal=request.json['flexibility_goal']
    strength_goal=request.json['strength_goal']
    smoking=request.json['smoking']
    diet_type=request.json['diet_type']
    activity_level=request.json['activity_level']

    engine=expert_system_init()
    expert_systeme_output=(engine,height,weight,age,gender,occupation,sleep_hours,stress_level,chronic_conditions,recent_surgeries_or_injuries,medications,current_physical_health,allergies,intolerances,weight_management,endurance_goal,flexibility_goal,strength_goal,smoking)

    return {"response":bard_output(expert_systeme_output)}
 


if __name__ == "__main__":
    app.run(debug=True)
