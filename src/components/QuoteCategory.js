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
          <MenuItem value={"Advice"}>Advice</MenuItem>
          <MenuItem value={"Humor"}>Humor</MenuItem>
          <MenuItem value={"Inspirational"}>Inspirational</MenuItem>
          <MenuItem value={"Life"}>Life</MenuItem>
          <MenuItem value={"Love"}>Love</MenuItem>
          <MenuItem value={"People"}>People</MenuItem>
          <MenuItem value={"Philosophy"}>Philosophy</MenuItem>
          <MenuItem value={"Wisdom"}>Wisdom</MenuItem>
        </Select>
      </FormControl>
    </Fragment>
  )
}
export default QuoteCategory;