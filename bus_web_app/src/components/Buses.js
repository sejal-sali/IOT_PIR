import { Button, Card, CardContent, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import logo from '../assets/logo.png'; // Import the SVG file
import './Home.css';

const Buses = () => {
  const location = useLocation();
  const history = useHistory();
  const [filteredBuses, setFilteredBuses] = useState([]);

  const busDetails = [
    { id: 1, source: 'Dublin', destination: 'Dundalk', time: '9:00 AM'},
    { id: 2, source: 'Dundalk', destination: 'Dublin', time: '10:30 AM'},
    { id: 3, source: 'Drogheda', destination: 'Dublin', time: '11:00 AM'},
    { id: 4, source: 'Dublin', destination: 'Drogheda', time: '1:00 PM'},
    { id: 5, source: 'Drogheda', destination: 'Dundalk', time: '3:30 PM'},
    { id: 6, source: 'Dundalk', destination: 'Drogheda', time: '5:00 PM'},
    { id: 7, source: 'Dundalk', destination: 'Drogheda', time: '6:00 PM'},
  ];

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const fromCity = params.get('from');
    const toCity = params.get('to');

    if (fromCity && toCity) {
      const filtered = busDetails.filter(bus => bus.source === fromCity && bus.destination === toCity);
      setFilteredBuses(filtered);
    } else {
    }
  }, [location.search, busDetails]);

  useEffect(() => {
    const unlisten = history.listen(() => {
      window.location.reload();
    });

    return () => {
      unlisten();
    };
  }, [history]);

  // const handleViewSeats = (busId) => {
  //   console.log(`View seats for Bus ID: ${busId}`);
  //   history.push(`/seats/${busId}`);
  // };
  const handleViewSeats = (busId) => {
    console.log(`View seats for Bus ID: ${busId}`);
    history.push(`/seats/${busId}`);
  };


  return (
    <div>
      <div className="navbar">
      <img src={logo} alt="Logo" className="logo" />
      </div>

      <div className="bus-cards-container">
        {filteredBuses.map((bus) => (
          <Card key={bus.id} className="bus-card">
            <CardContent>
              <Typography variant="h6">{bus.travelName}</Typography>
              <Typography variant="subtitle1">{bus.source} to {bus.destination}</Typography>
              <Typography variant="body2">Time: {bus.time}</Typography>
              <Button variant="outlined" onClick={() => handleViewSeats(bus.id)}>View Seats</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Buses;
