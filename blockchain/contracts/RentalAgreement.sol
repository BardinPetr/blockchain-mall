// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

import "./EIP712.sol";

contract RentalAgreement is EIP712 {

    uint private _roomInternalId;
    address private _landlord;
    RentalPermit private _rentalPermit;
    uint private _rentStartTime;
    bool private _inRent = false;

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

    function getTenant() public view returns (address) {
        return _rentalPermit.tenant;
    }

    function getRentalRate() public view returns (uint) {
        return _rentalPermit.rentalRate;
    }

    function getBillingPeriodDuration() public view returns (uint) {
        return _rentalPermit.billingPeriodDuration;
    }

    function getRentStartTime() public view returns (uint) {
        return _rentStartTime;
    }

    function getRentEndTime() public view returns (uint) {
        return _rentStartTime + _rentalPermit.billingsCount * _rentalPermit.billingPeriodDuration;
    }

    function rent(uint deadline, address tenant, uint rentalRate, uint billingPeriodDuration, uint billingsCount, Sign memory landlordSign) public payable {
        if(_inRent) revert("The contract is being in not allowed state");
        _rentalPermit = RentalPermit(deadline, tenant, rentalRate, billingPeriodDuration, billingsCount);
        _inRent = true;
        _rentStartTime = block.timestamp;
    }
}
