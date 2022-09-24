import * as React from 'react';

import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';

import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import OutlinedInput from '@mui/material/OutlinedInput';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';


export default function LinkEmails(props) {


    const handleLeagueChange = (index, field, e) => {
        if (typeof(e) != 'undefined'){
            const { name, value } = e.target;
            console.log("Field: " + field + "\tValue: "+ value +"\tIndex: " + index)
            console.log(e.target)
            props.onChange(field, value, index);
        }
    };

    return (
        <React.Fragment>
            <Box spacing={3} sx={{ my: 3, mx: 2 }}>
                <Box sx={{ m: 2 }}>
                    <Typography variant="h6" gutterBottom>
                        Link Emails to Teams
                    </Typography>
                    <Typography gutterBottom>
                        This is required if other people in your league want to use our services.
                    </Typography>
                </Box>
                
                <Divider variant="middle">
                </Divider>
                <Grid container xs={12} sx={{ m: 2 }} spacing={3}>
                    {
                        props.league.teams.map(
                            (team, index) => {
                                return (
                                    <React.Fragment>
                                        <Grid item xs={4}>
                                            <FormControl variant="outlined">
                                                <InputLabel htmlFor='outlined-adornment-teamname'>Team Name</InputLabel>
                                                <OutlinedInput
                                                    required
                                                    type='text'
                                                    id="outlined-adornment-teamname"
                                                    disabled={true}
                                                    value={team.team_name}
                                                    label="Team Name"
                                                />
                                            </FormControl>
                                        </Grid>
                                        <Grid item xs={4}>
                                            <FormControl variant="outlined">
                                                <InputLabel htmlFor='outlined-email'>Email</InputLabel>
                                                <OutlinedInput
                                                    required
                                                    id="outlined-email"
                                                    variant="standard"
                                                    label="Email"
                                                    value={team.email}
                                                    onChange={(e) => handleLeagueChange(index, "email", e)}
                                                />
                                            </FormControl>
                                        </Grid>
                                        <Grid item xs={4}>
                                            <FormControl variant="outlined">
                                                <InputLabel htmlFor='outlined-ownername'>Owner Name</InputLabel>
                                                <OutlinedInput
                                                    id="outlined-ownername"
                                                    variant="standard"
                                                    label="Owner Name"
                                                    value={team.owner_name}
                                                    onChange={(e) => handleLeagueChange(index, "owner_name", e)}
                                                />
                                            </FormControl>
                                        </Grid>
                                    </React.Fragment>
                                );
                            }
                        )
                    }
                </Grid>
                
            </Box>
        </React.Fragment>
    );
};