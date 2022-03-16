import Cookies from 'js-cookie'
import {decode} from "jsonwebtoken";

export function parseSignature(signature) {
    if (signature.length > 130) signature = signature.substring(2, 132);
    return {
        r: "0x" + signature.substring(0, 64),
        s: "0x" + signature.substring(64, 128),
        v: parseInt(signature.substring(128, 130), 16).toString(),
    };
}

export const getLastAccount = () => localStorage.getItem("lastAccount");
export const setLastAccount = (account) => localStorage.setItem("lastAccount", account);

export const setAuthCookie = (jwt) => Cookies.set('access_token_cookie', jwt);
export const getAuthCookie = () => Cookies.get('access_token_cookie');
export const decodeAuthCookie = () => decode(getAuthCookie());
