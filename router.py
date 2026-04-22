from fastapi import APIRouter, HTTPException, Depends,status
from database import get_mysql
from model import Student, student_mark,responsepercentage,SignupreqModel,SignupResponse, LoginreqModel, LoginResponse, CreateTeacherReqModel,CreateTeacherRespModel,markUpdateResponseModel
from logic import calculate_percentage, calculate_grade, my_classes
from autho import create_access_token, get_current_user
from security import hass_password, verify_password
import mysql.connector


router = APIRouter()

@router.post("/signup", response_model = SignupResponse)
def signup(signup : SignupreqModel):

    role = "student"   # giving to all role as student so bydefult everyone see only only data as a student 
    hassed_pass = hass_password(signup.password)   # convert pain password to hasses password

    conn = get_mysql() 
    cursor = conn.cursor()

    cursor.execute("select * from user_pass where username = %s",(signup.username, ))   
    user = cursor.fetchone()
    if user :
       raise HTTPException(status_code=400, detail="username already exist")  # first check if user exist block code , error handeling


    # error handeling second time 
    try:
        query = "insert into user_pass (username, password, role) values (%s,%s,%s)"
        cursor.execute(query,(signup.username,hassed_pass,role))
        conn.commit()

    except mysql.connector.Error as err:  
        if "Duplicate entry" in str(err):
            raise HTTPException(400, "username already exist")
        else:
            raise HTTPException(500, 'database error')
    
    finally:
        cursor.close()
        conn.close()

    return {"message" : "signup done "}


@router.post("/login", response_model= LoginResponse)
def login (user : LoginreqModel ):

    conn = get_mysql()
    cursor = conn.cursor()

    try:
        cursor.execute("select username, password, role from user_pass where username = %s",(user.username,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(401, "invalid username or password")

                
        stored_pass = result[1]
        role = result[2]

        if not verify_password(user.password,stored_pass):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "invalid username or password")
        
        
        token = create_access_token({"sub":user.username, "role" : role})

        return {
            "access_token" : token,
            "token_type" : "bearer",
            "role" : role
        }
        
    finally:
        cursor.close()
        conn.close()
    

@router.put("/create_teacher")
def create_teacher(crteacher : CreateTeacherReqModel, user : dict = Depends(get_current_user)):

    if user["role"] != "admin" :
        raise HTTPException(status_code=403, detail="only admin can update teacher")

    conn =get_mysql()
    cursor = conn.cursor()
    try :
        cursor.execute("update user_pass set role = 'teacher' where username = %s",(crteacher.teacher_name,))
        conn.commit()

        if cursor.rowcount == 0 :
            raise HTTPException(status_code=404, detail="user not found")
        
        return {
            "message" : "user promoted to teacher",
            "username" : crteacher.teacher_name
        }
  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

    finally:
        cursor.close()
        conn.close()


# joining student 
@router.post("/join/{Classs}",)  
def joining(student:Student, Classs : str ):
    
    my_class = my_classes()   # for prevent error,no one can write anything , importe logic file
    
    if Classs not in my_class  :
        raise HTTPException(status_code=400, detail="class not found!")  # use status code to define which type of error
    

    conn = get_mysql()
    cursor = conn.cursor()

    try:
        query = f"insert into {Classs} (student_name, student_rollno) values (%s, %s)"   # database is already created with unique roll no 

        cursor.execute(query,(student.name,student.rollno))
        conn.commit()
        return {
            "message" : "student added successfully",
            "data" : student
            }
    
    except :
        return {
            "message" : "error",
            "details": "database error"
        }

    finally:
        cursor.close()
        conn.close()
    

# store marks
@router.put("/{rollno}/{classs}",response_model=markUpdateResponseModel)
def mark_submit (rollno:int ,classs:str, Students_mark : student_mark, user : dict = Depends(get_current_user)): # assign student_subject
    
    my_class = my_classes() # for prevent error,no one can write anything , importe logic file

    if classs not in my_class:
        return {"message":"class is not found!"}
    
    if user["role"] not in  ["admin","teacher"] :   #check who is user 
        raise HTTPException(status_code=403, detail="you cannot submit marks") 
 
    conn = get_mysql()
    cursor = conn.cursor()

    try:
        query = f"update {classs} set Physics=%s, Chemistry=%s, Math=%s, English=%s, Biology=%s, IT=%s where student_rollno =%s"

        cursor.execute(query,(
            Students_mark.physics,
            Students_mark.chemistry, 
            Students_mark.math,
            Students_mark.english,
            Students_mark.biology,
            Students_mark.IT,
            rollno
            ))
        conn.commit()

        if cursor.rowcount == 0:
            return {"message" : "student not found "}
        
        return {"message" : "mark saved"}
    

    except Exception as e :
        return{
            "message" : "error!",
            "details": str(e)
        }

    finally:
        cursor.close()
        conn.close()


#return percentage  
@router.get ("/percentage/{classs}/{rollno}", response_model = responsepercentage)
def precentage(classs:str,rollno:int):

    my_class = my_classes()  # for prevent error,no one can write anything , importe logic file

    if classs not in my_class:
        return {"massage" : "class is not found!"}

    conn = get_mysql()
    cursor =conn.cursor()

    try:
        cursor.execute(f"select student_name,Physics, Chemistry, Math, English, Biology, IT from {classs} where student_rollno = {rollno} ")     # Ececute query
        
        result = cursor.fetchone()                            #store add data
        name = result[0] 
        marks = result[1:]

        if result is None:                                    # checking data is stored or not 
            return{"massage":"student not found"}
        
        else:
            percentage_ = round(calculate_percentage(marks),2)        # calling calculate_pecnetage fucntion
            grade = calculate_grade(percentage_)                   # calling calculate_grade fucntion
            
            # return data
            return{
                "name" : name,
                "percentage":percentage_,
                "grade":grade
                   
                }

    finally:    #close sql operation
        cursor.close()
        conn.close()

# student topper as per subject 
@router.get("/subjecttopper/{classs}/{subject}")
def sub_toper(classs:str, subject : str):
    
    my_class = my_classes()
    if classs not in my_class:
        return {"massage" : "class is not found!"}

    conn = get_mysql()
    cursor =conn.cursor()
    
    try:
        cursor.execute(f"select student_name from {classs} order by {subject} desc limit 3")
        top_3 = cursor.fetchall()

        return{"data": top_3}
    
    finally:
        cursor.close()
        conn.close()

@router.delete("/{classes}/{rollno}")
def del_user_id (classes : str, rollno : int, user : dict = Depends(get_current_user) ):

    my_class = my_classes()  # for prevent error,no one can write anything , importe logic file

    if classes not in my_class:
        return {"massage" : "class is not found!"}
    
    if user["role"] != "admin" :
        raise HTTPException(status_code=403,detail="you cannot delete data")

    conn = get_mysql()
    cursor =conn.cursor()
    
    try:

        query = f"delete from {classes} where student_rollno = %s"
        cursor.execute(query,(rollno,))
        conn.commit()

        return {"message" : "student delete"}

    finally:
        cursor.close()
        conn.close()





    

   
