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

  constructor(props) {
    super(props);
    this.state = {
      workoutJSON: [],
      chosenCategory: "All"
    }
    // this.categorySwitch = this.categorySwitch.bind(this);
  }

  componentDidMount() {
    fetch('https://api.npoint.io/62d119bbae2ebb1f8cf3')
      .then(data => data.json())
      .then(workouts => {
        this.setState({
          workoutJSON: workouts
        })
      })
  }

  categorySwitch = (e) => {
    console.log(e.target.value);
    this.setState({ chosenCategory: e.target.value });
  }

  get selectedWorkouts() {
    console.log(this.state.workoutJSON)
    if (this.state.workoutJSON.length === 0) {
      return undefined
    } else if (this.state.chosenCategory === "All") {
      console.log("Returning entire JSON")
      return this.state.workoutJSON
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
      return filterObjectByKey(this.state.workoutJSON, x => x === this.state.chosenCategory)
    }
  }

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
                <WorkoutCategory handleCategoryChange={this.categorySwitch} />
              </CardActions>
            </Card>
          </Grid>
        </Grid>

        <Grid className={this.props.classes.container}
           id="introduction" justify="center" container>
          <Grid xs={10} lg={8} spacing={2} justify="center" container>
            {
              this.selectedWorkouts
                ?
                Object.keys(this.selectedWorkouts).map((category, workouts) => {
                  return this.selectedWorkouts[category].map(workout => (
                    <WorkoutCard
                      name={workout.workout_name}
                      firstImage={workout.image_link_1}
                      secondImage={workout.image_link_2} />

                  ))
                })
                : null
            }

          </Grid>
        </Grid>
      </Box>
    )
  }
}

export default withStyles(styles)(WorkoutPage)
//   < WorkoutCard name = "1 Leg Pushup" firstImage = "https://www.jefit.com/images/exercises/800_600/4212.jpg"
// secondImage = "https://www.jefit.com/images/exercises/800_600/4213.jpg" />
//   <WorkoutCard name="90 90 Hamstring" firstImage="https://www.jefit.com/images/exercises/800_600/1860.jpg"
//     secondImage="https://www.jefit.com/images/exercises/800_600/1861.jpg" />
//   <WorkoutCard name="Ab Crunch Machine" firstImage="https://www.jefit.com/images/exercises/800_600/224.jpg"
//     secondImage="https://www.jefit.com/images/exercises/800_600/225.jpg" />