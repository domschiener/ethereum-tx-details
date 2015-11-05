# Ethereum Tx Details

Super simple program that provides more thorough information about a specific transaction or Ethereum account. The program basically interacts with several API's to extract the necessary information.

* **Etherscan.io**: It's used to get all the transactions from a specific Ethereum address
* **Poloniex**: Is used to get the Eth-BTC price at a 1 hour interval when a transaction was sent
* **Coinbase**: Is used to get the BTC-USD price at a 1 hour interval when a transaction was sent

## Extra Information

The application is able to accumulate and categorize the following information and save it locally into a CSV file:
* `Type` of Transaction: Whether it is a `tx` or `contract`
* `Timestamp`
* `Gasused`
* `Gasprice`
* `Ether<->USD in 1 hour interval`
* `Total Tx Cost in Ether`
* `Total Tx Cost in USD`

## How to Use

Currently the program only works with an Ethereum address. That means you need to specify an address and the program automatically extracts the transactions and gets all the additional information. To run the program, simply type in:
```
$ python getdata.py 1 <address>
```

`<address>` being the placeholder of the address.
