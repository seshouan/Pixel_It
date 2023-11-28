import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from typing import Any, List
from dataclasses import dataclass

load_dotenv("keys.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load Art Gallery ABI
    with open(Path("abi.json")) as f:
        contract_abi= json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract using web3
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()

# # Create Listing

listing_id_1 = contract.functions.createListing("QmNxrj2mNLS7Jra2hHNH9sLjn9YtQDEgZmCYv4Eir3qVMV", 5).call()
listing_id_2 = contract.functions.createListing("QmQM8s9dR8beg1RjfqeacL8FrYNecR5tzgUoUr5nTTxQDw", 4).call()
listing_id_3 = contract.functions.createListing("QmSq84tpk4wQcSGVjNuyYzNe4s2R9VuabySYeEPU3ZrPoC", 3).call()

# I want to add listing variables to the database but it doesn't return number, it returns:
st.write(f'ListingId: {listing_id_1}')


# Display Pictures 

art_database = {
    "Little Mermaid": ["Little Mermaid", 1, "https://ipfs.io/ipfs/QmNxrj2mNLS7Jra2hHNH9sLjn9YtQDEgZmCYv4Eir3qVMV"],
    "Bike": ["Bike", 2, "https://ipfs.io/ipfs/QmQM8s9dR8beg1RjfqeacL8FrYNecR5tzgUoUr5nTTxQDw"],
    "Scottland": ["Scottland", 3,"https://ipfs.io/ipfs/QmSq84tpk4wQcSGVjNuyYzNe4s2R9VuabySYeEPU3ZrPoC"],
}


################################################################################
# Streamlit Code

# Create Streamlit application headings using `st.markdown` to explain this app 
st.markdown("# This app is for Bidding on Art")

# get_images

cols=st.columns(3)

ad_list= list(art_database.values())

for each_col_idx in range(len(cols)):
    image=ad_list[each_col_idx]
    with cols[each_col_idx]:
        st.image(image[2], width=250)
        st.write(f'name: {image[0]}')
        st.write(f'ListingId: {image[1]}')
    

# Create Bid
st.title("Bid")
st.write("Choose a ListingID to create Bid")
listing_id = st.selectbox("Select ListingId", options=[1,2,3])

st.write("Choose an account to create Bid")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")



