import type { NextPage } from 'next'
import Head from 'next/head'
import SummarizerAI from '../components/homeComponents'
import SummarizerFromText from '../components/homeTextComponents'
import HomeCom from '../components/startComponent'
import styles from '../styles/Home.module.css'

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>Summarizer AI</title>
        <meta name="description" content="Summarizing test with the help of AI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className='bg-sky-700 ...'>
        <HomeCom/>
        <div className='p-5'>
          <SummarizerFromText/>
        </div>
      </div>
    </div>
  )
}

export default Home
