// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

struct Sign {
    uint8 v;
    bytes32 r;
    bytes32 s;
}

string constant RP_TYPE = "RentalPermit(uint256 deadline,address tenant,uint256 rentalRate,uint256 billingPeriodDuration,uint256 billingsCount)";
struct RentalPermit {
    uint256 deadline;
    address tenant;
    uint256 rentalRate;
    uint256 billingPeriodDuration;
    uint256 billingsCount;
}

string constant TICKET_TYPE = "Ticket(uint256 deadline,uint256 nonce,uint256 value)";
struct Ticket {
    uint256 deadline;
    uint256 nonce;
    uint256 value;
}

contract EIP712 {
    bytes32 private constant TICKET_TYPEHASH = keccak256(abi.encodePacked(TICKET_TYPE));
    bytes32 private constant RP_TYPEHASH = keccak256(abi.encodePacked(RP_TYPE));

    string private constant EIP712_DOMAIN = "EIP712Domain(string name,string version,address verifyingContract)";
    bytes32 private constant EIP712_DOMAIN_TYPEHASH = keccak256(abi.encodePacked(EIP712_DOMAIN));
    bytes32 private DOMAIN_SEPARATOR = keccak256(abi.encode(
        EIP712_DOMAIN_TYPEHASH,
        keccak256("Rental Agreement"),
        keccak256("1.0"),
        this
    ));

    function hashRentalPermit(RentalPermit memory rp) private view returns (bytes32) {
        return keccak256(abi.encodePacked(
                "\x19\x01",
                DOMAIN_SEPARATOR,
                keccak256(abi.encode(
                    RP_TYPEHASH,
                    rp.deadline,
                    rp.tenant,
                    rp.rentalRate,
                    rp.billingPeriodDuration,
                    rp.billingsCount
                ))
            ));
    }

    function hashTicket(Ticket memory t) private view returns (bytes32) {
        return keccak256(abi.encodePacked(
                "\x19\x01",
                DOMAIN_SEPARATOR,
                keccak256(abi.encode(
                    TICKET_TYPEHASH,
                    t.deadline,
                    t.nonce,
                    t.value
                ))
            ));
    }

    function verifyRentalPermit(address signer, RentalPermit memory rp, Sign memory sign) public view returns (bool) {
        return signer == ecrecover(hashRentalPermit(rp), sign.v, sign.r, sign.s);
    }

    function getTicketIssuer(Ticket memory t, Sign memory sign) public view returns (address) {
        return ecrecover(hashTicket(t), sign.v, sign.r, sign.s);
    }
}
