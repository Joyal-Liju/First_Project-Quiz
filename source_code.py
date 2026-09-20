import secrets
import string
import uuid
import mysql.connector as cont
con=cont.connect(host='localhost',user='root',password='joyboy')
cursor=con.cursor()

if con.is_connected():
    print('WELCOME TO QUIZ MAKER')

def quiz():
    run=True
    while run:
        global cursor
        print('1.Make or Review Quiz')
        print('2.Attempt Quiz')
        print('3.Exit')
        
        try:
            Quiz=int(input('enter your choice(1/2/3):'))
            if Quiz==1:
                print(‘-------------------------------------------------’)
                print("Instructions on Creating a Quiz")
                print('1. One can only create only one quiz from the same username')
                print('2. Even if you add questions after logging in second time, the questions will be added to the old quiz')
                print('3. The pass given at the creation of your account acts as the Quiz ID for the attempters')
                print(‘-------------------------------------------------’)
                menu()
            elif Quiz==2:
                print(‘-------------------------------------------------’)
                quiz_id=input('enter your quiz id')
                attempt_quiz(cursor, quiz_id)
            elif Quiz==3:
                print('=========Thank you for using=========')
                run=False
                break
            else:
                print('invalid choice')
                print(‘================================================’)
        except ValueError:
            print('invalid choice')
            print(‘===================================================’)
        else:
            break

def menu():
    while True:
        try:
            global cursor
            passw=''
            print('enter 1 if you are new')
            print('enter 2 if you are already created')
            log=int(input('enter your choice(1/2):'))
            if log ==1:
                print(‘-------------------------------------------------’)
                def name_check(cursor):
                   while True:  
                        name = input('Enter your username: ')
                        cursor.execute('use log')  
                        cursor.execute('select * from info')
                        n = cursor.fetchall()
                        
                        exists = False  
                        for i in n:
                            if i[1].upper() == name.upper():
                                print('Username already exists. Please try another username.')
                                exists = True
                                break  
                        if not exists:  
                            return name
                        
                name=name_check(cursor)
                
                sign_up(name)
                passw = generate_password()
                print('Username: ',name)
                print("YOUR password:", passw)
                cursor.execute('use LOG')
                cursor.execute("""insert into info(name,pass)
                            values('{}','{}')""".format(name,passw))
                print('now you can login using your username and ID')
                go=input('do you want to login and create quiz(y/n):')
                print(‘-------------------------------------------------’)
                con.commit()
                if go=='y' or go=='Y':
                    print(‘---------------------------------------------’)
                    login(cursor)
                if go!='y' and go!='Y':
                    quiz()
            elif log==2:
                print(‘-------------------------------------------------’)
                login(cursor)
            else:
                print('invalid choice')
                print(‘-------------------------------------------------’)

        except ValueError:
            print('invalid choice.. please input a valid choice')
            print(‘---------------------------------------------------’)

        else:
            break
    

def login(cursor):
    cursor.execute('use LOG')
    
    try_a='y'
    while try_a=='y' or try_a=='Y':
        user=input('enter your username:')
        user_id=input('enter your pass:')
        cursor.execute("select * from info where name='{}'".format(user,))
        detail=cursor.fetchone()
        
        if user==detail[1] and user_id==detail[2]:
            query=f"USE {user}"
            cursor.execute(query)
            print(‘----------------------------------------------------’)                                        
            print("1. Create quiz")
            print("2. View score")
            choice=int(input('enter your choice(1/2):'))
            if choice==1:
                print(‘-------------------------------------------------’)
                create_quiz_table(cursor)
                input_questions()
                break
            elif choice==2:
                view_score(user)
                break
                    
        else:
            print('invalid username or password')
            try_a=input('do you want to try again(y/n):')




def create_quiz_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
    Qno INT AUTO_INCREMENT,
    questions VARCHAR(255) NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_option VARCHAR(1) NOT NULL,
    PRIMARY KEY(Qno))
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS POINTS(
    no INT AUTO_INCREMENT,
    Name VARCHAR(30),
    Score INT,
    PRIMARY KEY(no))""")
    con.commit()

def input_questions():
    print('ADD YOUR QUESTIONS')
    while True:
        ques=input('enter question:')
        a=input('enter option a:')
        b=input('enter option b:')
        c=input('enter option c:')
        d=input('enter option d:')
        correct=input('enter the correct option(a/b/c/d):')
        insert_question(ques,a,b,c,d,correct)
        add=input('do you want to add more(y/n):')
        if add!='y' and add!='Y':
            print('Share your pass code as Quiz ID for attempting quiz')
            print(‘----------------------------------------------------’)
            quiz()
            break

                
def insert_question(question, option_a, option_b, option_c, option_d, correct_option):
    global cursor
    cursor.execute("""
    INSERT INTO quiz_questions (questions, option_a, option_b, option_c, option_d, correct_option)
    VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
    """.format(question, option_a, option_b, option_c, option_d, correct_option))
    con.commit()

def log_save():
    global cursor
    cursor.execute('create database IF NOT EXISTS LOG')
    cursor.execute("USE LOG")
    cursor.execute("""CREATE TABLE IF NOT EXISTS info (
                   Slno INT AUTO_INCREMENT,
                   name VARCHAR(35),
                   pass VARCHAR(6),
                   PRIMARY KEY(Slno)
                   )""")
    con.commit()

def generate_password(length=6):
    alphabet = string.ascii_uppercase + string.digits + string.ascii_lowercase
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def sign_up(name):
    global cursor
    q="create database IF NOT EXISTS {}".format(name,)
    cursor.execute(q)
    con.commit()
    return name

def attempt_quiz(cursor, quiz_id):
    cursor.execute('use LOG')
    cursor.execute('select name,pass from info where pass="{}"'.format(quiz_id))
    det=cursor.fetchone()
    if det==None:
        print('Quiz Not Found')
        print('Try Again')
        print(‘====================================================’)
        quiz()
    else:
        user=det[0]
        query=f"USE {user}"
        cursor.execute(query)
        cursor.execute("SELECT * FROM quiz_questions")
        quiz_data = cursor.fetchall()

        if not quiz_data:
            print("Quiz not found.")
        else:
            taker=input('enter your name:')
            score=0
            for question in quiz_data:
                print("Question:", question[1])
                print("Options:")
                print("a. ", question[2])
                print("b. ", question[3])
                print("c. ", question[4])
                print("d. ", question[5])
                user_answer = input("Your answer (a/b/c/d): ").lower()
                if user_answer == question[6]:
                    print("Correct!\n")
                    score+=1
                else:
                    print("Incorrect.The correct answer is",question[6], "\n")
                
            cursor.execute("""INSERT INTO POINTS(Name,Score)
                    values('{}',{})""".format(taker,score))
            con.commit()
            quiz()


def view_score(user):
    global cursor
    query=f"USE {user}"
    cursor.execute(query)
    print(‘------------------------------------------------------’)
    cursor.execute('select * from POINTS')
    num=cursor.fetchall()
    for i in num:
        print('name:',i[1],'Score:',i[2],end='\n')
    quiz()

log_save()   
quiz()
con.commit()

con.close()
