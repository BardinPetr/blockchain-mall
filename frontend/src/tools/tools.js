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