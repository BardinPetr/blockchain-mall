import { useEffect } from "react";

import { initializeConnector } from "@web3-react/core";
import { MetaMask } from "@web3-react/metamask";

const [metaMask, hooks] = initializeConnector(
  (actions) => new MetaMask(actions)
);

console.log(hooks)

const {
  useChainId,
  useAccount,
  useError,
  // useIsActivating,
  useIsActive,
  // useProvider,
} = hooks;

function MetamaskAuth() {
  const chainId = useChainId(77);
  const account = useAccount();
  const error = useError();
  // const isActivating = useIsActivating();
  const isActive = useIsActive();
  // const provider = useProvider();

  const authenticate = async () => {
    await metaMask.activate(chainId);
  };

  useEffect()
  return (
    <>
      {isActive ? (
        <p className="account__address">{account}</p>
      ) : (
        <button className="authentication__authenticate" onClick={authenticate}>
          Authenticate
        </button>
      )}
      {error && <p>Error: {error.toString()}</p>}
    </>
  );
}

export default MetamaskAuth;
