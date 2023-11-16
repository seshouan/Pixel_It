pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "./Simple_Auction.sol"

contract Gallery is ERC721Full {
    constructor() public ERC721Full("Certificate", "CERT") {}

    function awardCertificate(address student, string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newCertificateId = totalSupply();
        _mint(student, newCertificateId);
        _setTokenURI(newCertificateId, tokenURI);

        return newCertificateId;
    }
}

contract Pixel_IT_deploy {
    // create tokens for each image

    // create a gallery instance for bidding

    // save the address for the gallery

}