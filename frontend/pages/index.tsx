import type { NextPage } from 'next'
import Head from 'next/head'
import SummarizerAI from '../components/homeComponents'
import SummarizerFromText from '../components/homeTextComponents'
import styles from '../styles/Home.module.css'

const Home: NextPage = () => {
  return (
    <div className={styles.container} style={{
      background: 'black'
    }}>
      <Head>
        <title>Summarizer AI</title>
        <meta name="description" content="Summarizing test with the help of AI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className=''>
        <div className='grid grid-rows-2 gap-4'>
          <div><SummarizerAI/></div>
          <div><SummarizerFromText/></div>
        </div>
      </div>
    </div>
  )
}

export default Home
