import { default as React, useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import logo from '../assets/logo.png';
import './login.css';


const Login = () => {
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

  const handleHome = () => {
    history.push('/Home'); // Replace '/dashboard' with your desired route
  };

  const redirectToSignup = () => {
    history.push('/signup'); // Replace '/signup' with your signup page route
  };
  useEffect(() => {
    // Perform an action on component mount
    console.log('Login component mounted');
    // You can add any logic you want to execute on component mount here
    // For example, fetching data, initializing variables, etc.
  }, []);
  return (
    <div>
      <div className="navbar">
        <img src={logo} alt="Logo" className="logo" />
      </div>
      <div className="login-form">
        <form>
          <div className='loginheader'>
            <header>
              <h3>Login Form</h3></header>
          </div>
          <div>
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your Email"
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placehold er="Enter your Password"
            />
          </div>
          <button type="button" onClick={handleHome}>
            Login
          </button>
        </form>
        <p>
          Don't have an account? <button onClick={redirectToSignup}>Sign Up</button>
        </p>
      </div>
    </div>
  );
};

export default Login;