import * as React from 'react';

import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';

import { createTheme, ThemeProvider } from '@mui/material/styles';

import LeagueInfo from '@components/createLeague/LeagueInfo';
import ReviewLeague from '@components/createLeague/ReviewLeague';

import Layout from '@components/Layout';
import LinkEmails from '../components/createLeague/LinkEmails';



function Copyright() {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const steps = ['League Info', 'Link Emails', 'Review League'];
const sample_team_names = ["Burrow's Buddies", "Sacksonville", "The weeds", "Sandlawoods", "Big Booty Bitches"];

const theme = createTheme();

export default function CreateLeague () {
    const [activeStep, setActiveStep] = React.useState(0);

    const default_linkedLeague = {
        host: '',
        league_id: '',
        league_name: '',
        link_success: false
    }
    const create_sample_team = () => {
        return {
            email: '',
            owner_name: '',
            team_name: sample_team_names[Math.floor(Math.random() * 5)],
            user_id: Math.floor(Math.random() * 500),
            user_name: '',
            id: '',
        }
    }
    const [linked, setLinked] = React.useState(false);
    const [league, setLeague] = React.useState(
        {
            leagueName: '',
            leagueLogo: null,
            linkedLeagues: [default_linkedLeague],
            teams:[create_sample_team(), create_sample_team(), create_sample_team()],

        }
    );

    const handleAddLinkedLeague = () => {
        const newLeague = {...league};
        const newLinkedLeagues = [...league.linkedLeagues, default_linkedLeague];
        newLeague['linkedLeagues']= newLinkedLeagues;
        setLeague(newLeague);
    };

  const handleLeagueChange = (field, value, index) => {
    const newLeague = {...league};
    const newTeams = [];
    console.log("Field: " + field + "\tValue: "+ value)
    if (field=='linkedLeagues'){
        const newLinkedLeagues = [...league.linkedLeagues];
        newLinkedLeagues[index] = value;
        newLeague['linkedLeagues']= newLinkedLeagues;
        newLeague.linkedLeagues.forEach(linkedLeague =>{
            linkedLeague.teams.forEach(team => {
                team.id=team.user_id;

            });
        });
    } else {
        newLeague[field] = value;
    }
    var all_sub_leagues_linked = true;
    league.linkedLeagues.forEach(linkedLeague => {
        if (linkedLeague.link_success == false){
            all_sub_leagues_linked = false;
        }
    });
    setLinked(all_sub_leagues_linked)
    setLeague(newLeague);
  };

  const handleNext = () => {
    setActiveStep(activeStep + 1);
  };

  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  return (
    <Layout>
        <ThemeProvider theme={theme}>
        <CssBaseline />
        <Container component="main" sx={{ mb: 4 }}>
            <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
            <Typography component="h1" variant="h4" align="center">
                Create League
            </Typography>
            <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
                {steps.map((label) => (
                <Step key={label}>
                    <StepLabel>{label}</StepLabel>
                </Step>
                ))}
            </Stepper>
            <React.Fragment>
                {activeStep === steps.length ? (
                <React.Fragment>
                    <Typography variant="h5" gutterBottom>
                    League Created!
                    </Typography>
                    <Button href="/">Take Me Home</Button>
                </React.Fragment>
                ) : (
                <React.Fragment>
                    { activeStep == 0 && <LeagueInfo league={league} onChange={handleLeagueChange} addLinkedLeague={handleAddLinkedLeague}/>}
                    { activeStep == 1 && <LinkEmails league={league} onChange={handleLeagueChange}/>}
                    { activeStep == 2 && <ReviewLeague league={league} />}
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                    {activeStep !== 0 && (
                        <Button 
                        onClick={handleBack} 
                        sx={{ mt: 3, ml: 1 }}>
                        Back
                        </Button>
                    )}

                    <Button
                        variant="contained"
                        onClick={handleNext}
                        sx={{ mt: 3, ml: 1 }}
                    >
                        {activeStep === steps.length - 1 ? 'Place order' : 'Next'}
                    </Button>
                    </Box>
                </React.Fragment>
                )}
            </React.Fragment>
            </Paper>
            <Copyright />
        </Container>
        </ThemeProvider>   
    </Layout>
  );
};
