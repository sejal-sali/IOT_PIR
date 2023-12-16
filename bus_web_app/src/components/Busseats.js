import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import React, { useEffect, useState } from "react";
import logo from "../assets/logo.png";
import "./Home.css";

const SeatSVG_Gray = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    enableBackground="new 0 0 24 24"
    height="24"
    viewBox="0 0 24 24"
    width="24"
    style={{ transform: "rotate(180deg)" }}
  >
    <path d="M4,18v3h3v-3h10v3h3v-6H4V18z M19,10h3v3h-3V10z M2,10h3v3H2V10z M17,13H7V5c0-1.1,0.9-2,2-2h6c1.1,0,2,0.9,2,2V13z" fill="#999999" />
  </svg>

);

const SeatSVG_Green = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    enableBackground="new 0 0 24 24"
    height="24"
    viewBox="0 0 24 24"
    width="24"
    style={{ transform: "rotate(180deg)" }}
  >
    <path d="M4,18v3h3v-3h10v3h3v-6H4V18z M19,10h3v3h-3V10z M2,10h3v3H2V10z M17,13H7V5c0-1.1,0.9-2,2-2h6c1.1,0,2,0.9,2,2V13z" fill="#00ff00" />
  </svg>


);
const SeatSVG_White = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    enableBackground="new 0 0 24 24"
    height="24"
    viewBox="0 0 24 24"
    width="24"
    style={{ transform: "rotate(180deg)" }}
  >
    <path d="M4,18v3h3v-3h10v3h3v-6H4V18z M19,10h3v3h-3V10z M2,10h3v3H2V10z M17,13H7V5c0-1.1,0.9-2,2-2h6c1.1,0,2,0.9,2,2V13z" fill="#ffffff" />
  </svg>


);

const BusSeats = () => {
  const [data, setData] = useState([]);
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("https://bored-cod-tux.cyclic.app/api/data");
      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }
      const fetchedData = await response.json();
      // Convert JSON string to JavaScript object
      const data = JSON.parse(JSON.stringify(fetchedData));

      // Create an object to store the highest time for each seat
      const seatTimeMap = {};

      // Iterate through the data to find the highest time for each seat
      data.forEach(item => {
        const seatNum = item.seat_num;
        const currentTime = item.time;

        if (!seatTimeMap[seatNum] || currentTime > seatTimeMap[seatNum]) {
          seatTimeMap[seatNum] = currentTime;
        }
      });

      // Use the seatTimeMap to filter the data
      const filteredResult = Object.keys(seatTimeMap).map(seatNum => {
        const highestTime = seatTimeMap[seatNum];
        return data.find(item => item.seat_num === seatNum && item.time === highestTime);
      });
      setData(filteredResult); // Update state with fetched data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  return (
    <div className="center-content">
      <div className="navbar">
        <img src={logo} alt="Logo" className="logo" />
      </div>
      <Card>
        <CardContent>
          <div className="abc">
            {/* <div className="bus-seats-container">{renderSeats(data)}</div> */}
            <SeatLayout seatData={data} />
            <div className="indicators">
              <div className="indicator">
                <div className="seat occupied"></div>
                <span>Occupied Seat</span>
              </div>
              <div className="indicator">
                <div className="seat empty"></div>
                <span>Empty Seat</span>
              </div>
            </div>
          </div>

        </CardContent>
      </Card>
    </div>
  );
};
const data = [
  [null, null, null, 1, 2],
  [3, 4, null, 5, 6],
  [7, 8, null, 9, 10],
  [11, 12, null, 13, 14],
  [15, 16, null, 17, 18],
  [19, 20, null, 21, 22],
  [23, 24, null, 25, 26],
  [27, 28, null, 29, 30],
  [31, 32, null, 33, 34],
  [35, 36, null, 37, 38],
  [39, 40, 41, 42, 43]
];

const SeatLayout = ({ seatData }) => (
  <div>
    {data.map((row, rowIndex) => {
      if (seatData !== null && seatData.length !== 0) {
        return (
          <div key={rowIndex} style={{ display: 'flex' }}>
            {row.map((cell, cellIndex) => {
              if (cell !== null) {
                var element = null;
                seatData.forEach(item => {
                  if (parseInt(item.seat_num) === cell) {
                    element = item;
                  }
                });

                return (

                  <div
                    key={cellIndex}
                    style={{
                      width: '50px', // Adjust the width as needed
                      height: '50px', // Adjust the height as needed
                      boxSizing: 'border-box',
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center'
                    }}
                  >
                    {
                      element !== null && element.value === 0 ? <SeatSVG_Green /> : <SeatSVG_Gray />
                    }
                  </div>
                );
              } else {
                return (<div
                  key={cellIndex}
                  style={{
                    width: '50px', // Adjust the width as needed
                    height: '50px', // Adjust the height as needed
                    boxSizing: 'border-box',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center'
                  }}
                >
                  <SeatSVG_White />
                </div>);
              }

            })}
          </div>
        );
      }
    }
    )}
  </div>
);

export default BusSeats;
