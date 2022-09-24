import useUser from '@lib/firebase/useUser'
import Layout from '@components/Layout'

const Profile = () => {
  // Fetch the user client-side
  const { user } = useUser({ redirectTo: '/auth' })

  // Server-render loading state
  if (!user || user.isLoggedIn === false) {
    return <>Loading...</>
  }

  // Once the user request finishes, show the user
  return (
    <Layout>
      <h1>Your Profile</h1>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </Layout>
  )
}

export default Profile