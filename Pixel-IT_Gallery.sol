//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import "./Auction.sol";

contract Pixel_IT_deploy {
    constructor(address payable auction_creator) {
        // create an instance of the Auction runner
        NFTAuction auction = new NFTAuction();

        // mint the tokens for each digital art
        uint256 tokenId = auction.mint("QmNxrj2mNLS7Jra2hHNH9sLjn9YtQDEgZmCYv4Eir3qVMV", auction_creator);

        // create a listing for each digital art
        auction.createAuctionListing(5, tokenId, 180);
    }
}
