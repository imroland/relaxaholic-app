import React, { Fragment } from 'react';
import HomePage from './components/HomePage';
import QuotesPage from './components/QuotesPage';
import WorkoutPage from './components/WorkoutPage';
import CustomAppBar from './components/CustomAppBar';
import { Switch, Route, BrowserRouter } from 'react-router-dom';

class App extends React.Component {
  render() {
    return (
      <Fragment>
        <BrowserRouter>
          <CustomAppBar />
          <Switch>
            <Route exact path='/' component={HomePage} />
            <Route exact path='/motivational-quotes' component={QuotesPage} />
            <Route exact path ='/workouts' component={WorkoutPage} />
          </Switch>
        </BrowserRouter>
      </Fragment>
    );
  }
}

export default App;