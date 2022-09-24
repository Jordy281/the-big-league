import '../styles/globals.css'
import 'bootstrap/dist/css/bootstrap.min.css'

import initAuth from '@utils/initAuth'

initAuth()

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}

export default MyApp
