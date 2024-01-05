// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
contract Lottery{
    using SafeMathChainlink for uint256;
    AggregatorV3Interface internal priceFeed;
    address internal manager;
    address payable[] internal players;
    uint256 public EntryFee;
    uint16 public lottery_state;
    address public lWinner = address(0x0);
    modifier onlyManager(){
        require(msg.sender == manager);
        _;
    }
    constructor(address _priceFeedAddress) public{
        manager = msg.sender;
        EntryFee = 50 * (10 ** 18);
        priceFeed=AggregatorV3Interface(_priceFeedAddress);
    }
    function enter() public payable{
        require(lottery_state==1,"Lottery is not open!");
        require(msg.value > getEnterFee(),"Not enough ETH!");
        players.push(msg.sender);
    }
    function getPlayers() public onlyManager view returns(address payable[] memory){
        return players;
    }
    function owner() public view returns(address){
        return manager;
    }
    function getCount() public view returns(uint256){
        uint256 count=0;
        for(uint256 i=0;i<players.length;i++){
            if(players[i] == msg.sender){
                count++;
            }
        }
        return count;
    }
    function startLottery() public onlyManager{
        players = new address payable[](0);
        lottery_state=1;
    }
    function getBalance() public view returns(uint256){
        return address(this).balance;
    }
    function endLottery() public onlyManager returns(address) {
        lottery_state=0;
        uint256 r = random();
        address payable winner;
        uint256 index = r % players.length;
        winner = players[index];
        winner.transfer(address(this).balance);
        lWinner = winner;
        players = new address payable[](0);
        return winner;
    }
    function lastWinner() public view returns(address){
        return lWinner;
    }
    function random() internal view returns(uint256){
        return uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, players, block.number,
                                block.gaslimit, block.coinbase, blockhash(block.number-1))));
    }
    function getEnterFee() public view returns(uint256){
        uint256 linkPrice = getLatestPrice();
        uint256 price = (EntryFee * (10 ** 18)) / linkPrice;
        return price;
    }
    function getLatestPrice() public view returns(uint256){
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }
}