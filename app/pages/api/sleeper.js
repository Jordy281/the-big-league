import { verifyIdToken, getAuthUser, useAuthUser, getFirebaseAdmin } from 'next-firebase-auth'
import initAuth from '../../utils/initAuth'
import { doc, setDoc, updateDoc, deleteDoc } from 'firebase/firestore'


initAuth()
const db = getFirebaseAdmin().firestore();


const handlePost = async (user, leagues) => {
  return
};

const handlePut = async (user, accounts) => {
  return
};

const handleDelete = async (user) => {
  return
};

const handleGet = async (params) => {
  if (params['type'] )
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