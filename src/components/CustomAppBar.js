import React, { Fragment } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import { withRouter } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

function CustomAppBar(props) {
  const classes = useStyles();
  
  const handleNavHome = () => {
    props.history.push("/");
  };

  const handleNavQuotePage = () => {
    props.history.push("/motivational-quotes");
  }
  return (
    <Fragment>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            Relaxaholic
          </Typography>
          <Typography>
            <Button onClick={handleNavHome} color="inherit">Home</Button>
            <Button onClick={handleNavQuotePage} color="inherit">Motivational Quotes</Button>
          </Typography>
        </Toolbar>
      </AppBar>
    </Fragment>
  );
}

export default withRouter(CustomAppBar);