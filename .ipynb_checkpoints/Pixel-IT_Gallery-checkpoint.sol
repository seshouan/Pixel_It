//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Auction.sol";

contract Pixel_IT_deploy {
    address public auction_creator;
    NFTAuction public auction;

    constructor() {
        auction_creator = msg.sender;
        // create an instance of the Auction runner
        auction = new NFTAuction();
    }

    function createListing (string memory tokenURI, uint256 price) public {
        // mint the tokens for each digital art
        uint256 tokenId = auction.mint(tokenURI, auction_creator);
        // // // create a listing for each digital art
        auction.createAuctionListing(price, tokenId, 60, auction_creator);
    }
}