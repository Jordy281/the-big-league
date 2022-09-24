import * as React from 'react';
import { useEffect } from 'react'

import Layout from "@components/Layout";

import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';
import IconButton from '@mui/material/IconButton';

import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import { mainListItems, secondaryListItems } from '@components/settings/listItems';

import Snackbar from '@mui/material/Snackbar';
import Fade from '@mui/material/Fade';

import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';


import Account from '@components/settings/account/Account';
import Leagues from '@components/settings/account/Leagues';

import { getAuth, updateProfile } from "firebase/auth";

import { getAccounts, addAccounts, updateAccounts } from '@lib/accounts';
import { useRouter } from 'next/router';

import {
  useAuthUser,
  withAuthUser,
  withAuthUserTokenSSR,
  AuthAction,
} from 'next-firebase-auth'

const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    '& .MuiDrawer-paper': {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);

const mdTheme = createTheme();


const Settings = ({accounts}) => {
    const router = useRouter();

    const [selectedIndex, setSelectedIndex] = React.useState(0)
    const [open, setOpen] = React.useState(false);
    const [user, setUser] = React.useState(useAuthUser());
    const [state, setState] = React.useState({
      open: false,
      Transition: Fade,
    });

    const toggleDrawer = () => {
        setOpen(!open);
    };

    const handleListItemClick = (value, index) => {
      if ( index != selectedIndex ){
          setSelectedIndex(index)
      }
    };

    const handleUserChange = (field, value) =>{
      setUser({...user, [field]: value});
    };

    const handleSubmitChanges = (event) =>{
      event.preventDefault();
      updateProfile(auth.currentUser, user).then(() => {
        setState({
          ...state,
          open: true,
          message: "Profile Updated!"
        });
        
      }).catch((error) => {
        setState({
          ...state,
          open: true,
          message: "Profile Update Failed!"
        });
      });
    };
  
    const handleClose = () => {
      setState({
        ...state,
        open: false,
      });
    };
    
    
    const handleAddAccount = async (newAccount) =>{
      const acc = {
        'host' : 'Sleeper',
        'username' : newAccount.username,
        'email' : newAccount.email,
        'user_id' : newAccount.user_id,
        'avatar' : newAccount.avatar,
        'display_name' : newAccount.display_name,
      };
      const newaccountslist =[...accounts, acc]
      const token = await user.getIdToken();
      
      if (await addAccounts(token, newaccountslist)){
        accounts = newaccountslist;
        setState({
          ...state,
          open: true,
          message: "Account Added!"
        });
        router.replace(router.asPath);
      
      } else {
        setState({
          ...state,
          open: true,
          message: "Unable to add account :("
        });
      }
    };

    const handleDeleteAccount = async (account) =>{

      const newaccountslist = accounts.filter((acc) => !((acc.user_id == account.user_id) & (acc.host == account.host)));
      const token = await user.getIdToken();
      
      if (await updateAccounts(token, newaccountslist)){
        accounts = newaccountslist;
        setState({
          ...state,
          open: true,
          message: "Account Deletted!"
        });
        router.replace(router.asPath);
      
      } else {
        setState({
          ...state,
          open: true,
          message: "Unable to delete account :("
        });
      }
    };


    return (
      <Layout>
        <ThemeProvider theme={mdTheme}>
          <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <Drawer variant="permanent" open={open}>
              <Toolbar
              sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              px: [1],
              }}
              >
                <IconButton onClick={toggleDrawer}>
                {open &&
                  <ChevronLeftIcon />
                }
                {!open &&
                  <ChevronRightIcon />
                }
                </IconButton>
              </Toolbar>
              <Divider />
              <List component="nav">
                <ListItemButton
                onClick={(event) => handleListItemClick(event, 0)}
                >
                  <ListItemIcon>
                    <AccountCircleIcon />
                  </ListItemIcon>
                  <ListItemText primary="Account" />
                </ListItemButton>
                <ListItemButton
                onClick={(event) => handleListItemClick(event, 1)}
                >
                  <ListItemIcon>
                    <EmojiEventsIcon />
                  </ListItemIcon>
                  <ListItemText primary="Leagues" />
                </ListItemButton>
                <Divider sx={{ my: 1 }} />
                {secondaryListItems}
              </List>
            </Drawer>
            <Box
              component="main"
              sx={{
              backgroundColor: (theme) =>
              theme.palette.mode === 'light'
              ? theme.palette.grey[100]
              : theme.palette.grey[900],
              flexGrow: 1,
              height: '100vh',
              overflow: 'auto',
              }}
            >
              {selectedIndex==0 &&
                <Account 
                user = {user}
                accounts = {accounts}
                addAccount = {handleAddAccount}
                deleteAccount = {handleDeleteAccount}
                onChange = {handleUserChange}
                submitChange = {handleSubmitChanges}/>
              }
              {selectedIndex==1 &&
                <Leagues condition={selectedIndex==1}/>
              }
            </Box>
            <Snackbar
              open={state.open}
              onClose={handleClose}
              TransitionComponent={state.Transition}
              message={state.message}
              key={state.Transition.name}
            />
          </Box>
        </ThemeProvider>
      </Layout>
      );
    
}


export const getServerSideProps = withAuthUserTokenSSR({
  whenUnauthed: AuthAction.REDIRECT_TO_LOGIN,
})(async ({ AuthUser, req }) => {
  // Optionally, get other props.
  // You can return anything you'd normally return from
  // `getServerSideProps`, including redirects.
  // https://nextjs.org/docs/basic-features/data-fetching#getserversideprops-server-side-rendering
  const token = await AuthUser.getIdToken();

  // This endpoint uses an ID token.
  // Note: you shouldn't typically fetch your own API routes from within
  // `getServerSideProps`. This is for example purposes only.
  // https://github.com/gladly-team/next-firebase-auth/issues/264
  const data = await getAccounts(token, req);
  console.log("GET ACCOUNTS")

  return {
    props: {
      accounts: data.accounts
    },
  }
})

export default withAuthUser({
  whenUnauthedAfterInit: AuthAction.REDIRECT_TO_LOGIN,
})(Settings)