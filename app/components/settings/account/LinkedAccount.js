import * as React from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import { Avatar } from '@mui/material';

function LinkedAccount (props) {
    const supported_leagues = ['Sleeper', 'Yahoo', 'NFL']


    const [account, setAccount] = React.useState({ ...props.account});
    

    const handleDelete = () => {
        props.onDelete(account);
    };

    var avatar_source = '';
    if ( account.host == 'Sleeper' ) {
        avatar_source = 'https://sleepercdn.com/avatars/thumbs/' + account.avatar;
    }

  
    return (
        <React.Fragment>
            <ListItem 
                secondaryAction={
                    <IconButton edge="end" aria-label="delete" onClick={handleDelete}>
                        <DeleteIcon />
                    </IconButton>
                }>
                <ListItemAvatar>
                <Avatar src={avatar_source}/>
                </ListItemAvatar>
                <ListItemText primary={account.display_name} secondary={account.host} />
            </ListItem>
        </React.Fragment>
    );
};

export default LinkedAccount;
