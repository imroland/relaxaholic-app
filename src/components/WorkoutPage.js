import React, { Component } from 'react'
import Background from '../media/bg.jpg';
import WorkoutCategory from './WorkoutCategory'
import WorkoutCard from './WorkoutCard'
import { Grid, withStyles, Box, Card, CardContent, Typography, CardActions } from '@material-ui/core';

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

class WorkoutPage extends Component {

  render() {
    return (
      <Box className={this.props.classes.bg}>
        <Grid className={this.props.classes.container} id="introduction" justify="center" container>
          <Grid xs={10} lg={8} item>
            <Card>
              <CardContent>
                <Typography>
                  <h2>Finding a Workout to do? Wait no more!</h2>
                  <h3>Select your preferred type of workout:</h3>
                </Typography>
              </CardContent>
              <CardActions>
                <WorkoutCategory/>
              </CardActions>
            </Card>
          </Grid>
        </Grid>

        <Grid className={this.props.classes.container} id="introduction" justify="center" container>
          <Grid xs={10} lg={8} spacing={2} container>
            <WorkoutCard name="1 Leg Pushup" firstImage="https://www.jefit.com/images/exercises/800_600/4212.jpg"
            secondImage="https://www.jefit.com/images/exercises/800_600/4213.jpg"/>
            <WorkoutCard name="90 90 Hamstring" firstImage="https://www.jefit.com/images/exercises/800_600/1860.jpg"
            secondImage="https://www.jefit.com/images/exercises/800_600/1861.jpg"/>
            <WorkoutCard name="Ab Crunch Machine" firstImage="https://www.jefit.com/images/exercises/800_600/224.jpg"
            secondImage="https://www.jefit.com/images/exercises/800_600/225.jpg"/>
          </Grid>
        </Grid>
        {/* map workout card here */}
      </Box>
    )
  }
}

export default withStyles(styles)(WorkoutPage)
