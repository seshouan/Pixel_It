import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from typing import Any, List
from dataclasses import dataclass

load_dotenv("access.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

@st.cache_resource
def load_contract():
    # Load Art Gallery ABI
    with open(Path("deployer_abi.json")) as f:
        deployer_contract_abi= json.load(f)
    # Set the contract address (this is the address of the  deployed contract)
    deployer_contract_address = os.getenv("DEPLOYER_CONTRACT_ADDRESS")
    # Get the contract using web3
    deployer_contract = w3.eth.contract(
        address=deployer_contract_address,
        abi=deployer_contract_abi
    )
    with open(Path("auction_abi.json")) as f:
        auction_contract_abi= json.load(f)
    # Set the contract address (this is the address of the  deployed contract)
    auction_contract_address = os.getenv("AUCTION_CONTRACT_ADDRESS")
    # Get the contract using web3
    auction_contract = w3.eth.contract(
        address=auction_contract_address,
        abi=auction_contract_abi
    )
    return auction_contract

# Load the contract
contract = load_contract()

################################################################################
# Streamlit Code

# Create Streamlit application headings using `st.markdown` to explain this app 
st.markdown("# This app is for Bidding on Art")

# get_images

# ad_list= list(art_database.values())
listing_count=contract.functions.listingCounter().call()
cols=st.columns(max(listing_count, 3))
for each_col_idx in range(listing_count): 
    listing_id=each_col_idx+1
    token_uri=contract.functions.tokenURI(listing_id).call()
    listing=contract.functions.listings(listing_id).call()
    image=f'https://ipfs.io/ipfs/'+token_uri
    with cols[each_col_idx]:
        st.image(image, width=250)
        st.write(f'name: {listing[1]}')
        st.write(f'ListingId: {listing[1]}')

# Create Bid
st.title("Bid")
st.write("Choose a ListingID to create Bid")
listing_id = st.selectbox("Select ListingId", options=range(1, listing_count+1))
st.markdown("---")
            
st.write("Choose an account to create Bid")
accounts = w3.eth.accounts
address = st.sidebar.selectbox("Select Account", options=accounts)
pkey=st.sidebar.text_input('Enter Private Key')
st.sidebar.markdown("---")

st.write("Input Bid Amount")
bid_amount = st.slider("Select Account in Wei", 0,100)
st.write("Your bid amount is",bid_amount)
st.markdown("---")
# eth.contract.value= bid_amount

# w3.to_wei(1,'ether')

# st.write("Withdraw Bid")
# bid_amount = st.slider("Select Account in Ether", 0,10000)
# st.write("Your bid amount is",bid_amount)
# st.markdown("---")
if st.button('Bid'): 
    txn={'from': address, 
         # 'to': os.getenv("AUCTION_CONTRACT_ADDRESS"), 
         'value': bid_amount, 
         'nonce': w3.eth.get_transaction_count(address)}

    call_function=contract.functions.bid(listing_id).build_transaction(txn)
    signed_txn=w3.eth.account.sign_transaction(call_function, private_key=pkey)
    sent_txn=w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(sent_txn)

    st.write(receipt)

#Complete Auction

#Withdraw