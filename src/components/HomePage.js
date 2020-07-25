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
      randomCategory: "",
      randomIndex: 0
    };
    this.generateRandomizedIndex = this.generateRandomizedIndex.bind(this)
  }

  componentDidMount() {
    fetch('https://api.npoint.io/6e5c60ffd68b29d8a666')
      .then(data => data.json())
      .then(quotesJSON => this.setState({ quotes: quotesJSON }))
      .then(this.generateRandomizedIndex())
  }

  get newQuote() {
    if (this.state.quotes.length === 0) {
      return undefined;
    } else if (this.state.randomCategory.length > 0){
      return this.state.quotes[this.state.randomCategory][this.state.randomIndex]
    } else return undefined
  }

  generateRandomizedIndex() {
    const _ = require("lodash")
    const categories = ['Advice', 'Humor', 'Inspirational',
      'Life', 'Love', 'People', 'Philosophy', 'Wisdom'];
    const oneCategory = _.sample(categories)
    const oneIndex = _.random(oneCategory.length - 1)
    this.setState({
      randomCategory: oneCategory,
      randomIndex: oneIndex
    })
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
              this.newQuote ?
                <QuoteCard
                  description={this.newQuote.quotes_description}
                  author={this.newQuote.quotes_author} /> :
                null
            }
            <Paper>
              <Button id="new-quote" size="small" onClick={this.generateRandomizedIndex}>Generate Another Quote!</Button>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    );
  }
}

export default withStyles(styles)(HomePage);
