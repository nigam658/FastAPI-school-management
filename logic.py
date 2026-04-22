

def calculate_percentage (marks):
    percentage_ = (sum(marks) / (len(marks) * 100)) * 100
                  

    return percentage_


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    
    elif percentage >= 75 and percentage < 90:
        return "A"
    
    elif percentage >= 60 and percentage < 75:
        return "B"
    
    elif percentage >= 45 and percentage < 60:
        return "C"
    
    else:
        return "FAIL"
    
def my_classes():
    my_classe = ["class_8th","class_9th","class_10th"]
    return my_classe

    