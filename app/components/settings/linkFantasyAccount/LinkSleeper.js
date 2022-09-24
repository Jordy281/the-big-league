import React from "react";

import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';

import Button from '@mui/material/Button';
import PropTypes from 'prop-types';
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";

import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import IconButton from '@mui/material/IconButton';
import OutlinedInput from '@mui/material/OutlinedInput';
import FormHelperText from '@mui/material/FormHelperText';
import { Divider } from "@mui/material";

import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import Typography from "@mui/material/Typography";


export default function LinkSleeper(props) {

  const [formValues, setFormValues] = React.useState({}); 
  const [activeStep, setActiveStep] = React.useState(0);
  const [account, setAccount] = React.useState({}); 
  const [isLoading, setLoading] = React.useState(false);
  const [notFoundMessage, setNotFoundMessage] = React.useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormValues({
    ...formValues,
    [name]: value,
    });
  };

  const handleBack = () => {
    setAccount({});
    setNotFoundMessage(false);
    setActiveStep(activeStep-1);
    
  };

  const handleClose = () => {
    props.onClose(account);
    setFormValues({});
    setActiveStep(0);
    setAccount({});
    setNotFoundMessage(false);
    
  };

  const linkId = async () => {
    // this is where we should pull in data from host API
    const username = "Demo"

    var acc = {}
    await fetch("https://api.sleeper.app/v1/user/"+formValues.id)
      .then((res) => res.json())
      .then((data) => {
        acc = data;
    })
    
    //If successfully linked
    if (acc == null){
      setFormValues({
        ...formValues,
        ['username']: "",
        ['leagues']: []

      });
      setNotFoundMessage(true);
    }else if (acc.user_id == null){
      setFormValues({
        ...formValues,
        ['username']: "",
        ['leagues']: []
      });
      setNotFoundMessage(true);
    }else {
      var leagues = []
      await fetch("https://api.sleeper.app/v1/user/"+acc.user_id+"/leagues/nfl/202")
        .then((res) => res.json())
        .then((data) => {
          leagues = data;
          setLoading(false);
          console.log(leagues)
      })
      setFormValues({
        ...formValues,
        ['username']: acc.username,
        ['leagues']: leagues
      });
      setAccount(acc);
      setActiveStep(activeStep+1);
      setNotFoundMessage(false);
    }
  };

  return (
    <Dialog onClose={handleClose} open={props.open}>
      <DialogTitle>Link Sleeper Account</DialogTitle>
      { activeStep == 0 && 
        <Box>
        <DialogContent>
          <Box>
            <Grid container>
              
              <Grid item>
                { activeStep == 0 && 
                  <FormControl variant="outlined">
                    <InputLabel htmlFor='outlined-adornment-userid'>User ID:</InputLabel>
                    <OutlinedInput
                        required
                        type='text'
                        id="outlined-adornment-userid"
                        name="id"
                        value={formValues.id}
                        onChange={handleInputChange}
                        label="Username"
                    />
                    {
                      notFoundMessage && <FormHelperText id="component-error-text" error={true}>Account Not Found</FormHelperText>
                    }
                  </FormControl>
                }
              </Grid>

            </Grid>

          </Box>
          
        </DialogContent>
        <DialogActions>
            <Button autoFocus onClick={handleClose}>
                Cancel
            </Button>
            <Button autoFocus onClick={linkId}>
                Link
            </Button>
        </DialogActions>
        </Box>  
      }
      { (activeStep == 1) && 
        <Box>
        <DialogContent>
          <Box>
            <Grid container>
              
              <Grid item>
                  <FormControl variant="outlined">
                    <InputLabel htmlFor='outlined-adornment-username'>Is This You?</InputLabel>
                    <OutlinedInput
                        required
                        type='text'
                        id="outlined-adornment-username"
                        name="username"
                        value={formValues.username}
                        disabled={true}
                        label="Username"
                    />
                  </FormControl>
              </Grid>
              <Divider variant="middle"></Divider>
              <Typography variant="h6" gutterBottom>
                  Leagues Associated with the Account
              </Typography>
              <List>
              {
                formValues.leagues.map(
                    (league, index) => {
                      <ListItem 
                        secondaryAction={
                          <IconButton edge="end" aria-label="delete" onClick={handleDelete}>
                              <DeleteIcon />
                          </IconButton>
                      }>
                        <ListItemAvatar>
                        <Avatar src={"https://sleepercdn.com/avatars/thumbs/"+league.avatar}/>
                        </ListItemAvatar>
                        <ListItemText primary={league.name}/>
                      </ListItem>
                })
              }


              </List>
              

            </Grid>

          </Box>
          
        </DialogContent>
        <DialogActions>
            <Button autoFocus onClick={handleBack}>
                Back
            </Button>
            <Button autoFocus onClick={handleClose}>
                It's Me!
            </Button>
        </DialogActions>
        </Box>  
      }
      {
         (activeStep == 2) &&
         <Box>
          <DialogContent>
            <Box>
              <Grid container>
                
                <Grid item>
                    <FormControl variant="outlined">
                      <InputLabel htmlFor='outlined-adornment-username'>Is This You?</InputLabel>
                      <OutlinedInput
                          required
                          type='text'
                          id="outlined-adornment-username"
                          name="username"
                          value={formValues.username}
                          disabled={true}
                          label="Username"
                      />
                    </FormControl>
                </Grid>

              </Grid>

            </Box>
          </DialogContent>
          <DialogActions>
              <Button autoFocus onClick={handleBack}>
                  Back
              </Button>
              <Button autoFocus onClick={handleClose}>
                  It's Me!
              </Button>
          </DialogActions>

         </Box>
      }
      
    </Dialog>
  );
}
  
  LinkSleeper.propTypes = {
    onClose: PropTypes.func.isRequired,
    open: PropTypes.bool.isRequired,
  };