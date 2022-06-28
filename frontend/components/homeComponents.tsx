import React from 'react';

const SummarizerAI: React.FC = () => {
    const END_POINT: string = "http://localhost:5010/summaries/"
    const [prompt, setPromt] = React.useState("");
    const [postId, setPostID] = React.useState("");
    const [snippet, setSnippet] = React.useState("");

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
        setPostID(data.id);

        fetch(`${END_POINT}${data.id}`)
        .then((res) => res.json())
        .then(onResult);
    }

    console.log("Retrived on POST: " + postId);

    const onResult = (data: any) => {
        setSnippet(data.summary);
    }

    console.log(snippet);


    let resultsElement = <div>
        Here is the summary: <div>
            {snippet}
        </div>
    </div>;

    // if (hasResult) {
    //     resultsElement = <div>
    //     Here is the summary: 
    //     <div>Summary: {snippet}</div>
    //     </div>
    // }

    return (
        <>
        <h1>Summarizer AI</h1>
        <p>Write any valid URL and get a summarizer version of it:</p>
        <input 
        type='text'
        placeholder="https://www.ansa.it"
        value={prompt}
        onChange={(e) => setPromt(e.currentTarget.value)}></input>
        <button onClick={onSubmit}>Submit</button>
        {resultsElement}
        </>
    )
}

export default SummarizerAI;