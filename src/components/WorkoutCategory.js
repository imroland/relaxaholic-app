import React, { Fragment } from 'react'
import { FormControl, InputLabel, Select, MenuItem} from '@material-ui/core';

const QuoteCategory = ({ handleCategoryChange }) => {
  return (
    <Fragment>
      <FormControl >
        <InputLabel shrink id="category-label">
          Category
            </InputLabel>
        <Select
          labelId="category-label"
          id="category-select-label"
          defaultValue={"All"}
          onChange={handleCategoryChange}
          displayEmpty
        >
          <MenuItem value={"All"}>All</MenuItem>
          <MenuItem value="Abs">Abs</MenuItem>
          <MenuItem value={"Back"}>Back</MenuItem>
          <MenuItem value={"Biceps"}>Biceps</MenuItem>
          <MenuItem value={"Chest"}>Chest</MenuItem>
          <MenuItem value={"Forearm"}>Forearm</MenuItem>
          <MenuItem value={"Glutes"}>Glutes</MenuItem>
          <MenuItem value={"Lower Legs"}>Lower Legs</MenuItem>
          <MenuItem value={"Shoulders"}>Shoulders</MenuItem>
          <MenuItem value={"Triceps"}>Triceps</MenuItem>
        </Select>
      </FormControl>
    </Fragment>
  )
}
export default QuoteCategory;