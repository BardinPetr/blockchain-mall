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
    // function rent(uint deadline, address tenant, uint rentalRate, uint billingPeriodDuration, uint billingsCount, uint8 v, bytes32 r, bytes32 s) public payable {
        if(_inRent) revert("The contract is being in not allowed state");

        RentalPermit memory tmpRP = RentalPermit(deadline, tenant, rentalRate, billingPeriodDuration, billingsCount);

        if(!verify(_landlord, tmpRP, landlordSign)) revert("Invalid landlord sign");
        // if(!verify(_landlord, tmpRP, Sign(v,r,s))) revert("Invalid landlord sign");
        if(deadline < block.timestamp) revert("The operation is outdated");
        if(msg.sender != tenant) revert("The caller account and the account specified as a tenant do not match");
        if(tenant == _landlord) revert("The landlord cannot become a tenant");
        if(rentalRate <= 0) revert("Rent amount should be strictly greater than zero");
        if(billingPeriodDuration <= 0) revert("Rent period should be strictly greater than zero");
        if(billingsCount <= 0) revert("Rent period repeats should be strictly greater than zero");
        if(msg.value < rentalRate) revert("Incorrect deposit");

        _inRent = true;
        _rentStartTime = block.timestamp;
        _rentalPermit = tmpRP;
    }
}
