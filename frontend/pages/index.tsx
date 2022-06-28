import type { NextPage } from 'next'
import Head from 'next/head'
import SummarizerAI from '../components/homeComponents'
import styles from '../styles/Home.module.css'

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>Summarizer AI</title>
        <meta name="description" content="Summarizing test with the help of AI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <SummarizerAI/>
    </div>
  )
}

export default Home
