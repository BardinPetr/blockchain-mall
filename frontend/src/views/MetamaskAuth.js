import {useEffect, useState} from "react";
import {getLastAccount, parseSignature, setLastAccount} from "../tools/tools";
import {useMutation} from "@apollo/client";
import {AUTHENTICATE, REQUEST_AUTHENTICATION} from "../gql/mutations";

localStorage.setItem("access_token_cookie", "");

const eth = window.ethereum;

const MetamaskAuth = () => {
    const [accountInvalid, setAccountInvalid] = useState(false);
    const [authenticated, setAuthenticated] = useState(false);
    const [account, setAccount] = useState("");

    const [serverReqAuth] = useMutation(REQUEST_AUTHENTICATION, {
        fetchPolicy: "no-cache",
    })

    const [serverAuth] = useMutation(AUTHENTICATE, {
        fetchPolicy: "no-cache"
    })

    const authenticate = async (address) => {
        const res = await serverReqAuth({
            variables: {address},
        });

        const sign = await eth.request({
            method: "eth_signTypedData_v3",
            params: [address, res.data.message],
            from: address,
        });

        const rsv = parseSignature(sign);

        console.log({
                address,
                ...rsv
            })

        const authed = await serverAuth({
            variables: {
                address,
                ...rsv
            }
        })

        console.log(authed)
    }

    const connect = async () => {
        let acc = (await eth.request({method: "eth_requestAccounts"}))[0];
        // acc = Web3.utils.toChecksumAddress(acc);
        setAccount(acc);
        setLastAccount(acc);
        await authenticate(acc);
    };

    const checkAccounts = (accounts) => setAccountInvalid(accounts.length > 0 && getLastAccount() !== accounts[0]);

    useEffect(() => eth.request({method: "eth_accounts"}).then(checkAccounts), []);
    eth.on('accountsChanged', checkAccounts)

    return (
        <div>
            {authenticated ? (
                <p className="account__address">{account}</p>
            ) : (
                <button
                    className="authentication__authenticate"
                    onClick={connect}
                >
                    Authenticate
                </button>
            )}
            {accountInvalid && (
                <p className="authentication__warning">
                    Your MetaMask account is different from the one you authenticated
                    with before
                </p>
            )}
        </div>
    );
}

export default MetamaskAuth;