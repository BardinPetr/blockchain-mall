// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

import "./EIP712.sol";

contract RentalAgreement is EIP712 {
    event PurchasePayment(uint amount);

    uint private _roomInternalId;
    address private _landlord;

    RentalPermit private _rentalPermit;
    uint private _rentStartTime;
    bool private _inRent = false;

    address[] _cashierAddresses;
    mapping(address => uint256) _cashierNonces;
    uint256 _curCashierNonce = 1;

    uint256 _totalIncome = 0;
    uint256 _monthIncome = 0;
    uint256 _curMonth = 0;

    bool _inDebt = false;

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
        if (_inRent) revert("The contract is being in not allowed state");

        RentalPermit memory tmpRP = RentalPermit(deadline, tenant, rentalRate, billingPeriodDuration, billingsCount);

        if (!verifyRentalPermit(_landlord, tmpRP, landlordSign)) revert("Invalid landlord sign");
        if (deadline < block.timestamp) revert("The operation is outdated");
        if (msg.sender != tenant) revert("The caller account and the account specified as a tenant do not match");
        if (tenant == _landlord) revert("The landlord cannot become a tenant");
        if (rentalRate <= 0) revert("Rent amount should be strictly greater than zero");
        if (billingPeriodDuration <= 0) revert("Rent period should be strictly greater than zero");
        if (billingsCount <= 0) revert("Rent period repeats should be strictly greater than zero");
        if (msg.value < rentalRate) revert("Incorrect deposit");

        _inRent = true;
        _rentStartTime = block.timestamp;
        _rentalPermit = tmpRP;
    }

    function removeCashier(address cashierAddr) public {
        if (msg.sender != _rentalPermit.tenant) revert("You are not a tenant");
        if (_cashierNonces[cashierAddr] == 0) revert("Unknown cashier");

        uint i = 0;
        for (; i < _cashierAddresses.length; i++) if (_cashierAddresses[i] == cashierAddr) break;
        _cashierAddresses[i] = _cashierAddresses[_cashierAddresses.length - 1];
        _cashierAddresses.pop();

        _cashierNonces[cashierAddr] = 0;
    }

    function addCashier(address addr) public {
        if (msg.sender != _rentalPermit.tenant) revert("You are not a tenant");
        if (addr == _landlord) revert("The landlord cannot become a cashier");
        if (addr == 0x0000000000000000000000000000000000000000) revert("Zero address cannot become a cashier");

        _cashierAddresses.push(addr);
        _cashierNonces[addr] = _curCashierNonce++;
    }

    function getCashierNonce(address cashierAddr) public view returns (uint)  {
        return _cashierNonces[cashierAddr];
    }

    function getCashiersList() public view returns (address[] memory){
        return _cashierAddresses;
    }

    function getCurMonth() private view returns (uint256) {
        return ((uint256)(block.timestamp) - (uint256)(_rentStartTime)) / _rentalPermit.billingPeriodDuration;
    }

    function updateIncomes() private {
        uint256 month = getCurMonth();

        if (_inDebt) return;

        if (month > (_curMonth + 1)) {
            _inDebt = true;
        } else if(month == (_curMonth + 1)) {
            if(_monthIncome >= _rentalPermit.rentalRate) {
                _totalIncome += _monthIncome - (month < _rentalPermit.billingsCount ? _rentalPermit.rentalRate : 0);
                _monthIncome = 0;
            } else {
                _inDebt = true;
            }
        }
        _curMonth = month;
    }

    function pay(uint deadline, uint nonce, uint value, Sign memory cashierSign) public payable {
        Ticket memory t = Ticket(deadline, nonce, value);
        address cashier = getTicketIssuer(t, cashierSign);

        if (_cashierNonces[cashier] == 0) revert("Unknown cashier");
        if (deadline < block.timestamp) revert("The operation is outdated");
        if (nonce != _cashierNonces[cashier]) revert("Invalid nonce");
        if (msg.value != value) revert("Invalid value");
        if (deadline > getRentEndTime()) revert("The contract is being in not allowed state");

        updateIncomes();

        if (_inDebt) revert("The contract is being in not allowed state");

        _monthIncome += value;

        _cashierNonces[cashier]++;
        emit PurchasePayment(value);
    }

    function getTenantProfit() public view returns (uint) {
        uint256 month = getCurMonth();
        uint256 curRentalRate = (month < (_rentalPermit.billingsCount - 1) ? _rentalPermit.rentalRate : 0);
        return _totalIncome + (_monthIncome >= curRentalRate ? (_monthIncome - curRentalRate) : 0);
    }

    function withdrawTenantProfit() public {
        updateIncomes();
        uint256 profit = getTenantProfit();
        (bool success, ) = (payable(_rentalPermit.tenant)).call{value:profit}("");
        if (success) {
            _monthIncome = _monthIncome - (profit - _totalIncome);
            _totalIncome = 0;
        }
    }
}