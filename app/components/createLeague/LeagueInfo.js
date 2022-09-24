import * as React from 'react';

import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';

import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Divider from '@mui/material/Divider';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';


import LinkLeague from '@components/createLeague/LinkLeague';


export default function LeagueInfo(props) {

    const handleLinkedLeagueChange = (index, league) => {
        props.onChange('linkedLeagues', league, index);
    };

    const handleLeagueChange = (e) => {
        if (typeof(e) != 'undefined'){
            const { name, value } = e.target;
            if (name == 'relegation') {
                value = e.target.checked;
            }
            props.onChange(name, value, null);
        }
    };

    const handleAddLinkedLeague = (e) =>{
        props.addLinkedLeague();
    };

    return (
        <React.Fragment>
            <Box spacing={3} sx={{ my: 3, mx: 2 }}>
                <Typography variant="h6" gutterBottom>
                    League Information
                </Typography>
                <Grid container xs={6}>
                <TextField
                        required
                        id="leagueName"
                        name="leagueName"
                        label="League Name"
                        fullWidth
                        variant="standard"
                        value={props.league.leagueName}
                        onChange={handleLeagueChange}
                    />
                
                </Grid>
                <FormControlLabel
                    control={<Checkbox color="secondary" name="relegation" value={props.league.subleagues} onChange={handleLeagueChange}/>}
                    label="Does this league consist of sub leagues? (Relegation)"
                />

            </Box>
            <Divider variant="middle"></Divider>
            <Box sx={{ m: 2 }}>
                <Typography variant="h6" gutterBottom>
                    Link to Your Fantasy League
                </Typography>
                <Grid container spacing={3} direction='row'>
                    {
                        props.league.linkedLeagues.map(
                            (linked_league, index) => {
                                return (
                                    <Grid item xs={12}>
                                        <LinkLeague key={index} onChange={handleLinkedLeagueChange} index={index} league={linked_league}/>
                                    </Grid>
                                );
                            }
                        )
                    }
                    <Grid item>
                        <Fab size="small" color="secondary" aria-label="add" onClick={handleAddLinkedLeague}>
                            <AddIcon />
                        </Fab>
                    </Grid>
                </Grid>
                
            </Box>
        </React.Fragment>
    );
};