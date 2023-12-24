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