import React, { Fragment } from 'react'
import {
  Typography, Card, CardContent,
  CardActions, FormControl, InputLabel, Select,
  MenuItem
} from '@material-ui/core';

const CategorySelect = ({ handleCategoryChange }) => {
  return (
    <Fragment>
      <Card>
        <CardContent>
          <Typography>
            <h3>Select Your Preferred Quote Category:</h3>
          </Typography>
        </CardContent>
        <CardActions>
          <FormControl >
            <InputLabel shrink id="category-label">
              Category
            </InputLabel>
            <Select
              labelId="category-label"
              id="category-select-label"
              defaultValue={0}
              onChange={handleCategoryChange}
              displayEmpty
            >
              <MenuItem value={0}>All</MenuItem>
              <MenuItem value={1}>Advice</MenuItem>
              <MenuItem value={2}>Humor</MenuItem>
              <MenuItem value={3}>Inspirational</MenuItem>
              <MenuItem value={4}>Life</MenuItem>
              <MenuItem value={5}>Love</MenuItem>
              <MenuItem value={6}>People</MenuItem>
              <MenuItem value={7}>Philosophy</MenuItem>
              <MenuItem value={8}>Religion</MenuItem>
              <MenuItem value={9}>Wisdom</MenuItem>
            </Select>
          </FormControl>
        </CardActions>
      </Card>
    </Fragment>
  )
}
export default CategorySelect;