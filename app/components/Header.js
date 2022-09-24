import React from 'react'
import NavBar from '@components/navbar.js'

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'flex-end',
    alignItems: 'center',
    padding: 16,
  },
  versionsContainer: {
    marginLeft: 0,
    marginRight: 'auto',
  },
  button: {
    marginLeft: 16,
    cursor: 'pointer',
  },
}

const Header = () => {
    return(
      <>
        <NavBar></NavBar>
      </>
      
    );   
}

// Note that this is a higher-order function.
export default Header;