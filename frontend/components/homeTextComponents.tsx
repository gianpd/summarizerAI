import React from 'react';

import Results from './resultsComponent';
import Form from './formComponents';


const SummarizerFromText: React.FC = () => {
    const END_POINT: string = "http://localhost:5010/summaries/text"
    const [prompt, setPrompt] = React.useState("");
    const [summary, setSummary] = React.useState("");
    const [hasresult, setHasResult] = React.useState(false);
    const [isLoading, setIsLoading] = React.useState(true);


    const onSubmit = () => {
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
         .then(OnResult)
    }

    const OnResult = (data: any) => {
        setSummary(data.summary)
        setHasResult(true)
        setIsLoading(false);
    }

    console.log(summary);

    const onReset = () => {
        setPrompt("");
        setHasResult(false);
        setIsLoading(true);
    }


    const gradientTextStyle =
    "text-white text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-400 font-light w-fit mx-auto";

    let resultsElement = null;
    // if result is set -> define result element.
    if (hasresult) {
        resultsElement = (
            <Results
            prompt={prompt}
            summary={summary}
            onBack={onReset}/>
        )
    } else {
        resultsElement = (
            <Form
            comment="Submit a text and get a summarized version of it!"
            placeholder='enter some text'
            startsWith=''
            prompt={prompt}
            setPrompt={setPrompt}
            onSubmit={onSubmit}
            isLoading={isLoading}
            characterLimit={1024}/>
        )
    }

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
                    {resultsElement}
                </div>
            </div>
        </div>
        </>
    )
}

export default SummarizerFromText;