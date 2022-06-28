import React from 'react';

import Form from './formComponents'
import Results from './resultsComponent';

const SummarizerAI: React.FC = () => {
    const END_POINT: string = "http://localhost:5010/summaries/"

    // hooks
    const [prompt, setPrompt] = React.useState("");
    const [postId, setPostID] = React.useState("");
    const [summary, setSummary] = React.useState("");
    const [hasresult, setHasResult] = React.useState(false);
    const [isLoading, setIsLoading] = React.useState(true);

    const onSubmit = () => {
        // primo metodo chiamato quando url è inserito -> POST request to the back-end
        console.log("Submitting: " + prompt);

        fetch(END_POINT,
        {
            method: 'POST',
            mode: 'cors',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({'url': prompt})
        })
        .then((res) => res.json())
        .then(onResultPost);
    }

    const onResultPost = (data: any) => {
        setPostID(data.id); // set state postID to data.id

        // request the ID summary to the BE (GET)
        fetch(`${END_POINT}${data.id}`)
        .then((res) => res.json())
        .then(onResult);
    }

    console.log("Retrived on POST: " + postId);

    const onResult = (data: any) => {
        setSummary(data.summary);
        setHasResult(true);
        setIsLoading(true);
    }

    console.log(summary);

    const onReset = () => {
        setPrompt("")
        setHasResult(false)
        setIsLoading(true)
    }


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
            comment="Set any valid URL and get a summarized version of it!"
            placeholder='https://www.ansa.it'
            startsWith='https://'
            prompt={prompt}
            setPrompt={setPrompt}
            onSubmit={onSubmit}
            isLoading={isLoading}
            characterLimit={150}/>
        )
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
                    {resultsElement}
                </div>
            </div>
        </div>
        </>
    )
}

export default SummarizerAI;