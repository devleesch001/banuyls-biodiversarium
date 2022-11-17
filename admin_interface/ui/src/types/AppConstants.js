import config from "../../../../appconfig.json"

const BASE_API_URL="http://localhost:"+config["port"]+"/"

const TYPES_ICON = {
    fixed:"tree",
    moving:"fish",
}

const TYPES_COLOR = {
    moving:"#bbfffa",
    fixed:"#ffe28c",
}

function getToken()
{
    return localStorage.getItem("token")
}

function removeToken()
{
    localStorage.removeItem("token")
}

export {BASE_API_URL, TYPES_ICON, TYPES_COLOR, getToken, removeToken}