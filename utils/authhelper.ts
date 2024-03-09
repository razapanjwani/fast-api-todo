import { getCookies, setCookie, deleteCookie, getCookie, hasCookie } from 'cookies-next';

export const myGetCookie = async () => {
    return getCookies()
}

export const mySetCookie = async (token, refresh_token) => {
    const now = new Date();
    const expirationTime = new Date(now.getTime() + 60 * 60 * 1000)
    if (hasCookie("access_token")) {
        console.log("token exist");
    } else {
        setCookie("access_token", token, { expires: expirationTime })
        setCookie("refresh_token", refresh_token, { expires: expirationTime })
    }
}

export const myDelCookie = async () => {
    if (hasCookie("access_token") || hasCookie("refresh_token")) {
        deleteCookie("access_token")
        deleteCookie("refresh_token")
    }
}

