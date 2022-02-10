import pickle
import os

def get_acc_no():
    count=0
    try:
        f_obj=open("acccounts.dat","rb")
        while True:
            count+=1
            data=pickle.load(f_obj)
            del(data)
    except EOFError:
        f_obj.close()
    except FileNotFoundError:
        count+=1
    finally:
        return count

def check_bdate(date):
    valid=False
    if(date==""):
        print("Empty Date")
    else:
        date=date.split("-")
        for i in range(0,len(date)):
            date[i]=int(date[i])
        if(date[2]<=2019 and date[2]>=1925):
            if(date[1]<=12 and date[1]>=1):
                if(date[0]<=31 and date[0]>0):
                    if(date[1] in [1,3,5,7,8,10,12]):
                        valid=True
                        return valid#same like assert, will not go to elif statement
                    elif(date[1] in [4,6,9,11] and date[0]<31):
                        valid=True
                        return valid
                    elif(date[1]==2):
                        if(date[2]%4==0 and date[0]<30):
                            valid=True
                            return valid
                        elif(date[2]%4!=0 and date[0]<29):
                            valid=True
                            return valid
                        else:
                            print("Invalid Date")
                    else:
                        print("Invalid Date")
                else:
                    print("Invalid Date")
            else:
                print("Invalid Month")
        else:
            print("Invalid Year!")
    return valid

def search_acc(acc_to_search):
    try:
        found=False
        f_obj=open("acccounts.dat","rb")
        while True:
            data=pickle.load(f_obj)
            if(data.acc_no==acc_to_search):
                found=True
                print("Account Found")
                print("Account Number:",data.acc_no)
                print("Account Holder Name:",data.name)
                input()
                f_obj.close()
                break
    except EOFError:
        f_obj.close()
    except FileNotFoundError:
        print("Bank Database is Empty!")
    finally:
        return found

class bank:
    bank_code="528"
    def __init__(self):
        self.name=""
        self.age=0
        self.balance=0
        self.gender="a"
        self.city=""
        self.bdate=""
        self.acc_type=""
        self.acc_no=""

    def addAccount(self):
        self.name=input("Enter Full Name:")
        while(self.age <18 or self.age>100):
            self.age=int(input("Input Valid Age(18-100):"))
        while(self.gender not in "mMfFoO"):
            self.gender=input("Enter Your Gender(m-f-o):")
        while(not check_bdate(self.bdate)):
            self.bdate=input("Enter your Birthdate(dd-mm-yy):")
        self.city=input("Enter your Resident City:")
        while(self.balance<5000):
            self.balance=float(input("Enter Opening Balance(5000 min)"))
        while(self.acc_type not in "SsCc"):
            self.acc_type=input("Enter Account Type(S/C):")

    def displayDetails(self):
        x="%-7s %-15s %-10s %-12s %-15s %-6s %-4s" %(self.acc_no, self.name, self.balance, self.bdate, self.city, self.gender, self.age)
        print(x)

    def update(self, update_type):
        if(update_type in "Dd"):
            update_ammount=int(input("Enter the Ammount to Deposit:"))
        elif(update_type in "Ww"):
            update_ammount=int(input("Enter the Ammount to Withdraw:"))
            update_ammount*=-1
        self.balance+=update_ammount
        if(self.balance<1000):
                print("Sorry Account must have min balance of 1000")
                self.balance-=update_ammount

choice=1
while (choice>0 and choice<8):
    os.system("cls")
    print("1.Add Account")
    print("2.List")
    print("3.Search")
    print("4.Remove")
    print("5.Deposite")
    print("6.Widthdraw")
    print("7.Transfer")
    print("8.Exit")
    choice=int(input("Enter Choice->"))

    if(choice==1):
        account=bank()
        account.addAccount()
        account.acc_no=bank.bank_code+str(get_acc_no())
        f_obj=open("acccounts.dat","ab+")
        pickle.dump(account,f_obj)
        f_obj.close()
        del(account)
    elif(choice==2):
        try:
            f_obj=open("acccounts.dat","rb")
            z="%-7s %-15s %-10s %-12s %-15s %-6s %-4s" %("Acc No.", "Name", "Balance", "Birth Date", "City", "Gender", "Age")
            print("-"*len(z))
            print(z)
            print("-"*len(z))
            while True:
                obj_data=pickle.load(f_obj)
                obj_data.displayDetails()
        except FileNotFoundError:
            print("Bank Records Does not Exist Yet")
        except EOFError:
            print("-"*len(z))
            f_obj.close()
        finally:
            input()
    elif(choice==3):
        acc_to_search=input("Enter Account to Search:")
        if(not search_acc(acc_to_search)):
            print("Sorry No Such Account")
        input()
    elif(choice==4):
        acc_to_delete=input("Enter the Account to Delete:")
        if(not search_acc(acc_to_delete)):
            print("No Such Account in our Database")
        else:
            try:
                f_obj=open("acccounts.dat","rb")
                ftemp_obj=open("temp.dat","wb")
                while True:
                    data=pickle.load(f_obj)
                    if(data.acc_no!=acc_to_delete):
                        pickle.dump(data, ftemp_obj)
            except EOFError:
                f_obj.close()
                ftemp_obj.close()
            finally:
                os.remove("acccounts.dat")
                os.rename("temp.dat","acccounts.dat")

    elif(choice==5 or choice==6):
        temp_acc_no=input("Enter the Account Number:")
        if(search_acc(temp_acc_no)):
            try:
                f_obj=open("acccounts.dat","rb")
                ftemp_obj=open("temp.dat","wb")
                while True:
                    data=pickle.load(f_obj)
                    if(data.acc_no==temp_acc_no):
                        if(choice==5):
                            data.update("D")
                        else:
                            data.update("W")
                    pickle.dump(data, ftemp_obj)
            except EOFError:
                f_obj.close()
                ftemp_obj.close()
            finally:
                os.remove("acccounts.dat")
                os.rename("temp.dat","acccounts.dat")
        else:
            print("No Such Account in our Database!")
        input()
        
print("Thank you for using Serivce")
os.system("cls")
input()