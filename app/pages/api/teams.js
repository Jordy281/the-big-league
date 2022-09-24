import { verifyIdToken } from 'next-firebase-auth'
import initAuth from '../../utils/initAuth'

initAuth()

const handlePost = (req, res) => {
    // For all leagues the user is in:
        // 1. Add league to user.leagues
        // 2. Add league to Leagues

        // 3. Add all teams user owns to user.leagues.teams
        // 4. Add all teams user owns to Teams
        

};

const handleGet = (req, res) => {
    

};

const handler = async (req, res) => {
  if (!(req.headers && req.headers.authorization)) {
    return res.status(400).json({ error: 'Missing Authorization header value' })
  }
  const token = req.headers.authorization

  let favoriteColor

  // This "unauthenticated" token is just an demo of the
  // "SSR with no token" example.
  if (token === 'unauthenticated') {
    favoriteColor = 'unknown, because you called the API without an ID token'
  } else {
    try {
      await verifyIdToken(token)
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e)
      return res.status(403).json({ error: 'Not authorized' })
    }

    const { method } = req;

    switch (method) {
        case 'GET':
            res.json({ method: 'GET', endpoint: 'Users' });
            handleGet();
            break;
        case 'POST':
            handlePost();
            break;
        default:
            res.setHeader('Allow', ['GET', 'POST']);
            res.status(405).end(`Method ${method} Not Allowed`);
            break;
    }

    const colors = [
      'sea foam green',
      'light purple',
      'teal',
      'taupe',
      'dark grey',
    ]
    favoriteColor = colors[Math.floor(Math.random() * colors.length)]
  }

  return res.status(200).json({ favoriteColor })
}

export default handler