
import { Redirect, Route, BrowserRouter as Router, Switch } from 'react-router-dom';
import Buses from './components/Buses';
import Busseats from './components/Busseats';
import Home from './components/Home';
import login from './components/login'; // Updated import with correct casing
import signup from './components/signup';

const App = () => {
  const handleCheckBuses = (fromCity, toCity) => {
    // Logic to handle checking buses with selected cities
    console.log(`From: ${fromCity}, To: ${toCity}`);
  };

  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <Redirect to="/login" />
        </Route>
        <Route exact path="/login" component={login} />
        <Route path="/signup" component={signup} />
        <Route path="/home">
          <Home handleCheckBuses={handleCheckBuses} />
        </Route>
        <Route exact path="/buses" component={Buses} />
        <Route path="/seats/:busId" component={Busseats} />
      </Switch>
    </Router>
  );
};

export default App;
