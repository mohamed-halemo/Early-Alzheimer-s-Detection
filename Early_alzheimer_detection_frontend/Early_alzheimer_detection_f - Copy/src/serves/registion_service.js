import axios from "axios";
import serverConfig from '../server_config.json';

/**
 * This function is used to post the username & password
 * to the backend
 * @param {object} props  list of username & password
 * @returns response
 */
export default async function registionInfo(user, pwd) {
  let response = '';
  try {
    response = await axios.post(`${serverConfig.server_url}/register`, {
        user, pwd,
    }, {
      headers: {
        'content-type': 'application/json',
      },
    });
    // Success
    // console.log(response);
    return (response);
  } catch (error) {
    if (error.response) {
      /*
          * The request was made and the server responded with a
          * status code that falls out of the range of 2xx
          */
    
      return (error.response);
    } if (error.request) {
      /*
          * The request was made but no response was received, `error.request`
          * is an instance of XMLHttpRequest in the browser and an instance
          * of http.ClientRequest in Node.js
          */

    } else {
      // Something happened in setting up the request and triggered an Error
    
    }
    // console.log(error);
    return (response);
  }
}