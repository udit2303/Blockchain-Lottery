from brownie import accounts, Lottery    
from tkinter import *
from tkinter import messagebox
from math import *
import customtkinter as ctk, requests, dotenv
dotenv.load_dotenv()
def gui():
    root = ctk.CTk()
    root.title("Lottery")
    root.geometry("500x500") #set the size of the window
    if len(Lottery)<=0:
        messagebox.showerror("Error","No Lottery Contract found")
        return
    contract = Lottery[-1] #get the latest deployed contract
    def update():
        #Update the GUI
        global CurrentBalance,balance,lastWinner,currentState
        CurrentBalance.configure(text=f'Current Lottery Balance:{round(contract.getBalance({"from":accounts[0]})/10**18,6)}ETH')
        lastWinner.configure(text=f'Last Winner:{contract.lastWinner({"from":accounts[0]})}')
        currentState.configure(text=f'Current State:{"OPEN" if contract.lottery_state()==1 else "CLOSED"}')
        balance.configure(text=f'Balance:{round(accounts[0].balance()/10**18,6)}ETH')
        pass

    def login(acc):
        #Change settings when logging into the account
        try:
            accounts.add(acc)
        except Exception as e:
            messagebox.showerror("ERROR",e)
            return
        global label,balance,CurrentBalance,lastWinner,currentState
        address=accounts[0].address
        isOwner=False
        if contract.owner() == accounts[0]:
            isOwner=True
        label = ctk.CTkLabel(root,text=f'Account:{address[:5]}...{address[-5:]}')
        balance = ctk.CTkLabel(root,text=f'Balance:{round(accounts[0].balance()/10**18,6)}ETH')
        CurrentBalance = ctk.CTkLabel(root,text=f'Current Lottery Balance:{round(contract.getBalance()/10**18,6)}ETH')
        currentState = ctk.CTkLabel(root,text=f'Current State:{"OPEN" if contract.lottery_state()==1 else "CLOSED"}')
        currentState.grid(row=2,column=0,columnspan=4)
        CurrentBalance.grid(row =3, column=0, columnspan = 4)
        lastWinner = ctk.CTkLabel(root,text=f'Last Winner:{contract.lastWinner({"from":accounts[0]})}')
        lastWinner.place(anchor=CENTER,relx=0.5,rely=0.5)
        balance.grid(row=1,column=1)
        label.grid(row=0,column=1)
        logoutButton.configure(state="normal")
        loginButton.configure(state="disabled")
        enterButton.configure(state="normal")
        if isOwner:
            endButton.configure(state="normal")
            startButton.configure(state="normal")
            playersButton.configure(state="normal")
        balanceButton.configure(state="normal")
        countButton.configure(state="normal")
    def logout():
        #Change settings when logging out of the account
        global label,balance
        label.destroy()
        balance.destroy()
        accounts.clear()
        currentState.destroy()
        CurrentBalance.destroy()
        lastWinner.destroy()
        logoutButton.configure(state="disabled")
        loginButton.configure(state="normal")
        enterButton.configure(state="disabled")
        endButton.configure(state="disabled")
        startButton.configure(state="normal")
        playersButton.configure(state="disabled")
        balanceButton.configure(state="disabled")
        countButton.configure(state="disabled")

    def acc():
        
        dialog = ctk.CTkInputDialog(text="ENTER PRIVATE KEY:", title="WALLET")
        acc=dialog.get_input()
        if acc and not acc.startswith("0x"):
            acc = "0x" + acc
        login(acc)

    def enter():
        if contract.lottery_state() == 0:
            messagebox.showerror("Error","Lottery is not OPEN")
            return
        if accounts[0].balance() < contract.getEnterFee({'from':accounts[0]}):
            messagebox.showerror("Error","Insufficient balance")
            return
        amt = contract.getEnterFee({'from':accounts[0]})+1000
        #https://api.coinbase.com/v2/exchange-rates?currency=ETH
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd").json()["ethereum"]["usd"]
        ask = messagebox.askquestion("Confirmation",f"Are you sure you want to enter the lottery with {round(amt/10**18,6)} ETH({round((amt/10**18)*response,4)}USD)?")
        if ask=="no":
            messagebox.showwarning("Cancelled","You did not enter the lottery")
            return
        tx = contract.enter({'from':accounts[0],'value':amt})
        tx.wait(1)
        messagebox.showinfo("Success","You have entered the lottery")
        update()

    def end():
        #Check if Lottery is Inactive
        if contract.lottery_state() != 1:
            messagebox.showerror("Error","Lottery is not OPEN")
            return
        contract.endLottery({'from':accounts[0]})
        messagebox.showinfo("Success","The lottery has ended")
        update()
        pass

    def start():
        #Check if Lottery is Active
        if contract.lottery_state() != 0:
            messagebox.showerror("Error","Lottery is not CLOSED")
            return
        try:
            contract.startLottery({'from':accounts[0]})
        except Exception as e:
            messagebox.showerror("Error",e)
            return
        messagebox.showinfo("Success","The lottery has started")
        update()
        pass

    def players():

        player_list = contract.getPlayers({'from':accounts[0]})
        messagebox.showinfo("Players","\n".join(player_list) if player_list else "No players")
        pass

    def current_balance():

        bal = contract.getBalance({'from':accounts[0]})
        messagebox.showinfo("Current Lottery Balance: ",str(round(bal/10**18,6))+" ETH" if bal else "0 ETH")
        pass

    def count():

        messagebox.showinfo("Total Entries: ", f"{contract.getCount({'from':accounts[0]})} entries")
        pass
    def setup():
        #Intial Settings for buttons
        loginButton.grid(row=0,column=0)
        logoutButton.grid(row=1,column=0)
        logoutButton.configure(state="disabled")
        for i in range(2,6):
            root.grid_rowconfigure(i,weight=1)
        enterButton.grid(row=6,column=0)
        enterButton.configure(state="disabled")
        endButton.grid(row=6,column=1)
        endButton.configure(state="disabled")
        startButton.grid(row=6,column=2)
        startButton.configure(state="disabled")
        playersButton.grid(row=7,column=0)
        playersButton.configure(state="disabled")
        balanceButton.grid(row=7,column=1)
        balanceButton.configure(state="disabled")
        countButton.grid(row=7,column=2)
        countButton.configure(state="disabled")

    #Setup the GUI
    loginButton = ctk.CTkButton(root, text="ADD WALLET", command=acc)
    logoutButton = ctk.CTkButton(root, text="REMOVE WALLET", command=logout)
    enterButton = ctk.CTkButton(root, text="ENTER LOTTERY", command=enter)
    endButton = ctk.CTkButton(root, text="END LOTTERY", command=end)
    startButton = ctk.CTkButton(root, text="START LOTTERY", command=start)
    playersButton = ctk.CTkButton(root, text="PLAYERS", command=players)
    balanceButton = ctk.CTkButton(root, text="BALANCE", command=current_balance)
    countButton = ctk.CTkButton(root, text="ENTRIES", command=count)
    setup()
    
    root.mainloop()
def main():
    gui()