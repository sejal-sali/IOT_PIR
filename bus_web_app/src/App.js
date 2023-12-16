// import './App.css';

// function App() {
//   return (
//     <div className="App">
//     </div>
//   );
// }

// export default App;
// App.js
// import { Route, BrowserRouter as Router, Switch } from 'react-router-dom';
// import Buses from './components/Buses';
// import Busseats from './components/Busseats'; // Import the BusSeats component
// import Home from './components/Home';

// const App = () => {
//   const handleCheckBuses = (fromCity, toCity) => {
//     // Logic to handle checking buses with selected cities
//     console.log(`From: ${fromCity}, To: ${toCity}`);
//   };

//   return (
//     <Router>
//       <Switch>
//         <Route exact path="/">
//           <Home handleCheckBuses={handleCheckBuses} />
//         </Route>
//         <Route path="/buses" component={Buses} />
//         <Route path="/seats/:busId" component={Busseats} /> {/* New Route for BusSeats */}

//       </Switch>
//     </Router>
//   );
// };

// export default App;
import { Route, BrowserRouter as Router, Switch } from 'react-router-dom';
import Buses from './components/Buses';
import Busseats from './components/Busseats'; // Updated import for BusSeats
import Home from './components/Home';

const App = () => {
  const handleCheckBuses = (fromCity, toCity) => {
    // Logic to handle checking buses with selected cities
    console.log(`From: ${fromCity}, To: ${toCity}`);
  };

  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <Home handleCheckBuses={handleCheckBuses} />
        </Route>
        <Route exact path="/buses" component={Buses} /> {/* Updated path for Buses */}
        <Route path="/seats/:busId" component={Busseats} /> {/* Updated component for BusSeats */}
      </Switch>
    </Router>
  );
};

export default App;

