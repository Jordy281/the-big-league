import { verifyIdToken, getAuthUser, useAuthUser, getFirebaseAdmin } from 'next-firebase-auth'
import initAuth from '../../utils/initAuth'
import { doc, setDoc, updateDoc, deleteDoc } from 'firebase/firestore'


initAuth()
const db = getFirebaseAdmin().firestore();

const handlePost = async (user, accounts) => {
  // For all leagues the user is in:
    // 1. Add users linked account to linked_accounts
    // 2. Add all league he's in to Leagues
    // 3. Add all teams user owns to Team

  console.log("Accounts to be posted up:")
  console.log(accounts)
  var accountsRef = await db.collection('linked_accounts').doc(user.id)
  var setWithMerge = await accountsRef.set({
    'accounts': accounts
  }, { merge: false });
  return setWithMerge;
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
  const accounts = await db.collection('linked_accounts').get(user.id);
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
            return res.status(200).json(await handlePost(user, req.body['accounts']));

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