import Header from '@components/Header'
import Head from 'next/head'

export default function Layout({ children }) {
  return (
    <>
      <Header></Header>
      <main>{children}</main>
    </>
  );
}
