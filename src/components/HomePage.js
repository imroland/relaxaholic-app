import React from 'react';
import { random } from 'lodash';
import QuoteCard from './QuoteCard';
import 'typeface-roboto';
import { Grid, withStyles, Button, Typography, Paper, Box } from '@material-ui/core';
import Background from '../media/bg.jpg';

const styles = {
  container: {
    alignItems: 'flex-start',
    display: 'flex',
    marginBottom: '5vh'
  },
  bg: {
    backgroundImage: `url(${Background})`,
    backgroundPosition: 'center',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    width: '100vw',
    height: '100vh',
    paddingTop: '5vh',
    paddingBottom: '5vh'
  }
};

class HomePage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      quotes: [],
      selectedQuoteIndex: null
    };
    this.assignNewQuoteIndex = this.assignNewQuoteIndex.bind(this);
    this.selectQuoteIndex = this.generateNewQuoteIndex.bind(this);
  }

  componentDidMount() {
    fetch('https://gist.githubusercontent.com/awran5/355643af99164a61ae0f95c84206d151/raw/c62636e8eef7e73540fa04b67f753ca9b95ee21e/quotes-api.js')
      .then(data => data.json())
      .then(quotes => this.setState({ quotes }, this.assignNewQuoteIndex));
  }

  get selectedQuote() {
    if (!this.state.quotes.length || !Number.isInteger(this.state.selectedQuoteIndex)) {
      return undefined;
    }
    return this.state.quotes[this.state.selectedQuoteIndex];
  }

  /**
   * Returns an integer representing an index in state.quotes
   * If state.quotes is empty, returns undefined
   */
  generateNewQuoteIndex() {
    if (!this.state.quotes.length) {
      return undefined;
    }
    return random(0, this.state.quotes.length - 1);
  }

  assignNewQuoteIndex() {
    this.setState({ selectedQuoteIndex: this.generateNewQuoteIndex() });
  }

  render() {
    return (
      <Box className={this.props.classes.bg}>
        <Grid className={this.props.classes.container} id="introduction" justify="center" container>
          <Grid xs={10} lg={8} item>
            <Paper style={{ textAlign: "center" }}>
              <Typography>
                <h1>Welcome to the Relaxaholic Website!</h1>
                <p>
                  This is the homepage where you can view the quote of the day.
                  If you would like to view another quote, click on the button
                  below to generate a new one. To view specific quotes by category,
                  click "Motivational Quotes" at the top right of this page.
                </p>
              </Typography>
            </Paper>
          </Grid>
          <Grid xs={10} lg={8} item>
            <Paper style={{ textAlign: "center" }}>
              <Typography>
                <h2>Quote of the Day:</h2>
              </Typography>
            </Paper>
            {
              this.selectedQuote ?
                <QuoteCard selectedQuote={this.selectedQuote} /> :
                null
            }
            <Paper>
              <Button id="new-quote" size="small" onClick={this.assignNewQuoteIndex}>Generate Another Quote!</Button>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    );
  }
}

export default withStyles(styles)(HomePage);
