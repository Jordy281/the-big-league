import * as React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import AddLinkIcon from '@mui/icons-material/AddLink';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import Input from '@mui/material/Input';
import OutlinedInput from '@mui/material/OutlinedInput';

function LinkLeague (props) {
    const supported_leagues = ['Sleeper', 'Yahoo', 'NFL']

    const handleHostChange = (e) => {
        console.log('asdfa')
        const { name, value } = e.target;
        console.log(value)
        const league = {
            host: value,
            league_id: '',
            league_name: '',
            link_success: false
        };
        props.onChange(props.index, league);
    };;

    const handleLeagueIdChange = (e) => {
        const { name, value } = e.target;
        const league = {
            ...props.league,
            league_id: value,
            league_name: '',
            link_success: false,
        };

        props.onChange(props.index, league);
    };

    const linkId = () => {
        // this is where we should pull in data from host API
        const leagueName = "Demo"
        //If successfully linked
        const league = {
            ...props.league,
            link_success: true,
            league_name: leagueName
        };
        props.onChange(props.index, league);

    };
  
    return (
        <>
        <Grid container direction="row" alignItems="center" spacing={1}>
            <Grid item xs={4}>
                <FormControl variant="outlined" sx={{ m: 1, minWidth: 250 }}>
                <InputLabel htmlFor='outlined-adornment-leagueid'>League Provider</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={props.league.host}
                    label="Select League Provider"
                    onChange={handleHostChange}
                    autoWidth
                >
                    {
                        supported_leagues.map((league, index) => (
                            <MenuItem value={league} key={index}>{league}</MenuItem>
                        ))
                    }
                </Select>
                </FormControl>
            </Grid>
            <Grid item xs={4}>
                <FormControl variant="outlined">
                <InputLabel htmlFor='outlined-adornment-leagueid'>League Id</InputLabel>
                <OutlinedInput
                    required
                    type='text'
                    id="outlined-adornment-leagueid"
                    value={props.league.league_id}
                    onChange={handleLeagueIdChange}
                    endAdornment={
                        <InputAdornment position="end">
                            <IconButton
                            aria-label="link league id"
                            onClick={linkId}
                            >
                                <AddLinkIcon />
                            </IconButton>
                        </InputAdornment>
                    }
                    label="League ID"
                />
                </FormControl>
            </Grid>
            <Grid item xs={4}>
                <FormControl variant="outlined">
                    <InputLabel htmlFor='outlined-leaguename'>League Name</InputLabel>
                    <OutlinedInput
                        required
                        id="outlined-leaguename"
                        variant="standard"
                        disabled={true}
                        label="League Name"
                        value={props.league.league_name}
                    />
                </FormControl>
            </Grid>
        </Grid>
        </>
    );
};

export default LinkLeague;
