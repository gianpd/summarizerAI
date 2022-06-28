import React from 'react';


const SummarizerFromText: React.FC = () => {
    const END_POINT: string = "http://localhost:5010/summaries/text"
    const [prompt, setPrompt] = React.useState("");


    const OnSubmit = () => {
        console.log("Submitted: " + prompt);
        fetch(
            END_POINT,
            {
                method: 'POST',
                mode: 'cors',
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify({"text": prompt})
            }
        ).then((res) => res.json())
         .then(console.log)
    }


    const gradientTextStyle =
    "text-white text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-400 font-light w-fit mx-auto";

    return (
        <>
        <div className='h-screen flex'> 
            <div className='max-w-md mx-auto p-1'>
                <div className='bg-slate-800 p-8 text-white'>
                    <div className='text-center my-4'>
                        <h1 className={gradientTextStyle + " text-7xl font-light"}>
                            Summarizer AI
                        </h1>
                        <div className={gradientTextStyle + " text-4xl font-ligth aspect-auto"}>Your AI assistent</div>
                    </div>
                </div>
            </div>
            <div>
                <p>Enter some text and get a summarized version of it!</p>
            </div>
        </div>
        </>
    )
}

export default SummarizerFromText;