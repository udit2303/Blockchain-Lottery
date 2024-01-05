from brownie import network,accounts,MockV3Aggregator,config
import os
from dotenv import load_dotenv
load_dotenv()
local = ["development","ganache-local"]
forked = ["mainnet-fork","mainnet-fork-dev"]
decimals = 8
initial_value = 200000000000
def getAccount():
    if(network.show_active() in local or network.show_active() in forked):
        return accounts[0]
    else:
        return accounts.add(os.getenv("PRIVATE_KEY"))
def deploy_mock():
    if network.show_active() not in local:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        print(f"Active network is {network.show_active()}")
        print("Deploying Mocks...")
        if len(MockV3Aggregator)<=0:
            MockV3Aggregator.deploy(decimals,initial_value,{"from":getAccount()})
        price_feed_address=MockV3Aggregator[-1].address
        print("Mock deployed")
    return price_feed_address