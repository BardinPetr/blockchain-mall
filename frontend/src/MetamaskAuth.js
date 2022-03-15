import { useEffect, useState } from "react";

import { initializeConnector } from "@web3-react/core";
import { MetaMask } from "@web3-react/metamask";

// import { Web3 } from "web3";

const [metaMask, hooks] = initializeConnector(
  (actions) => new MetaMask(actions)
);

metaMask.connectEagerly();
localStorage.setItem("access_token_cookie", "");

const {
  useChainId,
  useAccount,
  useError,
  // useIsActivating,
  useIsActive,
  useProvider,
} = hooks;

function MetamaskAuth() {
  const chainId = useChainId(77);
  const account = useAccount();
  const error = useError();
  // const isActivating = useIsActivating();
  const isActive = useIsActive();
  // const provider = useProvider();
  const [accountChanged, setAccountChanged] = useState(undefined);
  const [signed, setSigned] = useState(false);

  const authenticate = async () => {
    if (!isActive) {
      await metaMask.activate(chainId);
    }
    setAccountChanged(false);
  };

  function parseSignature(signature) {
    signature = signature.substring(2, 132);
    var r = signature.substring(0, 64);
    var s = signature.substring(64, 128);
    var v = signature.substring(128, 130);
    console.log(signature);
    return {
      r: "0x" + r,
      s: "0x" + s,
      v: parseInt(v, 16),
    };
  }

  async function signMessage() {
    const data =
      '{"primaryType": "AuthMsg", "types": {"EIP712Domain": [{"name": "name", "type": "string"}, {"name": "version", "type": "string"}], "AuthMsg": [{"name": "address", "type": "address"}, {"name": "is_landlord", "type": "bool"}, {"name": "timestamp", "type": "uint256"}]}, "domain": {"name": "Rental Agreement", "version": "1.0"}, "message": {"address": "0x6a7615121b01A4a4e5f2eAD25EC53422f3453452", "is_landlord": true, "timestamp": 1647349201}}';

    const signer = Web3.utils.toChecksumAddress(account);

    const res = await window.ethereum.request({
      method: "eth_signTypedData_v3",
      params: [signer, data],
      from: signer,
    });

    console.log("sdfsdsdfsdf", parseSignature(res));
  }

  useEffect(async () => {
    if (account) {
      console.log(localStorage.getItem("lastAccount"));
      setAccountChanged(localStorage.getItem("lastAccount") !== account);
      localStorage.setItem("lastAccount", account);
      console.log(localStorage.getItem("lastAccount"));
      if (!signed) {
        console.log("sdfsdfsdsdfsdfsdf")
        await signMessage();
        setSigned(true);
      }
    }
  }, [account]);

  return (
    <>
      {isActive && !accountChanged ? (
        <p className="account__address">{account}</p>
      ) : (
        <>
          <button
            className="authentication__authenticate"
            onClick={authenticate}
          >
            Authenticate
          </button>

          {accountChanged && (
            <p className="authentication__warning">
              Your MetaMask account is different from the one you authenticated
              with before
            </p>
          )}
        </>
      )}
      {error && <p>Error: {error.toString()}</p>}
    </>
  );
}

export default MetamaskAuth;
