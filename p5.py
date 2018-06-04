import re
import datetime
import pymysql
db = pymysql.connect("localhost","root","ranom","bankdb")
cursor=db.cursor()
now=datetime.datetime.now()
y=str(now.year)
m=str(now.month)
d=str(now.day)
date=y+"-"+m+"-"+d
class customer:
    
    def __init__(self):
        self.val=1
        while self.val :
        
            print('\n1. Sign Up')
            print('2. Sign In')
            print('3. Admin Sign In')
            print('4. Quit\n')
            
            choice = int(input('Enter your choice: '))
            
            if choice==1:
                self.signup()
                
            elif choice==2:
                self.sign_in()
                
            elif choice==3:
                self.admin_signin()
                
            elif choice==4:
                self.quit_()
            
    
    def gen_account_no(self):
        ac_type=""
        ac_ty=int(input('Choose your account type: \n 1. Savings\n 2. Current\n'))
        f=0
        if ac_ty==1:
            ac_type="Savings"
            deposit=int(input('Do you want to make some initial deposit:\n1. YES\n2. NO\n'))
            if deposit==1:
                dep_fund=input('Enter deposit amount : ')
                while not(dep_fund.isdigit()):
                    dep_fund=input("Enter valid amount : ")
                f=1
                balance=str(dep_fund)
        
            else:
                balance=0 
        if ac_ty==2 :
            ac_type="Current"
            print('You need to deposit a minimum of Rs.5000 to open a current account')
            dep_fund=input('Enter deposit amount : ')
            while (not(dep_fund.isdigit()) or int(dep_fund)<5000):
                dep_fund=input("Enter valid amount greater than 5000 : ")
            f=2
            balance=str(dep_fund)

         
        if(ac_type == "Savings"):
            cursor.execute("Select count(*) from customer where ac_type='Savings'")
            data=cursor.fetchone()
            s=str(data[0])
            num=int(s)
            num=num+1
            s=str(num)
            while(len(s)<4):
                s = "0"+s
            ac_no = "250012"+s
            print("Your Account Number(Customer ID) is ",ac_no)

        if(ac_type == "Current"):
            cursor.execute("Select count(*) from customer where ac_type='Current'")
            data=cursor.fetchone()
            s=str(data[0])
            num=int(s)
            num=num+1
            s=str(num)
            while(len(s)<4):
                s = "0"+s
            ac_no = "250011"+s
            
        return ac_type, ac_no, balance, f
    
    
    def is_leap_year(self,y):
        if y%4==0 and y%100==0 and y%400==0:
            return 1
        else:
            return 0
            
    def check_pwd(self,pwd):
        if len(pwd)>=8:
            if re.search('\W', pwd):
                return 0
            return 1
        return 0
    
    def signup(self):
        
        #print('\nInside Sign Up\n')
        
        f_name=input('Enter your first name: ')
        l_name=input('Enter your last name: ')
        aadhar=input('Enter your aadhar no: ')
        while(len(aadhar)!=12 or not aadhar.isdigit()) :
            aadhar=input('Enter your correct aadhar no: ')
        cursor.execute("Select aadhar from customer");
        data=cursor.fetchall();
        #a line added here
        aadhar_list=[adhr for adhr in tup for tup in data]
        
# =============================================================================
#         i=0
#         while(i<len(data)):
#             a2=data[i][0]
#             i=i+1
#             if aadhar == a2 :
#                 print("Aadhar is already in use")
#                 aadhar=input('Enter your aadhar no: ')
#             while(len(aadhar)!=12 or not aadhar.isdigit()) :
#                 aadhar=input('Enter your correct aadhar no: ')
#                 i=0
# =============================================================================
        
        while True:
            aadhar=input('enter your aadhar number(must be 12 digits only): ')
            if aadhar not in aadhar_list and len(aadhar)==12:
                if aadhar.isdigit():
                    break
                else:
                    print('invalid aadhar! ')
                    continue
        
        addr=input('Enter your address: ')
        city=input('Enter city: ')
        state=input('Enter your state: ')
        pin=input('Enter your pin: ')
        
        while(len(pin)!=6 or not pin.isdigit()) :
            pin=input('Enter your correct pin code: ')

        pwd_verify=0
        pwd=input('Choose your password(must contain characters and numbers only): ')
        pwd_verify=self.check_pwd(pwd)
        while pwd_verify!=1:
             pwd=input('Password must be of atleast 8 characters and should contain a number and a alphabet : ')
             pwd_verify=self.check_pwd(pwd)

        
        
        ac_type,ac_no,balance,f=self.gen_account_no()
        print("Your Account Number(Customer ID) is ",ac_no)
            
        status="unlocked"
        cursor.execute("insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(f_name,l_name,aadhar,addr,city,state,pin,ac_no,pwd,status,ac_type))
        if(f==1):
            cursor.execute("insert into savings values(%s,%s,%s,%s,%s)",(ac_no,date,"Deposit",balance,balance))
            cursor.execute("insert into ac_balance values(%s,%s)",(ac_no,balance))
        if(f==2):
            cursor.execute("insert into current values(%s,%s,%s,%s,%s)",(ac_no,date,"Deposit",balance,balance))
            cursor.execute("insert into ac_balance values(%s,%s)",(ac_no,balance))
        if(f==0):
            cursor.execute("insert into ac_balance values(%s,%s)",(ac_no,balance))
        db.commit();
        #send to the database
        #generate customer_id and display it to the userprint('exiting signup')
   
    
    def sign_in(self):
        print('\nInside Sign In:\n ')
        while 1:
            ac_no=input('Enter your Customer ID(Account Number) : ')
            while(len(ac_no)!=10 or not ac_no.isdigit()) :
                print("Customer ID is a 10 digit numeric value") 
                ac_no=input('Enter your Customer ID(Account Number) : ')
            cursor.execute("Select ac_no,status,pwd from customer where ac_no=(%s)",ac_no);
            data=cursor.fetchone()
            if(data==None):
                print("Customer ID(Account Number) does not exist")
            else :
                break

        
        
        trial_no=0
        max_trial=3
        self.logout=0
        while trial_no<3:
            pwd=input('Enter your password: ')
            pas = data[2]    
            if(pas == pwd and data[1] == "unlocked"):
                self.login=1
                print("Sign in Successful\n")
                break
            elif(pas !=pwd):
                trial_no+=1
                print("Incorrect Password ",(max_trial-trial_no)," attempts left")
            elif(data[1]=="locked"):
                print("You can't Sign In, your account has been locked")
                self.login=0
                break
            elif(data[1]=="closed"):
                print("You can't Sign In, your account has been closed")
                self.login=0
                break
            #check for the existence of the account
            
        if trial_no==3:
            self.login=0
            cursor.execute("update customer set status='locked' where ac_no = (%s)",ac_no)
            print('\nYOUR ACCOUNT HAS BEEN LOCKED\n')
            
        db.commit();
        #submenu after sign-in
        if self.login==1:
            ch=1
            while ch:
                print('\n1. Address Change ')
                print('2. Open New Account ')
                print('3. Money Deposit ')
                print('4. Money Withdrawal ')
                print('5. Transfer Money ')
                print('6. Print Statement ')
                print('7. Account Closure ')
                print('8. Avail Loan')
                print('0. Customer Logout ')
                
                option=int(input('Enter your choice: '))
                
                if option==1:
                    print('\nEnter details about your new address\n')
                    new_addr1=input('Address Line 1 : ')
                    new_addr2=input('Address Line 2 : ')
                    new_addr=new_addr1+new_addr2;
                    new_city=input('City : ')
                    new_state=input('State : ')
                    new_pin=input('Pincode : ')
                    while(len(new_pin)!=6 or not new_pin.isdigit()) :
                        new_pin=input('Enter Correct Pincode: ')
                    cursor.execute("update customer set addr=(%s),city=(%s),state=(%s),pincode=(%s) where ac_no=(%s)",(new_addr,new_city,new_state,new_pin,ac_no))
                    print("Address Updated Successfully\n")
                    db.commit()
                    #write sql query and update to the db
                    

                elif option==2:
                    while 1:
                        print("\n1. Open Saving Account")
                        print("2. Open Current Account")
                        print("3. Open Fixed Deposit")
                        op = int(input("Enter yout choice : "))

                        if op==1:
                            cursor.execute("Select ac_type from customer where ac_no = %s",ac_no)
                            d = cursor.fetchone()
                            if(d[0]=="Savings"):
                                print("You already have a Savings Account, choose other options")
                                break
                            cursor.execute("Select aadhar from customer where ac_no=%s",ac_no)
                            d=cursor.fetchone()
                            cursor.execute("select count(*) from customer where aadhar=%s",d[0])
                            c = cursor.fetchone()
                            if(c[0]==2):
                                print("You already have one Savings Account and one Current Account")
                            else :
                                f=0
                                cursor.execute("Select * from customer where ac_no = %s",ac_no)
                                d = cursor.fetchone()
                                ac_type="Savings"
                                deposit=int(input('Do you want to make some initial deposit:\n1. YES\n2. NO\n'))
                                if deposit==1:
                                    dep_fund=input('Enter deposit amount : ')
                                    while (len(amount)>9 or not dep_fund.isdigit()):
                                        dep_fund=input("Enter valid amount : ")
                                    f=1
                                    balance=str(dep_fund)
                                else:
                                    balance = 0

                                if(ac_type == "Savings"):
                                    cursor.execute("Select count(*) from customer where ac_type='Savings'")
                                    data=cursor.fetchone()
                                    s=str(data[0])
                                    num=int(s)
                                    num=num+1
                                    s=str(num)
                                    while(len(s)<4):
                                        s = "0"+s
                                        ac_no2 = "250012"+s
                                    print("Your Savings Account Number(Customer ID) is ",ac_no2)
                                cursor.execute("insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(d[0],d[1],d[2],d[3],d[4],d[5],d[6],ac_no2,d[8],d[9],ac_type))
                                if(f==1):
                                    cursor.execute("insert into savings values(%s,%s,%s,%s,%s)",(ac_no2,date,"Deposit",balance,balance))
                                    cursor.execute("insert into ac_balance values(%s,%s)",(ac_no2,balance))
                                if(f==0):
                                    cursor.execute("insert into ac_balance values(%s,%s)",(ac_no2,balance))
                                    
                                db.commit();
                                break;     
                        elif op==2:
                            cursor.execute("Select ac_type from customer where ac_no = %s",ac_no)
                            d = cursor.fetchone()
                            if(d[0]=="Current"):
                                print("You already have a Current Account, choose other options")
                                break
                            cursor.execute("Select aadhar from customer where ac_no=%s",ac_no)
                            d=cursor.fetchone()
                            cursor.execute("select count(*) from customer where aadhar=%s",d[0])
                            c = cursor.fetchone()
                            if(c[0]==2):
                                print("You already have one Savings Account and one Current Account")
                            else :
                                f=0
                                cursor.execute("Select * from customer where ac_no = %s",ac_no)
                                d = cursor.fetchone()
                                ac_type="Current"
                                print('You need to deposit a minimum of Rs.5000 to open a current account')
                                dep_fund=input('Enter deposit amount : ')
                                while (not(dep_fund.isdigit()) or int(dep_fund)<5000):
                                    dep_fund=input("Enter valid amount greater than 5000 : ")
                                f=2
                                balance=str(dep_fund)
                                

                                if(ac_type == "Current"):
                                    cursor.execute("Select count(*) from customer where ac_type='Current'")
                                    data=cursor.fetchone()
                                    s=str(data[0])
                                    num=int(s)
                                    num=num+1
                                    s=str(num)
                                    while(len(s)<4):
                                        s = "0"+s
                                        ac_no2 = "250011"+s
                                    print("Your Current Account Number(Customer ID) is ",ac_no2)
                                cursor.execute("insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(d[0],d[1],d[2],d[3],d[4],d[5],d[6],ac_no2,d[8],d[9],ac_type))
                                if(f==2):
                                    cursor.execute("insert into current values(%s,%s,%s,%s,%s)",(ac_no2,date,"Deposit",balance,balance))
                                    cursor.execute("insert into ac_balance values(%s,%s)",(ac_no2,balance))
                                if(f==0):
                                    cursor.execute("insert into ac_balance values(%s,%s)",(ac_no2,balance))
                                    
                                db.commit();
                                break;
                        elif op==3:
                            fd_amount = input("Enter Fixed Deposit Amount : ")
                            while(len(fd_amount)>9 or int(fd_amount)<1000 or int(fd_amount)%1000 != 0 or not fd_amount.isdigit()):
                                print("FD Amount should be minimum Rs.1000 and in multiples of 1000")
                                fd_amount = input("Enter Valid FD Amount : ")
                            fd_term = input("Enter Fixed Deposit Term in Months : ")
                            while(len(fd_term)>3 or int(fd_term)<12 or not fd_term.isdigit()):
                                print("FD Term should be minimum of 12 months")
                                fd_term = input("Enter Valid FD Term : ")
                            cursor.execute("Select count(*) from fd_ac where ac_no=%s",ac_no)
                            num = cursor.fetchone()
                            s = str(num[0]+1)
                            fd_ac=""
                            while(len(s)<3):
                                s = "0"+s
                                fd_ac = "FD"+s
                            fd_ac = fd_ac + ac_no
                            print("Your FD Account Number is : ",fd_ac)
                            print("FD Amount is Rs.",fd_amount," and term is ",fd_term," months")
                            cursor.execute("insert into fd_ac values(%s,%s,%s,%s,%s)",(ac_no,fd_ac,date,fd_amount,fd_term))
                            db.commit()
                            break

                                
                elif option==3:
                    amount=input('Enter the amount you want to deposit : ')
                    while(len(amount)>9 or not amount.isdigit()) :
                        amount=input('Enter valid amount : ')
                    
                    cursor.execute("select ac_type from customer where ac_no = %s",ac_no)
                    data=cursor.fetchone()
                    if(data[0]=="Savings"):
                        cursor.execute("select count(*) from savings where year(date) = (%s) and month(date)=(%s) and ac_no=(%s)",(y,m,ac_no))
                        count=cursor.fetchone()
                        if(count[0]<10):
                            cursor.execute("select balance from ac_balance where ac_no = %s",ac_no)
                            data2=cursor.fetchone() 
                            balance=int(data2[0])
                            balance=str(balance + int(amount))
                            cursor.execute("insert into savings values(%s,%s,%s,%s,%s)",(ac_no,date,"Deposit",amount,balance))
                            cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance,ac_no))
                        else :
                            print("You already did 10 transactions this month")
                           
                    if(data[0]=="Current"):
                        cursor.execute("select balance from ac_balance where ac_no = %s",ac_no)
                        data2=cursor.fetchone() 
                        balance=int(data2[0])
                        balance=str(balance + int(amount))
                        cursor.execute("insert into current values(%s,%s,%s,%s,%s)",(ac_no,date,"Deposit",amount,balance))
                        cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance,ac_no))

                    db.commit()
                    #write sql query and update to the db
                
                elif option==4:
                    amount=input('Enter the amount you want to withdrawal: ')
                    while(len(amount)>9 or not amount.isdigit()) :
                        amount=input('Enter valid amount : ')
                        
                    cursor.execute("select ac_type from customer where ac_no = %s",ac_no)
                    data=cursor.fetchone()
                    if(data[0]=="Savings"):
                        cursor.execute("select count(*) from savings where year(date) = (%s) and month(date)=(%s) and ac_no=(%s)",(y,m,ac_no))
                        count=cursor.fetchone()
                        if(count[0]<10):
                            cursor.execute("select balance from ac_balance where ac_no = %s",ac_no)
                            data2=cursor.fetchone() 
                            balance=int(data2[0])
                            if(balance>=int(amount)):
                                balance=str(balance - int(amount))
                                cursor.execute("insert into savings values(%s,%s,%s,%s,%s)",(ac_no,date,"Withdrawal",amount,balance))
                                cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance,ac_no))
                            else :
                                print("Your account balance is less than ",amount," so, we cannot process the transaction")
                        else :
                            print("You already did 10 transactions this month")
                           
                    if(data[0]=="Current"):
                        cursor.execute("select balance from ac_balance where ac_no = %s",ac_no)
                        data2=cursor.fetchone() 
                        balance=int(data2[0])
                        if(balance-int(amount)>=5000):
                            balance=str(balance - int(amount))
                            cursor.execute("insert into current values(%s,%s,%s,%s,%s)",(ac_no,date,"Withdrawal",amount,balance))
                            cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance,ac_no))
                        else :
                            print("Your account must always have a minimum balance of Rs.5000")
                            print("Processing this transaction will result in invalidating this constraint")

                        
                    db.commit()
                
                elif option==6:
                    while 1 :
                        print("1. Print full bank statement")
                        print("2. Print bank statement within a range")
                        op=int(input("Enter choice : "))
                        if op==1 :                        
                            cursor.execute("select ac_type from customer where ac_no = %s",ac_no)
                            data=cursor.fetchone()
                            print("The Bank Statement for ",ac_no," : ")
                            if(data[0]=="Savings"):
                                cursor.execute("select date,trans_type,amount,balance from savings where ac_no=%s order by date",ac_no)
                                print("Date\t\tTransaction\t\t\tAmount\tBalance")
                                data1=cursor.fetchall()
                                i=0
                                while(i<len(data1)):
                                    if(data1[i][1].startswith("Transfer")):
                                       print(data1[i][0],"\t",data1[i][1],"\t",data1[i][2],"\t",data1[i][3])
                                    else :
                                       print(data1[i][0],"\t",data1[i][1],"\t\t\t",data1[i][2],"\t",data1[i][3])
                                    i=i+1
                                    
                            if(data[0]=="Current"):
                                cursor.execute("select date,trans_type,amount,balance from current where ac_no=%s order by date",ac_no)
                                print("Date\t\tTransaction\t\t\tAmount\tBalance")
                                data1=cursor.fetchall()
                                i=0
                                while(i<len(data1)):
                                    
                                    if(data1[i][1].startswith("Transfer")):
                                       print(data1[i][0],"\t",data1[i][1],"\t",data1[i][2],"\t",data1[i][3])
                                    else :
                                       print(data1[i][0],"\t",data1[i][1],"\t\t\t",data1[i][2],"\t",data1[i][3])
                                    i=i+1
                            break

                        elif op == 2:
                            d1 = input("Enter start date in YYYY-MM-DD format : ")
                            d2 = input("Enter end date in YYYY-MM-DD format : ")
                            date1 = d1.split("-")
                            date2= d2.split("-")
                            if(int(date1[0])<2017 or int(date1[0])>2018):
                                print("Start date out of bound")
                                break
                            if(int(date1[1])<1 or int(date1[1])>12):
                                print("Invalid Date")
                                break
                            if(int(date1[2])<0):
                                print("Invalid date")
                            if(int(date1[1])==1 or int(date1[1])==3 or int(date1[1])==5 or int(date1[1])==7 or int(date1[1])==8 or int(date1[1])==10 or int(date1[1])==12):
                                if(int(date1[2])>31):
                                    print("Invalid date")
                                    break
                            if(int(date1[1])==4 or int(date1[1])==6 or int(date1[1])==9 or int(date1[1])==11):
                                if(int(date1[2])>30):
                                    print("Invalid date")
                                    break
                            if(self.is_leap_year(int(date1[0])) and int(date1[1])==2):
                                if(int(date1[2])>29):
                                    print("Invalid date")
                                    break
                            if(not self.is_leap_year(int(date1[0])) and int(date1[1])==2):
                                if(int(date1[2])>28):
                                    print("Invalid date")
                                    break
                                   
                            if(int(date2[0])<2017 or int(date2[0])>2018):
                                print("End date out of bound")
                                break
                            if(int(date2[1])<1 or int(date2[1])>12):
                                print("Invalid date")
                                break
                            if(int(date2[2])<0):
                                print("Invalid date")
                            if(int(date2[1])==1 or int(date2[1])==3 or int(date2[1])==5 or int(date2[1])==7 or int(date2[1])==8 or int(date2[1])==10 or int(date2[1])==12):
                                if(int(date2[2])>31):
                                    print("Invalid date")
                                    break
                            if(int(date2[1])==4 or int(date2[1])==6 or int(date2[1])==9 or int(date2[1])==11):
                                if(int(date2[2])>30):
                                    print("Invalid date")
                                    break
                            if(self.is_leap_year(int(date2[0])) and int(date2[1])==2):
                                if(int(date2[2])>29):
                                    print("Invalid date")
                                    break
                            if(not self.is_leap_year(int(date2[0])) and int(date2[1])==2):
                                if(int(date2[2])>28):
                                    print("Invalid date")
                                    break

                            if(date1[0]>date2[0]):
                                print("End date should be after Start date")
                                break
                            if(date1[0]==date2[0]):
                                if(date1[1]>date2[1]):
                                    print("End date should be after Start date")
                                    break
                                else:
                                    if(date1[2]>date2[2]):
                                        print("End date should be after Start date")
                                        break    
                            cursor.execute("select ac_type from customer where ac_no = %s",ac_no)
                            data=cursor.fetchone()
                            print("The Bank Statement for ",ac_no," : ")
                            if(data[0]=="Savings"):
                                cursor.execute("select date,trans_type,amount,balance from savings where ac_no=(%s) and date between (%s) and (%s)",(ac_no,d1,d2))
                                print("Date\t\tTransaction\t\t\tAmount\tBalance")
                                data1=cursor.fetchall()
                                i=0
                                while(i<len(data1)):
                                    if(data1[i][1].startswith("Transfer")):
                                       print(data1[i][0],"\t",data1[i][1],"\t",data1[i][2],"\t",data1[i][3])
                                    else :
                                       print(data1[i][0],"\t",data1[i][1],"\t\t\t",data1[i][2],"\t",data1[i][3])
                                    i=i+1
                                    
                            if(data[0]=="Current"):
                                print("OK")
                                cursor.execute("select date,trans_type,amount,balance from current where ac_no=%s and date between %s and %s",(ac_no,d1,d2))
                                print("Date\t\tTransaction\t\t\tAmount\tBalance")
                                data1=cursor.fetchall()
                                i=0
                                while(i<len(data1)):
                                    
                                    if(data1[i][1].startswith("Transfer")):
                                       print(data1[i][0],"\t",data1[i][1],"\t",data1[i][2],"\t",data1[i][3])
                                    else :
                                       print(data1[i][0],"\t",data1[i][1],"\t\t\t",data1[i][2],"\t",data1[i][3])
                                    i=i+1
                            break
                    #write sql query to print the statement of the account
                    
                
                elif option==5:
                    r_ac_no=input("Enter the recipient's account number : ")                      
                    while(r_ac_no==ac_no or (len(r_ac_no)!=10 or not r_ac_no.isdigit())):
                        if(r_ac_no==ac_no):
                            print("Customer's A/C no and Recipient's A/C no should not be same")
                        else :
                            print("Customer's A/C no is a 10 digit numeric value")
                        r_ac_no=input("Enter the recipient's account number CORRECTLY : ")
                    while 1 :
                        cursor.execute("Select count(*) from customer where ac_no=%s",r_ac_no)
                        d = cursor.fetchone()
                        cursor.execute("Select status from customer where ac_no=%s",r_ac_no)
                        st=cursor.fetchone()
                        if(st[0]=="locked" and d[0]==1):
                            print("Recipient's Account is locked")
                        elif(st[0]=="closed" and d[0]==1):
                            print("Recipient's Account is closed")
                        else:
                            break
                    trans="Transfer to "+r_ac_no
                    trans2="Transfer from "+ac_no
                    amount=input('Enter the amount to be transferred : ')
                               #ranojit chutiya
                    while(len(amount)>9 or not amount.isdigit()) :
                        amount=input('Enter valid amount : ')
                    cursor.execute("select ac_type from customer where ac_no = %s",ac_no)
                    data=cursor.fetchone()
                    if(data[0]=="Savings"):
                        cursor.execute("select count(*) from savings where year(date) = (%s) and month(date)=(%s) and ac_no=(%s)",(y,m,ac_no))
                        count=cursor.fetchone()
                        if(count[0]<10):
                            cursor.execute("select balance from ac_balance where ac_no = %s",ac_no)
                            data2=cursor.fetchone() 
                            balance=int(data2[0])
                            if(balance>=int(amount)):
                                balance=str(balance - int(amount)) 
                                cursor.execute("select count(*) from customer where ac_no=%s",r_ac_no)
                                fl=cursor.fetchone()
                                if(fl[0]==1):
                                    cursor.execute("select ac_type from customer where ac_no = %s",r_ac_no)
                                    d=cursor.fetchone()
                                    if(d[0]=="Savings"):
                                        cursor.execute("select count(*) from savings where year(date) = (%s) and month(date)=(%s) and ac_no=(%s)",(y,m,r_ac_no))
                                        count2=cursor.fetchone()
                                        if(count2[0]<10):
                                            cursor.execute("select balance from ac_balance where ac_no = %s",r_ac_no)
                                            d2=cursor.fetchone() 
                                            balance2=int(d2[0])
                                            balance2=str(balance2 + int(amount))
                                            cursor.execute("insert into savings values(%s,%s,%s,%s,%s)",(r_ac_no,date,trans2,amount,balance2))
                                            cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance2,r_ac_no))
                                            cursor.execute("insert into savings values(%s,%s,%s,%s,%s)",(ac_no,date,trans,amount,balance))
                                            cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance,ac_no))
                                        else :
                                            print("A/C no ",r_ac_no," already did 10 transactions this month, so you cannot transfer money to that account")
                           
                                    if(d[0]=="Current"):
                                        cursor.execute("select balance from ac_balance where ac_no = %s",r_ac_no)
                                        d2=cursor.fetchone() 
                                        balance2=int(d2[0])
                                        balance2=str(balance2 + int(amount))
                                        cursor.execute("insert into current values(%s,%s,%s,%s,%s)",(r_ac_no,date,trans2,amount,balance2))
                                        cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance2,r_ac_no))
                                        cursor.execute("insert into savings values(%s,%s,%s,%s,%s)",(ac_no,date,trans,amount,balance))
                                        cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance,ac_no))

                                
                            else :
                                print("Your account balance is less than ",amount," so, we cannot process the transaction")
                        else :
                            print("You already did 10 transactions this month")

                    if(data[0]=="Current"):
                        cursor.execute("select balance from ac_balance where ac_no = %s",ac_no)
                        data2=cursor.fetchone() 
                        balance=int(data2[0])
                        if(balance-int(amount)>=5000):
                            balance=str(balance - int(amount))
                            cursor.execute("select count(*) from customer where ac_no=%s",r_ac_no)
                            fl=cursor.fetchone()
                            if(fl[0]==1):
                                cursor.execute("select ac_type from customer where ac_no = %s",r_ac_no)
                                d=cursor.fetchone()
                                if(d[0]=="Savings"):
                                    cursor.execute("select count(*) from savings where year(date) = (%s) and month(date)=(%s) and ac_no=(%s)",(y,m,r_ac_no))
                                    count2=cursor.fetchone()
                                    if(count2[0]<10):
                                        cursor.execute("select balance from ac_balance where ac_no = %s",r_ac_no)
                                        d2=cursor.fetchone() 
                                        balance2=int(d2[0])
                                        balance2=str(balance2 + int(amount))
                                        cursor.execute("insert into savings values(%s,%s,%s,%s,%s)",(r_ac_no,date,trans2,amount,balance2))
                                        cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance2,r_ac_no))
                                        cursor.execute("insert into current values(%s,%s,%s,%s,%s)",(ac_no,date,trans,amount,balance))
                                        cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance,ac_no))
                                    else :
                                        print("A/C no ",r_ac_no," already did 10 transactions this month, so you cannot transfer money to that account")
                           
                                if(d[0]=="Current"):
                                    cursor.execute("select balance from ac_balance where ac_no = %s",r_ac_no)
                                    d2=cursor.fetchone() 
                                    balance2=int(d2[0])
                                    balance2=str(balance2 + int(amount))
                                    cursor.execute("insert into current values(%s,%s,%s,%s,%s)",(r_ac_no,date,trans2,amount,balance2))
                                    cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance2,r_ac_no))
                                    cursor.execute("insert into current values(%s,%s,%s,%s,%s)",(ac_no,date,trans,amount,balance))
                                    cursor.execute("update ac_balance set balance=%s where ac_no=%s",(balance,ac_no))

                            
                        else :
                            print("Your account must always have a minimum balance of Rs.5000")
                            print("Processing this transaction will result in invalidating this constraint")

                    db.commit()
                    
                elif option==7:
                    closure=int(input('press 1 to close your account, 0 to go back to previous menu : '))
                    if closure==1:
                        cursor.execute("update customer set status=%s where ac_no = %s",("closed",ac_no))
                        print("Your Account has been closed")
                        print("You are being logged out")
                        db.commit()
                        break

                elif option==8:
                    cursor.execute("Select ac_type from customer where ac_no =%s",ac_no)
                    data=cursor.fetchone()
                    if(data[0]=="Current"):
                        print("You cannot avail a Loan")
                        print("To avail a loan, you must have a savings account and you need to sign in from that account")
                    else:
                        cursor.execute("select balance from ac_balance where ac_no=%s",ac_no)
                        amt=cursor.fetchone()
                        l_amount=input("Enter Loan Amount : ")
                        while(len(l_amount)>9 or not l_amount.isdigit() or int(l_amount)>2*int(amt[0]) or int(l_amount)%1000!=0 or int(l_amount)<1000) :
                            print("Loan amount must not be more than twice your savings account balance and should be in multiples of 1000")
                            l_amount=input('Enter valid loan amount : ')
                        loan_term = input("Enter Loan Repayment Term in Months : ")
                        while(len(loan_term)>3 or int(loan_term)<12 or not loan_term.isdigit()):
                            print("Loan Term should be minimum of 12 months")
                            loan_term = input("Enter Valid Loan Repayment Term : ")
                        cursor.execute("Select count(*) from loan_ac where ac_no=%s",ac_no)
                        num = cursor.fetchone()
                        s = str(num[0]+1)
                        loan_no=""
                        while(len(s)<3):
                            s = "0"+s
                        loan_no = "LN"+s
                        loan_no = loan_no + ac_no
                        print("Your Loan Account Number is : ",loan_no)
                        print("Loan Amount is Rs.",l_amount," and term is ",loan_term," months")
                        cursor.execute("insert into loan_ac values(%s,%s,%s,%s,%s)",(ac_no,loan_no,date,l_amount,loan_term))
                        db.commit()
                        
                        
                elif option==0:
                    self.login=0
                    self.logout=1
                    break
                
                else:
                    print('invalid option')
                    ch=1
            
    def admin_signin(self):
        f=1
        while f :
            alogin=0
            admin_id=input('Enter Admin ID : ')
            cursor.execute("Select id from admin")
            data=cursor.fetchall()
            i=0
            while(i<len(data)):
                if(admin_id != data[i][0]):
                    admin_id=input("Enter valid Admin ID : ")
                else:
                    f=0
                    break
        pwd=input('Enter Admin Password : ')
        cursor.execute("Select pwd from admin where id=(%s)",admin_id)
        data=cursor.fetchone()
        i=0
        while(data[0]!=pwd and i<3):
            i=i+1
            pwd=input("Enter correct Password : ")
        if i==3:
            print("Admin Sign In Failed\n")
        else :
            print("Admin Sign In Successful\n")
            alogin=1
            pas=data[0]
        
        while alogin :
            print('\n1. View Closed Account ')
            print('2. View Locked Account ')
            print('3. View Unlocked Account ')
            print('4. Change Account Status ')
            print('5. Change Admin Password')
            print('6. FD Report of a Customer')
            print('7. FD Report of a Customer vis-a-vis another Customer')
            print('8. FD Report w.r.t a particular FD amount')
            print('9. Loan Report of a Customer')
            print('10. Loan Report of a Customer vis-a-vis another Customer')
            print('11. Loan Report w.r.t a particular Loan amount')
            print('12. Loan-FD Report of Customers')
            print('13. Report of Customers who are yet to avail a loan')
            print('14. Report of Customers who are yet to open an FD account')
            print('15. Report of Customers who neither have a loan nor a FD account with the bank')
            
            print('16. Admin Logout ')
                
            option=int(input('Enter your choice: '))

            if option == 1:
                cursor.execute("select count(*) from customer where status='closed'")
                ct=cursor.fetchone()
                cursor.execute("Select fname,lname,ac_type,ac_no,status from customer where status='closed'")
                data=cursor.fetchall()
                i=0
                if ct[0]==0 :
                    print("No Closed Accounts")
                else:
                    print("First name,Last name,A/C type,A/C No,Status")
                    while(i<len(data)):
                        print(data[i][0],", ",data[i][1],", ",data[i][2],", ",data[i][3],", ",data[i][4])
                        i=i+1
                    
            elif option == 2:
                cursor.execute("select count(*) from customer where status='locked'")
                ct=cursor.fetchone()
                cursor.execute("Select fname,lname,ac_type,ac_no,status from customer where status='locked'")
                data=cursor.fetchall()
                i=0
                if ct[0]==0 :
                    print("No Locked Accounts")
                else:
                    print("First name,Last name,A/C type,A/C No,Status")
                    while(i<len(data)):
                        print(data[i][0],", ",data[i][1],", ",data[i][2],", ",data[i][3],", ",data[i][4])
                        i=i+1
                    
            elif option == 3 :
                cursor.execute("select count(*) from customer where status='unlocked'")
                ct=cursor.fetchone()
                cursor.execute("Select fname,lname,ac_type,ac_no,status from customer where status='unlocked'")
                data=cursor.fetchall()
                i=0
                if ct[0]==0 :
                    print("No Unlocked Accounts")
                else:
                    print("First name,Last name,A/C type,A/C No,Status")
                    while(i<len(data)):
                        print(data[i][0],", ",data[i][1],", ",data[i][2],", ",data[i][3],", ",data[i][4])
                        i=i+1
                        
            elif option == 4 :
                while 1 :
                    ac=input("Enter ID of customer whose account status is to be changed : ")
                    while(len(ac)!=10 or not ac.isdigit()) :
                        print("Customer ID is a 10 digit numeric value") 
                        ac=input('Enter valid Customer ID : ')
                    cursor.execute("Select status from customer where ac_no=(%s)",ac);
                    data=cursor.fetchone()
                    if(data==None):
                        print("Entered Customer ID does not exist")
                    else :
                        print("Status of ",ac," : ",data[0])
                        if(data[0]=="locked"):
                            print("Enter 'u' to UNLOCK the Account")
                            print("Enter 'c' to CLOSE the Account")
                            print("Enter 'n' to CANCEL operation")
                            c = input("Enter choice : ")
                            if(c=='u'):
                                cursor.execute("update customer set status='unlocked' where ac_no = %s",ac)
                                print("Account Status Changed")
                                break
                            elif(c=='c'):
                                cursor.execute("update customer set status='closed' where ac_no = %s",ac)
                                print("Account Status Changed")
                                break
                            elif(c=='n'):
                                break
                            else:
                                print("Invalid Input")

                        elif(data[0]=="unlocked"):
                            print("Enter 'l' to LOCK the Account")
                            print("Enter 'c' to CLOSE the Account")
                            print("Enter 'n' to CANCEL operation")
                            c = input("Enter choice : ")
                            if(c=='l'):
                                cursor.execute("update customer set status='locked' where ac_no = %s",ac)
                                print("Account Status Changed")
                                break
                            elif(c=='c'):
                                cursor.execute("update customer set status='closed' where ac_no = %s",ac)
                                print("Account Status Changed")
                                break
                            elif(c=='n'):
                                break
                            else:
                                print("Invalid Input")

                        
                        elif(data[0]=="closed"):
                            print("Enter 'l' to LOCK the Account")
                            print("Enter 'u' to UNLOCK the Account")
                            print("Enter 'n' to CANCEL operation")
                            c = input("Enter choice : ")
                            if(c=='l'):
                                cursor.execute("update customer set status='locked' where ac_no = %s",ac)
                                print("Account Status Changed")
                                break
                            elif(c=='u'):
                                cursor.execute("update customer set status='unlocked' where ac_no = %s",ac)
                                print("Account Status Changed")
                                break
                            elif(c=='n'):
                                break
                            else:
                                print("Invalid Input")

                    db.commit()
                    
            elif option == 5 :
                p = input("Enter Current Admin Password : ")
                while(p!=pas):
                    print("Incorrect Password Input")
                    p = input("Enter CORRECT Current Admin Password : ")
                p2 = input("Enter new Admin Password : ")
                p3 = ""
                while(p2==p):
                    print("New Password Cannot be the same as the Old Password")
                    p2=input("Enter new Admin Password : ")
                p3 = input("Confirm new Admin Password : ")
                while(p3!=p2):
                    print("Please enter correctly")
                    p3 = input("Confirm new Admin Password : ")
                cursor.execute("update admin set pwd = %s where id=%s",(p2,admin_id))
                print("Password Changed")
                db.commit()

            elif option == 6:
                ac = input("Enter Customer's A/C number : ")
                while(len(ac)!=10 or not ac.isdigit()) :
                    print("Customer ID is a 10 digit numeric value") 
                    ac=input('Enter valid Customer ID : ')
                cursor.execute("Select count(*) from fd_ac where ac_no=%s",ac)
                d=cursor.fetchone()
                if(d[0]==0):
                    print("Customer ID ",ac," doesn't have any FD account")
                else :
                    cursor.execute("Select fd_no,amount,term from fd_ac where ac_no = %s",ac)
                    print("FD A/C no\t\tAmount\tTerm")
                    data=cursor.fetchall()
                    i=0
                    while(i<len(data)):
                        print(data[i][0],"\t",data[i][1],"\t",data[i][2])
                        i=i+1

            elif option == 7:
                fl=0
                ac = input("Enter Customer's A/C number : ")
                while(len(ac)!=10 or not ac.isdigit()) :
                    print("Customer ID is a 10 digit numeric value") 
                    ac=input('Enter valid Customer ID : ')
                cursor.execute("Select count(*) from fd_ac where ac_no=%s",ac)
                d=cursor.fetchone()
                if(d[0]==0):
                    print("Customer ID ",ac," doesn't have any FD account")
                else :
                    cursor.execute("Select sum(amount) from fd_ac where ac_no = %s",ac)
                    data2=cursor.fetchone()
                    cursor.execute("Select * from fd_ac where ac_no != %s and amount >= %s",(ac,data2[0]))
                    data=cursor.fetchall()
                    i=0
                    print("Customer ID\tFD A/C no\t\tAmount\tTerm")
                    i=0
                    while(i<len(data)):
                        fl=1
                        print(data[i][0],"\t",data[i][1],"\t",data[i][3],"\t",data[i][4])
                        i=i+1
                    if(fl==0):
                        print("NO DATA\n")
                        
            elif option == 8 :
                fl=0
                amt = input("Enter an amount : ")
                while(len(amt)>9 or int(amt)<1000 or int(amt)%1000 !=0):
                    print("Amount must be minimum Rs.1000 and should be in multiples of 1000")
                    amt = input("Enter valid amount : ")
                cursor.execute("Select distinct ac_no,fd_no,amount from fd_ac where amount>%s",int(amt))
                d=cursor.fetchall()
                print("Customer ID\tFD A/C no\t\tFirst Name\tLast Name\tAmount")
                i=0
                while(i<len(d)):
                    fl=1
                    cursor.execute("Select fname,lname from customer where ac_no=%s",d[i][0])
                    data=cursor.fetchall()
                    j=0
                    while(j<len(data)):
                        print(d[i][0],"\t",d[i][1],"\t",data[j][0],"\t",data[j][1],"\t\t",d[i][2])
                        j=j+1
                    i=i+1
                if(fl==0):
                    print("NO DATA\n")

            elif option == 9:
                ac = input("Enter Customer's A/C number : ")
                while(len(ac)!=10 or not ac.isdigit()) :
                    print("Customer ID is a 10 digit numeric value") 
                    ac=input('Enter valid Customer ID : ')
                cursor.execute("Select count(*) from loan_ac where ac_no=%s",ac)
                d=cursor.fetchone()
                if(d[0]==0):
                    print("Customer ID ",ac," doesn't have any Loan account")
                else :
                    cursor.execute("Select loan_no,amount,term from loan_ac where ac_no = %s",ac)
                    print("Loan A/C no\t\tAmount\tTerm")
                    data=cursor.fetchall()
                    i=0
                    while(i<len(data)):
                        print(data[i][0],"\t",data[i][1],"\t",data[i][2])
                        i=i+1

            elif option == 10:
                fl=0
                ac = input("Enter Customer's A/C number : ")
                while(len(ac)!=10 or not ac.isdigit()) :
                    print("Customer ID is a 10 digit numeric value") 
                    ac=input('Enter valid Customer ID : ')
                cursor.execute("Select count(*) from loan_ac where ac_no=%s",ac)
                d=cursor.fetchone()
                if(d[0]==0):
                    print("Customer ID ",ac," doesn't have any Loan account")
                else :
                    cursor.execute("Select sum(amount) from loan_ac where ac_no = %s",ac)
                    data2=cursor.fetchone()
                    cursor.execute("Select * from loan_ac where ac_no != %s and amount >= %s",(ac,data2[0]))
                    data=cursor.fetchall()
                    i=0
                    print("Customer ID\tLoan A/C no\t\tAmount\tTerm")
                    i=0
                    while(i<len(data)):
                        fl=1
                        print(data[i][0],"\t",data[i][1],"\t",data[i][3],"\t",data[i][4])
                        i=i+1
                    if(fl==0):
                        print("NO DATA\n")

            elif option == 11:
                fl=0
                amt = input("Enter an amount : ")
                while(len(amt)>9 or int(amt)<1000 or int(amt)%1000 !=0):
                    print("Amount must be minimum Rs.1000 and should be in multiples of 1000")
                    amt = input("Enter valid amount : ")
                cursor.execute("Select distinct ac_no,loan_no,amount from loan_ac where amount>%s",int(amt))
                d=cursor.fetchall()
                print("Customer ID\tLoan A/C no\t\tFirst Name\tLast Name\tAmount")
                i=0
                while(i<len(d)):
                    fl=1
                    cursor.execute("Select fname,lname from customer where ac_no=%s",d[i][0])
                    data=cursor.fetchall()
                    j=0
                    while(j<len(data)):
                        print(d[i][0],"\t",d[i][1],"\t",data[j][0],"\t",data[j][1],"\t\t",d[i][2])
                        j=j+1
                    i=i+1
                if(fl==0):
                    print("NO DATA\n")

            elif option ==12:
                fl=0
                cursor.execute("Select ac_no,sum(amount) from fd_ac group by ac_no")
                data=cursor.fetchall()
                cursor.execute("Select ac_no,sum(amount) from loan_ac group by ac_no")
                data2=cursor.fetchall()
                i=0
                print("Customer ID\tFirst Name\tLast Name\tSum of Loan Amount\tSum of FD Amount")
                while(i<len(data)):
                    j=0
                    while(j<len(data2)):
                        if(data2[j][0]==data[i][0]):
                            if(data2[j][1]>data[i][1]):
                                fl=1
                                cursor.execute("Select fname,lname from customer where ac_no = %s",data[i][0])
                                data3=cursor.fetchone()
                                print(data[i][0],"\t",data3[0],"\t",data3[1],"\t\t",data2[j][1],"\t\t",data[i][1])
                        j=j+1
                    i=i+1
                            
                    
                if(fl==0):
                    print("NO DATA\n")

            elif option ==13:
                fl=0
                cursor.execute("Select ac_no from customer where ac_type='Savings'")
                data=cursor.fetchall()
                i=0
                print("Customer ID\tFirst Name\tLast Name")
                while(i<len(data)):
                    cursor.execute("Select count(*) from loan_ac where ac_no=%s",data[i][0])
                    c=cursor.fetchone()
                    if(c[0]==0):
                        fl=1
                        cursor.execute("Select fname, lname from customer where ac_no=%s",data[i][0])
                        data2=cursor.fetchone()
                        print(data[i][0],"\t",data2[0],"\t",data2[1])
                    i=i+1
                if(fl==0):
                    print("NO DATA\n")

            elif option ==14:
                fl=0
                cursor.execute("Select ac_no from customer")
                data=cursor.fetchall()
                i=0
                print("Customer ID\tFirst Name\tLast Name")
                while(i<len(data)):
                    cursor.execute("Select count(*) from fd_ac where ac_no=%s",data[i][0])
                    c=cursor.fetchone()
                    if(c[0]==0):
                        fl=1
                        cursor.execute("Select fname, lname from customer where ac_no=%s",data[i][0])
                        data2=cursor.fetchone()
                        print(data[i][0],"\t",data2[0],"\t",data2[1])
                    i=i+1
                if(fl==0):
                    print("NO DATA\n")
                        
            elif option ==15:
                fl=0
                cursor.execute("Select ac_no from customer")
                data=cursor.fetchall()
                i=0
                print("Customer ID\tFirst Name\tLast Name")
                while(i<len(data)):
                    cursor.execute("Select count(*) from loan_ac where ac_no=%s",data[i][0])
                    c=cursor.fetchone()
                    if(c[0]==0):
                        cursor.execute("Select count(*) from fd_ac where ac_no=%s",data[i][0])
                        c2=cursor.fetchone()
                        if(c2[0]==0):
                            fl=1
                            cursor.execute("Select fname, lname from customer where ac_no=%s",data[i][0])
                            data2=cursor.fetchone()
                            print(data[i][0],"\t",data2[0],"\t",data2[1])
                    i=i+1
                if(fl==0):
                    print("NO DATA\n")
                    
            elif option == 16 :
                alogin=0
                
                    
        #verify from the database
        
    
    def quit_(self):
        self.val=0
        db.close()
        
if __name__ == "__main__" :    
    c=customer()
    
