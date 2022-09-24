import * as React from 'react';

import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import { Divider } from "@mui/material";
import List from '@mui/material/List';
import "firebase/auth";


import LinkSleeper from "@components/settings/linkFantasyAccount/LinkSleeper";
import LinkNFL from "@components/settings/linkFantasyAccount/LinkNFL";
import LinkYahoo from "@components/settings/linkFantasyAccount/LinkYahoo";
import LinkedAccount from "./LinkedAccount";

export default function Account ( props ) {
    if (!props){
        console.log("props is undifined: " + props)
        return (<p>Error: User is undefined</p>);
    }

    const [linkNFLFantasy, setLinkNFLFantasy] = React.useState(false); 
    const [linkSleeper, setLinkSleeper] = React.useState(false); 
    const [linkYahoo, setLinkYahoo] = React.useState(false); 


    const handleInputChange = (e) => {
        const { name, value } = e.target;
        props.onChange(name, value);
    };


    const handleSubmit = (e) => {
        props.submitChange(e);
    };

    const handleSleeperClickOpen = () => {
        setLinkSleeper(true);
    };

    const handleSleeperClose = (sleeperAccount) => {
        setLinkSleeper(false);
        if (sleeperAccount && Object.keys(sleeperAccount).length != 0 && Object.getPrototypeOf(sleeperAccount) === Object.prototype){
            props.addAccount(sleeperAccount);
        }
    };

    const handleNFLClickOpen = () => {
        setLinkNFLFantasy(true);
    };
    const handleNFLClose = () => {
        setLinkNFLFantasy(false);
    };

    const handleYahooClickOpen = () => {
        setLinkYahoo(true);
    };
    
    const handleYahooClose = () => {
        setLinkYahoo(false);
    };

    const handleDeleteLinkedAccount = (account) => {
        props.deleteAccount(account);
    }

    return (
        <React.Fragment>
            <Box spacing={3} sx={{ my: 3, mx: 2 }}>
                <Grid container alignItems="center" spacing={2}>
                    <Grid item>
                    <TextField
                        id="name-input"
                        name="displayName"
                        label="Name"
                        type="text"
                        value={props.user.displayName}
                        onChange={handleInputChange}
                        disabled={true}
                    />
                    </Grid>
                    <Grid item>
                    <TextField
                        id="id-input"
                        name="id"
                        label="ID:"
                        type="text"
                        value={props.user. id}
                        onChange={handleInputChange}
                        disabled={true}
                    />
                    </Grid>
                    <Grid item>
                    <TextField
                        id="name-input"
                        name="email"
                        label="Email"
                        type="text"
                        value={props.user.email}
                        onChange={handleInputChange}
                        disabled={true}
                    />
                    </Grid>
                    <Grid item>
                        <Button disabled={true} variant="contained" color="primary" type="submit" onClick={handleSubmit}>
                            Submit
                        </Button>
                    </Grid>
                </Grid>
            </Box>
            
            {
                props.accounts.length >0 &&
                <Box sx={{ m: 2 }}>
                    <Divider variant="middle"></Divider>
                    <Typography variant="h6" gutterBottom>
                        Your Fantasy Accounts
                    </Typography>
                    <List>
                    {
                        props.accounts.map(
                            (account, index) => {
                                return (
                                    <LinkedAccount key={index} onDelete={handleDeleteLinkedAccount} index={index} account={account}/>
                                );
                            }
                        )
                    }
                    </List>
                </Box>

            }
            <Divider variant="middle"></Divider>

            <Box sx={{ m: 2 }}>
                <Typography>
                    Link Your Fantasy Accounts
                </Typography>
                <Grid container>
                    <Grid Item>
                        <Button onClick={handleSleeperClickOpen}>
                            <img src="/images/sleeper_logo.png" width="100" alt="Sleeper"/>
                        </Button>
                        <LinkSleeper
                            open={linkSleeper}
                            onClose={handleSleeperClose}
                        />
                    </Grid>
                    <Grid Item>
                        <Button onClick={handleYahooClickOpen}>
                            <img src="/images/yahoo_fantasy_logo.png" width="100" alt="Yahoo"/>
                        </Button>
                        <LinkYahoo
                            open={linkYahoo}
                            onClose={handleYahooClose}
                        />
                    </Grid>
                    <Grid Item>
                        <Button onClick={handleNFLClickOpen}>
                            <img src={"/images/nfl_fantasy_logo.jpg"} width="100" alt="NFL.com" />
                        </Button>
                        <LinkNFL
                            open={linkNFLFantasy}
                            onClose={handleNFLClose}
                        />
                    </Grid>
                </Grid>
            </Box>
        </React.Fragment>
    );
    
};
