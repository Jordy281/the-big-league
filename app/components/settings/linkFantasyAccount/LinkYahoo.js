import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import PropTypes from 'prop-types';



export default function LinkYahoo(props) {
  
    const handleClose = () => {
        props.onClose();
    };
  
    return (
      <Dialog onClose={handleClose} open={props.open}>
        <DialogTitle>Not Yet Supported</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Linking your Yahoo Fantasy account is not available at this time. Check back in 2023 for more information!
          </DialogContentText>
        </DialogContent>
        <DialogActions>
            <Button autoFocus onClick={handleClose}>
                Close
            </Button>
        </DialogActions>
      </Dialog>
    );
  }
  
  LinkYahoo.propTypes = {
    onClose: PropTypes.func.isRequired,
    open: PropTypes.bool.isRequired,
  };
  