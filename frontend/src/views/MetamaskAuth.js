import {useEffect, useState} from "react";
import {decodeAuthCookie, getLastAccount, parseSignature, setAuthCookie, setLastAccount, gqlPost} from "../tools/tools";
import {useMutation} from "@apollo/client";
import {AUTHENTICATE, GET_ACCESS_TOKEN, REQUEST_AUTHENTICATION} from "../gql/mutations";
import Web3 from "web3";

const eth = window.ethereum;

const MetamaskAuth = ({children}) => {
    const [accountInvalid, setAccountInvalid] = useState(false);
    const [authenticated, setAuthenticated] = useState(false);
    const [account, setAccount] = useState("");

    const [serverReqAuth] = useMutation(REQUEST_AUTHENTICATION, {
        fetchPolicy: "no-cache",
    })

    const [serverAuth] = useMutation(AUTHENTICATE, {
        fetchPolicy: "no-cache"
    })

    const [getAccessToken] = useMutation(GET_ACCESS_TOKEN, {
        fetchPolicy: "no-cache"
    })

    const authenticate = async (address) => {
        const res = await serverReqAuth({
            variables: {address},
        });

        const sign = await eth.request({
            method: "personal_sign",
            params: [Web3.utils.utf8ToHex(res.data.message), address],
            from: address,
        });

        const rsv = parseSignature(sign);

        const ares = await gqlPost(AUTHENTICATE, {
                address,
                ...rsv
        });
        console.log(ares);
        const gares = await gqlPost(GET_ACCESS_TOKEN, {address: address});
        console.log(gares);
        setAuthCookie(gares.data.token);
        const wx = decodeAuthCookie();
        console.log(wx);
        // window.landlord = wx.role === "landlord"
        setAuthenticated(true);
    }

    const connect = async () => {
        let acc = (await eth.request({method: "eth_requestAccounts"}))[0];
        setAccount(acc);
        setLastAccount(acc);
        await authenticate(acc);
    };

    const checkAccounts = (accounts) => setAccountInvalid(
        accounts.length > 0 && getLastAccount() && getLastAccount() !== accounts[0]
    );

    useEffect(() => eth.request({method: "eth_accounts"}).then(checkAccounts), []);
    eth.on('accountsChanged', checkAccounts)

    return (
        <>
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
        </>
    );
}

export default MetamaskAuth;
