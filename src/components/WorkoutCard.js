import React from 'react'
import {
  Card, CardContent, CardMedia, Typography,
  withStyles, Box, Grid
} from '@material-ui/core'

const styles = {
  img: {
  }
}

const WorkoutCard = (workout) => (
  <Grid xs={10} lg={4} item>
    <Card>
      <CardContent>
        <Typography>
          {workout.name}
        </Typography>
        <Box display="flex" flexWrap="wrap">
          <CardMedia className={workout.classes.img}
            component="img" src={workout.firstImage}
          />
          <CardMedia className={workout.classes.img}
            component="img" src={workout.secondImage}
          />
        </Box>
      </CardContent>
    </Card>
  </Grid>
)
export default withStyles(styles)(WorkoutCard);