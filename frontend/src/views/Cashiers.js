import { useState, useEffect } from "react";
import { gqlPost } from "../tools/tools";
import { useParams } from "react-router-dom";
import { GET_CASHIERS, GET_ROOM } from "../gql/queries";
import { ADD_CASHIER } from "../gql/mutations";
import Web3 from 'web3';

import Input from "./Input";
import Button from "./Button";

function Cashiers() {
  const { id } = useParams();
  const [addresses, setAddresses] = useState([]);
  const [newAddress, setNewAddress] = useState("");
  useEffect(async () => {
    const d = await gqlPost(GET_CASHIERS, { id });
    const data = d.data.getCashiers;
    console.log(d);
    console.log(data);
    setAddresses(data);
  }, []);


  const sumbitCashier = async () => {
    var web3 = new Web3(window.ethereum);
    await window.ethereum.enable();
    var contract_abi = `[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "roomInternalId",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "PurchasePayment",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"name": "addCashier",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "contractStatus",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "endAgreement",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "deadline",
				"type": "uint256"
			},
			{
				"components": [
					{
						"internalType": "uint8",
						"name": "v",
						"type": "uint8"
					},
					{
						"internalType": "bytes32",
						"name": "r",
						"type": "bytes32"
					},
					{
						"internalType": "bytes32",
						"name": "s",
						"type": "bytes32"
					}
				],
				"internalType": "struct Sign",
				"name": "landlordSign",
				"type": "tuple"
			},
			{
				"components": [
					{
						"internalType": "uint8",
						"name": "v",
						"type": "uint8"
					},
					{
						"internalType": "bytes32",
						"name": "r",
						"type": "bytes32"
					},
					{
						"internalType": "bytes32",
						"name": "s",
						"type": "bytes32"
					}
				],
				"internalType": "struct Sign",
				"name": "tenantSign",
				"type": "tuple"
			}
		],
		"name": "endAgreementManually",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getBillingPeriodDuration",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getBillingsCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "cashierAddr",
				"type": "address"
			}
		],
		"name": "getCashierNonce",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getCashiersList",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "deadline",
						"type": "uint256"
					}
				],
				"internalType": "struct EndConsent",
				"name": "e",
				"type": "tuple"
			},
			{
				"components": [
					{
						"internalType": "uint8",
						"name": "v",
						"type": "uint8"
					},
					{
						"internalType": "bytes32",
						"name": "r",
						"type": "bytes32"
					},
					{
						"internalType": "bytes32",
						"name": "s",
						"type": "bytes32"
					}
				],
				"internalType": "struct Sign",
				"name": "sign",
				"type": "tuple"
			}
		],
		"name": "getEndConsentIssuer",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getLandlord",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getLandlordProfit",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getRentEndTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getRentStartTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getRentalRate",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getRoomInternalId",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTenant",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTenantProfit",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "deadline",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "nonce",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "value",
						"type": "uint256"
					}
				],
				"internalType": "struct Ticket",
				"name": "t",
				"type": "tuple"
			},
			{
				"components": [
					{
						"internalType": "uint8",
						"name": "v",
						"type": "uint8"
					},
					{
						"internalType": "bytes32",
						"name": "r",
						"type": "bytes32"
					},
					{
						"internalType": "bytes32",
						"name": "s",
						"type": "bytes32"
					}
				],
				"internalType": "struct Sign",
				"name": "sign",
				"type": "tuple"
			}
		],
		"name": "getTicketIssuer",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "mi",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "deadline",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "nonce",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			},
			{
				"components": [
					{
						"internalType": "uint8",
						"name": "v",
						"type": "uint8"
					},
					{
						"internalType": "bytes32",
						"name": "r",
						"type": "bytes32"
					},
					{
						"internalType": "bytes32",
						"name": "s",
						"type": "bytes32"
					}
				],
				"internalType": "struct Sign",
				"name": "cashierSign",
				"type": "tuple"
			}
		],
		"name": "pay",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "cashierAddr",
				"type": "address"
			}
		],
		"name": "removeCashier",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "deadline",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "tenant",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "rentalRate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "billingPeriodDuration",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "billingsCount",
				"type": "uint256"
			},
			{
				"components": [
					{
						"internalType": "uint8",
						"name": "v",
						"type": "uint8"
					},
					{
						"internalType": "bytes32",
						"name": "r",
						"type": "bytes32"
					},
					{
						"internalType": "bytes32",
						"name": "s",
						"type": "bytes32"
					}
				],
				"internalType": "struct Sign",
				"name": "landlordSign",
				"type": "tuple"
			}
		],
		"name": "rent",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "ti",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "signer",
				"type": "address"
			},
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "deadline",
						"type": "uint256"
					},
					{
						"internalType": "address",
						"name": "tenant",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "rentalRate",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "billingPeriodDuration",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "billingsCount",
						"type": "uint256"
					}
				],
				"internalType": "struct RentalPermit",
				"name": "rp",
				"type": "tuple"
			},
			{
				"components": [
					{
						"internalType": "uint8",
						"name": "v",
						"type": "uint8"
					},
					{
						"internalType": "bytes32",
						"name": "r",
						"type": "bytes32"
					},
					{
						"internalType": "bytes32",
						"name": "s",
						"type": "bytes32"
					}
				],
				"internalType": "struct Sign",
				"name": "sign",
				"type": "tuple"
			}
		],
		"name": "verifyRentalPermit",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdrawLandlordProfit",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdrawTenantProfit",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]`

    var response1 = await gqlPost(GET_ROOM, { id: id })
    var contract_address = response1['data']['room']['contractAddress']
    const contract1 = web3.eth.Contract(contract_abi, contract_address);
    console.log();
    contract1.methods.addCashier(newAddress).send();


    const d = await gqlPost(ADD_CASHIER, { id, address: newAddress });
    console.log(d);
  }

  return (
    <>
      <p>cashiers</p>
      {addresses && (
        <ul className="cashiers">
          {addresses.map((address) => (
            <li className="cashier__address">{address}</li>
          ))}
        </ul>
      )}
      <form className="add-cashier" onSubmit={sumbitCashier}>
        <Input
          type="text"
          k="add-cashier__address"
          onInput={(e) => setNewAddress(e.target.value)}
          value={newAddress}
          required
        />
        <Button type="submit" k="add-cashier__submit" />
      </form>
    </>
  );
}

export default Cashiers;
