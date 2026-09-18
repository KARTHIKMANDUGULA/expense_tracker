class bank:
    def __init__(self,acc,balance):
        self.acc=acc
        self.__balance=balance
        self.history=[]
    
    def credit(self,amount):
        if amount>0:
            self.__balance +=amount
            print("=======================================================")
            print(f"amount of rs.{amount} is credited in acc.{self.acc}\nremaining balance is rs.{self.__balance}")
            print("=======================================================")
            self.history.append(f"credit,+{amount},balance,{self.__balance}\n")
        else :
            print("pls enter valid inputs")

    def debit(self,amount):
        if amount>0:
            if amount<=self.__balance:
                self.__balance-=amount
                print("=======================================================")
                print(f"amount of rs.{amount} is debited in acc.{self.acc}\nremaining balance is rs.{self.__balance}")
                print("=======================================================")
                self.history.append(f"debit,-{amount},balance,{self.__balance}\n")
            else:
                print("insufficeient funds in the bank.kindly enter less amount")
        else :
            print("pls enter valid inputs")
            print("=======================================================")

    def get_balance(self):
        return self.__balance

    def save(self):
        with open ("save_to_file.csv","a") as f:
            f.writelines(self.history)
while True:

    try:

        acc_no=int(input("enter acc_no:"))
        bal=float(input("pls deposit money:"))
        if bal<0:
            print("amount should not be negative,kindly enter correct amount")
        else :
            print("money deposited in bank sucessfully")
            acc1=bank(acc_no,bal)
            break
        
    except ValueError:
        print("enter valid inputs")


while True:
    n=input("choose[add,debit,check balance,exit]:").strip().lower()     
    if n=="add":
        try:
            acc1.credit(float(input("enter money to add:")))
        except ValueError:
            print("enter valid inputs")
    elif n=="debit":
        try:
            acc1.debit(float(input("enter money to debit:")))
        except ValueError:
            print("enter valid inputs")
    elif n=="check balance":
        print(f"total balance is:{acc1.get_balance()}")
        print("=======================================================")
    elif n=="exit":
        print("session saved,exiting")
        print("=======================================================")
        break
    else :
        print("enter valid type and try again")
        print("=======================================================")


acc1.save()
