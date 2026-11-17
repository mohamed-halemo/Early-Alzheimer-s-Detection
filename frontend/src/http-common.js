import axios from "axios";
import serverConfig from './server_config.json';

export default axios.create({
  baseURL: serverConfig.server_url+"images",
  headers: {
    "Content-type": "application/json"
  }
});