import { default as React, useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import logo from '../assets/logo.png';
import './login.css';

const Login = () => {
  const [name, setname] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const history = useHistory();

  useEffect(() => {
    const unlisten = history.listen(() => {
      window.location.reload();
    });

    return () => {
      unlisten();
    };
  }, [history]);
  const handleLogin = () => {
    history.push('/dashboard'); // Replace '/dashboard' with your desired route
  };

  const redirectToLogin = () => {
    history.push('/login'); // Replace '/signup' with your signup page route
  };

  return (
    <div>
 <div className="navbar">
      <img src={logo} alt="Logo" className="logo" />
      </div>
      
        <div className="login-form">
        <form>
        <div className='loginheader'>
            <header>
              <h3>Signup Form</h3></header>
          </div>
        <div>
            <label>Name:</label>
            <input
              type="Name"
              value={name}
              onChange={(e) => setname(e.target.value)}
              placeholder="Enter your Name"
            />
          </div>
          <div>
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
            />
          </div>
          <button type="button" onClick={handleLogin}>
            Signup Here
          </button>
        </form>
        <p>
          You Already have an account 
          <button onClick={redirectToLogin}>Login</button>
        
        </p>
      </div>
    </div>
  );
};

export default Login;