import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { useState } from 'react';
import logo from '../assets/logo.svg';
import './Home.css';

const Busseats = () => {
  const totalSeats = 40;
  const seatsPerRow = 4;
  const rows = totalSeats / seatsPerRow;
  const [selectedSeats, setSelectedSeats] = useState([]);

  const handleSeatClick = (seatNumber) => {
    if (selectedSeats.includes(seatNumber)) {
      setSelectedSeats(selectedSeats.filter((seat) => seat !== seatNumber));
    } else {
      setSelectedSeats([...selectedSeats, seatNumber]);
    }
  };

  const renderSeats = () => {
    const seats = [];
    for (let i = 1; i <= totalSeats; i++) {
      const isSelected = selectedSeats.includes(i);
      const className = isSelected ? 'selected' : '';
      seats.push(
        <div key={i} className={`seat ${className}`} onClick={() => handleSeatClick(i)}>
          {i}
        </div>
      );
    }
    return seats;
  };

  return (
    <div>
      <div className="navbar">
      <img src={logo} alt="Logo" width="200" height="50" />

      </div>

      <div className="bus-seats-container">
        <Card className="bus-seats-card">
          <CardContent>
            <Typography variant="h5" component="h2">
              Bus Seats
            </Typography>
            <div className="seats-layout">{renderSeats()}</div>
            <div className="indicators">
              <div className="indicator">
                <div className="seat empty"></div>
                <span>Empty Seat</span>
              </div>
              <div className="indicator">
                <div className="seat reserved"></div>
                <span>Reserved Seat</span>
              </div>
              <div className="indicator">
                <div className="seat selected"></div>
                <span>Selected Seat</span>
              </div>
            </div>
            <div className="selected-count">
              <p>Selected Seats: {selectedSeats.length}</p>
              <p>Selected Seat Numbers: {selectedSeats.join(', ')}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Busseats;
