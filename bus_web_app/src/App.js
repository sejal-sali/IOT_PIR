import React, { useState } from 'react';
import BusForm from './components/BusForm';
import BusList from './components/BusList';

const App = () => {
  const [selectedDestinations, setSelectedDestinations] = useState(null);

  const handleFormSubmit = (destinations) => {
    setSelectedDestinations(destinations);
  };

  const getBusList = () => {
    // Fetch bus list based on selected destinations
    // You can use an API or a predefined list
    return [
      { id: 1, name: 'Bus 1', icon: 'bus1.png' },
      { id: 2, name: 'Bus 2', icon: 'bus2.png' },
      // Add more buses as needed
    ];
  };

  return (
    <div>
      <h1>Bus Booking App</h1>

      {!selectedDestinations ? (
        <BusForm onFormSubmit={handleFormSubmit} />
      ) : (
        <BusList buses={getBusList()} />
      )}
    </div>
  );
};

export default App;
