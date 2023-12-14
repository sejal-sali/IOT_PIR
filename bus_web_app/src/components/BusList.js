import React from 'react';

const BusList = ({ buses }) => {
  return (
    <div>
      <h2>Bus List</h2>
      <ul>
        {buses.map((bus) => (
          <li key={bus.id}>
            <img src={bus.icon} alt="Bus Icon" />
            <p>{bus.name}</p>
            {/* Display other basic info */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BusList;
