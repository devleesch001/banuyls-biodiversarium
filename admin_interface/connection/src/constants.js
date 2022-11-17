import config from "../../../appconfig.json"

const BASE_URL="http://localhost:"+config["port"]+"/"

function setToken(token)
{
    localStorage.setItem("token", token)
}

export { BASE_URL, setToken }