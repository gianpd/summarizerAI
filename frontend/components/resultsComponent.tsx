import React from 'react';

interface ResultProps {
    prompt: string,
    summary: string,
    onBack: any
}

const Results: React.FC<ResultProps> = (props) => {

    const resultSection = (label: string, body: any) => {
        return (
          <div className="bg-slate-700 p-4 my-3 rounded-md">
            <div className="text-slate-400 text-sm font-bold mb-4">{label}</div>
            <div>{body}</div>
          </div>
        );
      };

    return (
    <>
    <div className='mb-6'>
        {resultSection(
            "Prompt",
            <div className='text-lg font-bold'>{props.prompt}</div>
        )}
        {resultSection("Summary", props.summary)}
    </div>
    <button
      className='bg-gradient-to-r from-teal-400
      to-blue-500 disabled:opacity-50 w-full p-2 rounded-md text-lg'
      onClick={props.onBack}>
        Back
    </button>
    </>
    )
}

export default Results;