from llm_call import *
from expert_system import *

from flask import *
from flask_cors import CORS

#flask init
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)


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
    userAttributes=UserAttributes(engine,height,weight,age,gender,occupation,sleep_hours,stress_level,chronic_conditions,recent_surgeries_or_injuries,medications,current_physical_health,allergies,intolerances,weight_management,endurance_goal,flexibility_goal,strength_goal,smoking,diet_type,activity_level)
    print(expert_systeme_output(engine,userAttributes))
    return {"response":bard_output(expert_systeme_output(engine,userAttributes))}
 


if __name__ == "__main__":
    app.run(debug=True)
