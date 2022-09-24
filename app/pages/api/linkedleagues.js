import { verifyIdToken, getAuthUser, useAuthUser, getFirebaseAdmin } from 'next-firebase-auth'
import initAuth from '../../utils/initAuth'
import { doc, setDoc, updateDoc, deleteDoc } from 'firebase/firestore'


initAuth()
const db = getFirebaseAdmin().firestore();


const handlePost = async (linkedaccount, leagues) => {
  // Add all linked_leagues user is in from 
  if (leagues.length == 0){
    // Get the leagues from sleeper api
    const season = '2022'
    const userId = linkedaccount.id
    url = `https://api.sleeper.app/v1/user/${userId}/leagues/nfl/${season}`
    axios.get(url).then(resp => {
      console.log(resp.data);
      leagues = resp.data
    });
  }
  function addToDatabase(item) {
    // We can append/overwrite league to the database. This makes it easier to manage, and updates the league in case details.
    var accountsRef = await db.collection('linked_leagues').doc(item.league_id)
    var setWithMerge = await accountsRef.set(item, { merge: false });
  };
  leagues.forEach(addToDatabase);
};

const handlePut = async (user, accounts) => {
  console.log("Accounts to be put up:")
  console.log(accounts)
  var accountsRef = await db.collection('linked_accounts').doc(user.id)
  var setWithMerge = await accountsRef.set({
    'accounts': accounts
  }, { merge: false });
  return setWithMerge;
};


const handleDelete = async (user) => {
  await db.collection("linked_accounts").doc(user.id).delete().then(() => {
    return true;
  }).catch((error) => {
    console.error("Error removing document: ", error);
    return false;
  });
};

const handleGet = async (user) => {
  const accounts = await db.collection('linked_leagues').get(user.id);
  const accountsData = accounts.docs.map(entry => entry.data());
  return accountsData[0];
};

const handler = async (req, res) => {
  if (!(req.headers && req.headers.authorization)) {
    return res.status(400).json({ error: 'Missing Authorization header value' })
  }
  const token = req.headers.authorization
  var user = {}
  // This "unauthenticated" token is just an demo of the
  // "SSR with no token" example.
  if (token === 'unauthenticated') {
    return res.status(400).end(`Token Not Authorized For This Request`);
  } else {
    try {
      user = await verifyIdToken(token)
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e)
      return res.status(403).json({ error: 'Not authorized' })
    }

    const { method } = req;
    console.log("Request Method: "+method)
    switch (method) {
        case 'GET':
            return res.status(200).json(await handleGet(user));

        case 'POST':
            if ('league' in req.body) {
              return res.status(200).json(await handlePost(req.body['linked_account'], [req.body['league']]));
            }
            return res.status(200).json(await handlePost(req.body['linked_account'], []));

        case 'PUT': 
          return res.status(200).json(await handlePut(user, req.body['accounts']));

        case 'DELETE':
          return res.status(200).json(await handleDelete(user));

        default:
            res.setHeader('Allow', ['GET', 'POST', 'PUT', 'DELETE']);
            return res.status(405).end(`Method ${method} Not Allowed`);
    }
  }
}

export default handler