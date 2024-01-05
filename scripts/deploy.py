from brownie import Lottery,config,network,accounts
from scripts.helpful_scripts import getAccount
import scripts.gui
from dotenv import load_dotenv
load_dotenv()
local = ["development","ganache-local"]
forked = ["mainnet-fork","mainnet-fork-dev"]

def deploy():
    account=getAccount()
    # price_feed_address = deploy_mock()
    contract=startLottery(account)
    a = input("Would you like to use the GUI?(Y/N):")
    
    if a=="Y" or a=="y":
        scripts.gui.main() #Start the GUI
        return
    
    choice = True
    while choice:
            print("1. Enter the lottery 2. Pick a winner 3. Get players 4. Get balance 5. Start a new lottery 6. Change Account")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                contract.enter({'from':account,'value':contract.getEnterFee()+1000})
                print(f"{account.address} entered the lottery")
            elif choice == 2:
                winner = contract.endLottery({'from':account})
                print(f"{winner.internal_transfers[0]['to']} won the lottery")
            elif choice == 3:
                players = contract.getPlayers({'from':account})
                print("Players: ")
                for player in players:
                    print(player)
            elif choice == 4:
                contract.getBalance({'from':account})
                print("Current Lottery balance: ",contract.getBalance())
            elif choice ==5:
                 contract.startLottery({'from':account})
                 print("New Lottery started")
            elif choice==6:
                address= input("Enter the private key of account you want to use: ")
                try:
                    accounts.add(address)
                    account = accounts[-1]
                except Exception as e:
                    print(e)
                print("Now Using: ",account)
            else:
                choice = False
def startLottery(account):
    if len(Lottery)<=0:
        try:
            Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],{"from":account},
                           publish_source=config["networks"][network.show_active()]["verify"])
        except Exception as e:
            raise Exception(e)
    return Lottery[-1]
 
#Executing    
def main():
    deploy()
