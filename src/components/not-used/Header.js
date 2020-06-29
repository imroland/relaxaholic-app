import React, { Component } from 'react'
import { withRouter } from "react-router-dom"

class Header extends Component {
  
  handleNavHome = () => {
    this.props.history.push("/");
  };

  handleNavDirectory = () => {
    this.props.history.push("/motivational-quotes")
  }

  render() {
    return (
      <div>
        <button onClick={this.handleNavHome}>Home</button>
        <button onClick={this.handleNavDirectory}>Motivational Quotes</button>
      </div>
    )
  }
}
export default withRouter(Header);