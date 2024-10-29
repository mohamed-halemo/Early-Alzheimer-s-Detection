import axios from "axios";
import serverConfig from '../server_config.json';

export default async function loginInfo(user, pwd) {
    let response = '';
    try {
      response = await axios.post(serverConfig.server_url+'users/login', 
      {
        headers: {
          'content-type': 'application/json',
        },
        email:  user,
        password: pwd
      });
  
      // console.log(response)
      localStorage.removeItem('token')
      localStorage.setItem('token', response.data.tokens);
      // console.log(localStorage);
      return (response);
    } catch (error) {
      if (error.response) {
        /*
            * The request was made and the server responded with a
            * status code that falls out of the range of 2xx
            */
          // console.log(error.response.data);
          // console.log(error.response.status);
          // console.log(error.response.headers);
        return (error.response);
      } if (error.request) {
        /*
            * The request was made but no response was received, `error.request`
            * is an instance of XMLHttpRequest in the browser and an instance
            * of http.ClientRequest in Node.js
            */
        // console.log(error.request);
      } else {
        // Something happened in setting up the request and triggered an Error
        // console.log('Error', error.message);
      }
      // console.log(error);
      return (response);
    }
  }