import React, { useEffect, useState } from 'react';

const SeatLayoutFromDb = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Function to fetch data from the API
    const fetchData = async () => {
      try {
        // Make an API call using fetch
        const response = await fetch('https://bored-cod-tux.cyclic.app/api/data');
        
        // Check if the response is successful
        if (response.ok) {
          // Convert the response to JSON
          const result = await response.json();
          
          // Set the retrieved data in state
          setData(result);
        } else {
          // Handle error if API call fails
          throw new Error('Failed to fetch data');
        }
      } catch (error) {
        console.error(error);
        // Handle errors appropriately (e.g., show error message)
      }
    };

    // Call the fetchData function
    fetchData();
  }, []); // Empty dependency array ensures useEffect runs only once

  return (
    <div>
      {data ? (
        // Display fetched data
        <div>{JSON.stringify(data)}</div>
      ) : (
        // Display a loading message or spinner while data is being fetched
        <div>Loading...</div>
      )}
    </div>
  );
};

export default SeatLayoutFromDb;
