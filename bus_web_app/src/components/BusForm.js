import React, { useState } from 'react';

const BusForm = ({ onFormSubmit }) => {
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');

  const handleCheck = () => {
    // Pass the selected 'from' and 'to' to the parent component
    onFormSubmit({ from, to });
  };

  return (
    <div>
      <label>
        From:
        <select value={from} onChange={(e) => setFrom(e.target.value)}>
          {/* Populate 'from' destinations */}
          <option value="cityA">City A</option>
          <option value="cityB">City B</option>
          {/* Add more options as needed */}
        </select>
      </label>

      <label>
        To:
        <select value={to} onChange={(e) => setTo(e.target.value)}>
          {/* Populate 'to' destinations */}
          <option value="cityX">City X</option>
          <option value="cityY">City Y</option>
          {/* Add more options as needed */}
        </select>
      </label>

      <button onClick={handleCheck}>Check</button>
    </div>
  );
};

export default BusForm;
