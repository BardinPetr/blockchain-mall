// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

struct Sign {
    uint8 v;
    bytes32 r;
    bytes32 s;
}

contract RentalAgreement {
    uint private _roomInternalId;
    address private _landlord;

    constructor(uint roomInternalId) {
        _landlord = msg.sender;
        _roomInternalId = roomInternalId;
    }

    function getRoomInternalId() public view returns (uint) {
        return _roomInternalId;
    }

    function getLandlord() public view returns (address) {
        return _landlord;
    }

    function getTenant() public view returns (address) {}

    function getBillingPeriodDuration() public view returns (uint) {}

    function getRentStartTime() public view returns (uint) {}

    function getRentEndTime() public view returns (uint) {}

    function getRentalRate() public view returns (uint) {}

    /*
    RentalPermit(uint256 deadline, address tenant, uint256 rentalRate, uint256 billingPeriodDuration, uint256 billingsCount)
    EIP712Domain(string name, string version, address verifyingContract) // name = "Rental Agreement", version = "1.0"
    */

    // function rent(uint deadline, address tenant, uint rentalRate, uint billingPeriodDuration, uint billingsCount, Sign landlordSign) public payable {}

}
