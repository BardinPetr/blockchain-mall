import { useEffect, useState } from "react";

import { initializeConnector } from "@web3-react/core";
import { MetaMask } from "@web3-react/metamask";

const [metaMask, hooks] = initializeConnector(
  (actions) => new MetaMask(actions)
);

metaMask.connectEagerly();

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

  const authenticate = async () => {
    if (!isActive) {
      await metaMask.activate(chainId);
    }
    setAccountChanged(false);
  };

  useEffect(() => {
    if (account) {
      console.log(localStorage.getItem("lastAccount"));
      setAccountChanged(localStorage.getItem("lastAccount") !== account);
      localStorage.setItem("lastAccount", account);
      console.log(localStorage.getItem("lastAccount"));
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
