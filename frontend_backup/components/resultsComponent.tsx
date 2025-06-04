import React from 'react';

interface ResultProps {
    prompt: string,
    summary: string,
    onBack: any
}

const Results: React.FC<ResultProps> = (props) => {

    const resultSection = (label: string, body: any) => {
        return (
          <div className="bg-slate-600 p-4 my-3 rounded-md">
            <div className="font-mono text-slate-400 text-sm font-bold mb-4">{label}</div>
            <div>{body}</div>
          </div>
        );
      };

    return (
    <>
    <div className='mb-9'>
        {resultSection(
            "Prompt",
            <div className='text-lg font-mono mb-4'>{props.prompt}</div>
        )}
        {resultSection(
          "Summary", 
          <div className='text-lg font-mono mb-9'>{props.summary}</div>)}
    </div>
    <button
      className='font-mono bg-gradient-to-r from-teal-400
      to-blue-600 disabled:opacity-50 w-full p-5 rounded-md text-lg font-bold'
      onClick={props.onBack}>
        Back
    </button>
    </>
    )
}

export default Results;