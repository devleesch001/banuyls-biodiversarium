import config from "../../../appconfig.json"

const BASE_URL=window.location.protocol + "//" + window.location.host+":"+config["port"]+"/"

function setToken(token)
{
    localStorage.setItem("token", token)
}

export { BASE_URL, setToken }