import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';

import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import { useEffect, useState } from 'react';
import StyledFirebaseAuth from 'react-firebaseui/StyledFirebaseAuth';

import { getApp } from 'firebase/app'
import { 
    getAuth, 
    EmailAuthProvider,
    GoogleAuthProvider,
    TwitterAuthProvider
} from 'firebase/auth'

const firebaseAuthConfig = {
    signInFlow: 'popup',
    // Auth providers
    // https://github.com/firebase/firebaseui-web#configure-oauth-providers
    signInOptions: [
        {
            provider: EmailAuthProvider.PROVIDER_ID,
            requireDisplayName: true,
        },
        // add additional auth flows below
        GoogleAuthProvider.PROVIDER_ID,
        TwitterAuthProvider.PROVIDER_ID,
    ],
    signInSuccessUrl: '/',
    credentialHelper: 'none',
    callbacks: {
        // https://github.com/firebase/firebaseui-web#signinsuccesswithauthresultauthresult-redirecturl
        signInSuccessWithAuthResult: () =>
        // Don't automatically redirect. We handle redirects using
        // `next-firebase-auth`.
        false,
    },
}

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        The Big League
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const theme = createTheme();

const FirebaseAuth = () => {
    // Do not SSR FirebaseUI, because it is not supported.
    // https://github.com/firebase/firebaseui-web/issues/213
    const [renderAuth, setRenderAuth] = useState(false)
    useEffect(() => {
        if (typeof window !== 'undefined') {
            setRenderAuth(true)
        }
    }, [])
    return (
        <div>
            {renderAuth ? (
                <ThemeProvider theme={theme}>
                <Container component="main" maxWidth="xs" >
                    <Grid
                        container
                        spacing={0}
                        direction="column"
                        alignItems="center"
                        justifyContent="center"
                        style={{ minHeight: '80vh' }}
                    >

                        <Grid item xs={3}>
                            <CssBaseline />
                            <Paper
                                sx={{
                                    p: 2,
                                    margin: 'auto',
                                    maxWidth: 500,
                                    flexGrow: 1,
                                    backgroundColor: (theme) =>
                                    theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
                                }}
                                >
                                <Box
                                    sx={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    }}
                                >
                                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                                    <LockOutlinedIcon />
                                    </Avatar>
                                    <Typography component="h1" variant="h5">
                                    Sign in
                                    </Typography>
                                    <StyledFirebaseAuth
                                        uiConfig={firebaseAuthConfig}
                                        firebaseAuth={getAuth(getApp())}
                                    />
                                </Box>
                            </Paper>
                        </Grid>
                    </Grid>
                <Copyright sx={{ mt: 8, mb: 4 }} />
            </Container>
            </ThemeProvider>
            ) : null}
        </div>
    )
}

export default FirebaseAuth