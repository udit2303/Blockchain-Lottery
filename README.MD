This is a simple lottery system on a blockchain. Users can enter the lottery by purchasing lottery tickets with a certain fee. They have the option to purchase multiple tickets.

## How it Works

1. Users can enter the lottery by paying the required fee.
2. The owner of the lottery contract is responsible for starting and ending the lottery.
3. Once the lottery is over, a random user will be selected as the winner.

## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)

## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.

Install brownie via pipx
```bash
pip install --user pipx
pipx ensurepath
# restart your terminal
pipx install eth-brownie
```
You will have to inject customtkinter to use the GUI.
```bash
pipx inject eth-brownie customtkinter
```
Set your environment variables

Set your `INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). 

You can get a `INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/). 

You'll also need testnet Sepolia ETH and LINK. You can get LINK and ETH into your wallet by using the [Sepolia faucets located here](https://faucets.chain.link/sepolia).

## Compiling
To compile the contract, run
```bash
brownie compile
```

## Deploying
If you want to run the deployment script on a specific network, you can specify the network name with the --network flag. For example, if you wanted to deploy to the Sepolia test network, you would use the command 
```bash
brownie run scripts/deploy --network Sepolia.
```
Remember to replace Sepolia with the name of the network you want to use(ensure it is added to the [networks list in brownie](https://eth-brownie.readthedocs.io/en/stable/network-management.html)).
This deploys our Smart Contract to the Sepolia network. We Will access this contract(or the latest deployed contract) in our GUI.

After the contract is deployed, the GUI can be access by 

```bash
brownie run scripts/deploy --network Sepolia
LotteryProject is the active project.

Running 'scripts\deploy.py::main'...
Would you like to use the GUI?(Y/N): # Enter Y to use the GUI
```


![GUI](https://i.imgur.com/DZzO0Je.png)
![GUI2](https://i.imgur.com/QsoPMfN.png)
![GUI3](https://i.imgur.com/CBrtDpm.png)


