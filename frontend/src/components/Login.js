import { useRef, useState, useEffect } from 'react';
/*import AuthContext from "../context/AuthProvider";*/
import loginInfo  from '../serves/login_service';
import { useNavigate } from 'react-router-dom';




const Login = () => {
    /*const { setAuth } = useContext(AuthContext);*/
    const navigate = useNavigate();
    const userRef = useRef();
    const errRef = useRef();

    const [user, setUser] = useState('');
    const [pwd, setPwd] = useState('');
    const [errMsg, setErrMsg] = useState('');
    

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        setErrMsg('');
    }, [user, pwd])

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            loginInfo(
                user,
                pwd).then((response) => {
                if (response.status === 200) {
                    
                    setUser('');
                    setPwd('');
                    navigate('/history');
                } 
                // navigate('/visualize');
              });
           /* const response = await axios.post(LOGIN_URL,
                JSON.stringify({ user, pwd }),
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true
                }
            );
            console.log(JSON.stringify(response?.data));
            //console.log(JSON.stringify(response));
            const accessToken = response?.data?.accessToken;
            const roles = response?.data?.roles;
            setAuth({ user, pwd, roles, accessToken });*/
           
        } catch (err) {
            if (!err?.response) {
                setErrMsg('No Server Response');
            } else if (err.response?.status === 400) {
                setErrMsg('Missing Username or Password');
            } else if (err.response?.status === 401) {
                setErrMsg('Unauthorized');
            } else {
                setErrMsg('Login Failed');
            }
            errRef.current.focus();
        }
    }

    return (
  
       <div >

                <h1 className="appName" >BrainAware</h1>
                 <img src="/images/logo.png" alt="My Image" className="logo" />
                 <img src="/images/image.png" alt="My Image" className="imagee" />
            
                    <h1 className='Title'>Alzheimer Detection Access</h1>
                    <p  className="loginPara">Please fill your detail to access your account.</p>
                    <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
                
                    <form onSubmit={handleSubmit}>
                        <label htmlFor="username" className="loginLabels">Username</label>
                        <input
                            type="text"
                            id="username"
                            placeholder="DrName@example.com"
                            ref={userRef}
                            autoComplete="off"
                            onChange={(e) => setUser(e.target.value)}
                            value={user}
                            required
                        />

                        <label htmlFor="password" className="loginLabels">Password</label>
                        <input
                            type="password"
                            id="password"
                            placeholder="&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;"
                            onChange={(e) => setPwd(e.target.value)}
                            value={pwd}
                            required
                        />
                        <button className='signinButton'><p className='signin'>Sign in</p></button>
                    </form>
                   <p className="forget">Forget Password?</p> 
           
                </div>
    
    )
}

export default Login