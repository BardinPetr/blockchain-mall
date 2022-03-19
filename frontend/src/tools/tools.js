import Cookies from "js-cookie";
import { decode } from "jsonwebtoken";
import axios from "axios";
import { print } from "graphql";

export function parseSignature(signature) {
  if (signature.length > 130) signature = signature.substring(2, 132);
  return {
    r: "0x" + signature.substring(0, 64),
    s: "0x" + signature.substring(64, 128),
    v: parseInt(signature.substring(128, 130), 16).toString(),
  };
}

export const getLastAccount = () => localStorage.getItem("lastAccount");
export const setLastAccount = (account) =>
  localStorage.setItem("lastAccount", account);

export const getAccount = () => localStorage.getItem("account");
export const setAccount = (account) => localStorage.setItem("account", account);

export const setAuthCookie = (jwt) => Cookies.set("access_token_cookie", jwt);
export const getAuthCookie = () => Cookies.get("access_token_cookie");
export const decodeAuthCookie = () => {
  console.log("decodeAuthCookie cookie", getAuthCookie());
  return decode(getAuthCookie());
};

export const isLandlord = () => decodeAuthCookie().role === "landlord";
export const getAddress = () => decodeAuthCookie().address;

export const DEBUG = false;
export const BASE_URL = `${
  DEBUG ? "http://0.0.0.0:8089" : window.location.origin
}/graphql`;

export async function gqlPost(query, variables) {
  console.log("gqlPost cookie", getAuthCookie());
  const response = await axios.post(
    BASE_URL,
    {
      query: print(query),
      variables: variables,
    },
    {
      withCredentials: true,
      headers: {
        authorization: getAuthCookie(),
      },
    }
  );
  return response.data;
}
