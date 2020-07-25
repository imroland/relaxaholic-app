import React, { Component } from 'react';
import 'typeface-roboto';
import {
  Grid, withStyles, Box,
  Card, CardContent, CardActions, Typography
} from '@material-ui/core';
import QuoteCategory from './QuoteCategory';
import QuoteCard from './QuoteCard';
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
    backgroundSize: 'auto auto cover',
    backgroundRepeat: 'repeat-y',
    backgroundAttachment: 'fixed',
    paddingTop: '5vh',
    paddingBottom: '5vh'
  }
};

class QuotesPage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      quotesJSON: [],
      chosenCategory: "All"
    }
    this.categorySwitch = this.categorySwitch.bind(this);
  }

  componentDidMount() {
    fetch('https://api.npoint.io/6e5c60ffd68b29d8a666')
      .then(data => data.json())
      .then(quotes => this.setState({ quotesJSON: quotes }))
  }

  categorySwitch = (e) => {
    console.log(e.target.value);
    this.setState({ chosenCategory: e.target.value });
  }

  get selectedQuotes() {
    console.log(this.state.quotesJSON);
    if (this.state.quotesJSON.length === 0) {
      console.log("returning undefined.");
      return undefined;
    } else if (this.state.chosenCategory === "All") {
      console.log("Returning entire JSON")
      return this.state.quotesJSON
    } else {
      function filterObjectByKey(obj, filterFunc) {
        return Object.keys(obj).reduce((newObj, key) => {
          if (filterFunc(key)) {
            newObj[key] = obj[key];
          }
          return newObj;
        }, {});
      }
      console.log("returning workouts only from particular category..")
      return filterObjectByKey(this.state.quotesJSON, x => x === this.state.chosenCategory)
    }
  }

  render() {
    return (
      <Box className={this.props.classes.bg}>
        <Grid className={this.props.classes.container} id="quotes-page-intro" justify="center" container>
          <Grid xs={10} lg={8} item>
            <Card>
              <CardContent>
                <Typography>
                  <h2>Welcome to the Quotes Page!</h2>
                  <h3>Select Your Preferred Category:</h3>
                </Typography>
              </CardContent>
              <CardActions>
                <QuoteCategory handleCategoryChange={this.categorySwitch} />
              </CardActions>
            </Card>
          </Grid>
        </Grid>
        {
          this.selectedQuotes ?
            Object.keys(this.selectedQuotes).map((category, quotes) => {
              return this.selectedQuotes[category].map(quote => (
                <Grid className={this.props.classes.container} id="quote-list" justify="center" container>
                  <Grid xs={10} lg={8} item>
                    <QuoteCard
                      description={quote.quotes_description} 
                      author={quote.quotes_author}/>
                  </Grid>
                </Grid>
              ))
            }) : null
        }
      </Box>
    )
  }
}
export default withStyles(styles)(QuotesPage);