import { Button } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import logo from '../assets/logo.png'; // Import the SVG file
import './Home.css';

const Home = ({ handleCheckBuses }) => {
  const history = useHistory();
  const [fromCity, setFromCity] = useState('');
  const [toCity, setToCity] = useState('');
  const cities = ['Dublin', 'Dundalk', 'Drogheda'];

  // Auto-refresh on route change
  useEffect(() => {
    const unlisten = history.listen(() => {
      window.location.reload(); // Reload the page when a route change occurs
    });

    return () => {
      unlisten(); // Clean up the listener when the component unmounts
    };
  }, [history]);
  const handleLoginClick = () => {
    history.push('/login'); // Redirect to login page
  };

  const handleSignupClick = () => {
    history.push('/signup'); // Redirect to signup page
  };

  const handleFromCityChange = (event) => {
    const selectedCity = event.target.value;
    setFromCity(selectedCity);
    setToCity('');
  };

  const handleToCityChange = (event) => {
    const selectedCity = event.target.value;
    setToCity(selectedCity);
  };

  const handleCheckButtonClick = () => {
    if (fromCity !== '' && toCity !== '') {
      // Use handleCheckBuses function
      handleCheckBuses(fromCity, toCity);
      history.push(`/buses?from=${fromCity}&to=${toCity}`);
    } else {
      alert('Please select both From and To cities.');
    }
  };

  return (
    <div>
      <div className="navbar">
  <img src={logo} alt="Logo" className="logo" />
</div>

      <div className='container'>
        <h1>View Occupancy</h1>
        <div className='form'>
          <label htmlFor="fromCity">From:</label>
          <select id="fromCity" value={fromCity} onChange={handleFromCityChange}>
            <option value="">Select City</option>
            {cities.map((city) => (
              <option key={city} value={city} disabled={city === toCity}>
                {city}
              </option>
            ))}
          </select>

          <label htmlFor="toCity">To:</label>
          <select id="toCity" value={toCity} onChange={handleToCityChange}>
            <option value="">Select City</option>
            {cities.map((city) => (
              <option key={city} value={city} disabled={city === fromCity}>
                {city}
              </option>
            ))}
          </select>
          <div className='button'>
            <Button variant="outlined" onClick={handleCheckButtonClick}>
              Check Buses
            </Button>
           
          </div>
         

            </div>
        </div>
      </div>
   
  );
};

export default Home;
