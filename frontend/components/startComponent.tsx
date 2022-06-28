import React from "react";

const HomeComp: React.FC = () => {

    const gradientTextStyle =
    "text-white text-transparent bg-clip-text bg-gradient-to-r from-teal-300 to-blue-500 font-light w-fit mx-auto";

    return (
        <>
        <div className="bg-white dark:bg-slate-800 rounded-lg px-6 py-8 ring-1 ring-slate-900/5 shadow-xl"> 
          <div className="inline-flex">
            <div className='bg-cyan-900 p-3 text-white'>
              <div className='text-center my-3'>
                <h1 className={gradientTextStyle + " text-5xl font-light"}>
                  Summarizer AI
                </h1>
              <div className={gradientTextStyle + " text-4xl font-ligth aspect-auto"}>Your AI assistent</div>
            </div>
          </div>
        </div>
    </div>
        </>
    )
}

export default HomeComp;