import Head from 'next/head'
import styles from '@styles/Home.module.css'
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'

import Landing from '@components/Landing'
import Layout from '@components/Layout'

import {
  useAuthUser,
  withAuthUser,
  withAuthUserTokenSSR,
  AuthAction,
} from 'next-firebase-auth'

const Home = () => {
  const user = useAuthUser()

  if (user) {
    return (
      <Layout>
        <div className={styles.container}>
          <Card>
            <Card.Body>
              <Card.Title>{user.name}</Card.Title>
              <Card.Text>{user.email}</Card.Text>
              <hr />
              {user.profilePic ? <image src={user.profilePic} height={100} width={100}></image> : <p>No profile pic</p>}
              <hr />
              <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                <Button onClick={() => logout()} style={{ width: '100px' }}>Log Out</Button>
                <a href="https://github.com/bjcarlson42/nextjs-with-firebase" target="_blank">
                  <Button variant="outline-secondary" style={{ width: '100px' }}>Code</Button>
                </a>
              </div>
            </Card.Body>
          </Card>
        </div>
      </Layout>
    )
  }
  else return (
    <Landing /> 
  )
}
export const getServerSideProps = withAuthUserTokenSSR()()

export default withAuthUser({
  whenUnauthedAfterInit: AuthAction.REDIRECT_TO_LOGIN,
})(Home)