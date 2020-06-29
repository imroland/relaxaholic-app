import React, { Component } from 'react';
import 'typeface-roboto';
import { Grid, withStyles, Box } from '@material-ui/core';
import CategorySelect from './CategorySelect';
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
      quotesArrayCatergorized: [],
      selectedCategoryIndex: 0,
    }
    this.categorySwitch = this.categorySwitch.bind(this);
  }

  componentDidMount() {
    fetch('https://gist.githubusercontent.com/awran5/355643af99164a61ae0f95c84206d151/raw/c62636e8eef7e73540fa04b67f753ca9b95ee21e/quotes-api.js')
      .then(data => data.json())
      .then(quotesJSON => this.processQuotes(quotesJSON));
  }

  processQuotes = (quotes) => {
    const advice = quotes.filter(q => q.topics.includes("Advice"));
    const humor = quotes.filter(q => q.topics.includes("Humor"));
    const inspirational = quotes.filter(q => q.topics.includes("Inspirational"));
    const life = quotes.filter(q => q.topics.includes("Life"));
    const love = quotes.filter(q => q.topics.includes("Love"));
    const people = quotes.filter(q => q.topics.includes("People"));
    const philosophy = quotes.filter(q => q.topics.includes("Philosophy"));
    const religion = quotes.filter(q => q.topics.includes("Religion"));
    const wisdom = quotes.filter(q => q.topics.includes("Wisdom"));

    this.setState({
      quotesArrayCatergorized: [
        quotes, advice, humor, inspirational,
        life, love, people, philosophy, religion, wisdom
      ]
    });
  }

  categorySwitch = (e) => {
    console.log(e.target.value);
    this.setState({ selectedCategoryIndex: e.target.value });
  }

  get selectedQuoteCategory() {
    console.log(this.state.quotesArrayCatergorized);
    if (this.state.quotesArrayCatergorized.length === 0) {
      console.log("returning undefined.");
      return undefined;
    } else {
      console.log("returning array of quotes.")
      console.log(this.state.quotesArrayCatergorized[this.state.selectedCategoryIndex]);
      return this.state.quotesArrayCatergorized[this.state.selectedCategoryIndex];
    }
  }

  render() {
    return (
      <Box className={this.props.classes.bg}>
        <Grid className={this.props.classes.container} id="quotes-page-intro" justify="center" container>
          <Grid xs={10} lg={8} item>
            <CategorySelect handleCategoryChange={this.categorySwitch} />
          </Grid>
        </Grid>
        {
        
        this.selectedQuoteCategory ?
          this.selectedQuoteCategory.map(
            quote => (
              <Grid className={this.props.classes.container} id="quote-list" justify="center" container>
                <Grid xs={10} lg={8} item>
                  <QuoteCard selectedQuote={quote} />
                </Grid>
              </Grid>
            )
          ) : null
        }
      </Box>
    )
  }
}
export default withStyles(styles)(QuotesPage);