import React from "react";

const HomeComp: React.FC = () => {

    const gradientTextStyle =
    "font-mono text-white text-transparent bg-clip-text bg-gradient-to-r from-teal-300 to-blue-500 font-light w-fit mx-auto";

    return (
        <>
          <div className="center-flex">
            <div className='bg-cyan-800 p-5 bg-clip-text'>
              <div className='text-center my-5'>
                <h1 className={gradientTextStyle + " text-5xl font-light aspect-auto"}>
                  Summarizer AI
                </h1>
              <div className={gradientTextStyle + " text-3xl font-light aspect-auto"}>Your AI assistent</div>
            </div>
          </div>
        </div>
        </>
    )


}

export default HomeComp;