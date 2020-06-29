import React from 'react'
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter } from '@fortawesome/free-brands-svg-icons';

const QuoteCard = ({ selectedQuote }) => (
  <Card>
    <CardContent>
      <Typography id="text">
        {selectedQuote.quote} - <span id="author">{selectedQuote.author}</span>
      </Typography>
    </CardContent>
    <CardActions>
      <IconButton
        id="tweet-quote"
        target="_blank"
        href={encodeURI(`https://twitter.com/intent/tweet?text=${selectedQuote.quote}`)}
      >
        <FontAwesomeIcon icon={faTwitter}></FontAwesomeIcon>
      </IconButton>
    </CardActions>
  </Card>
);

export default QuoteCard;


