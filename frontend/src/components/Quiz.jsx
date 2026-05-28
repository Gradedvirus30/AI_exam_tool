import axios from "axios";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

function Quiz(){

const [topic,setTopic]=useState("");

const [questions,setQuestions]=useState("");

const [answers,setAnswers]=useState("");

const [showAnswers,setShowAnswers]=useState(false);

const generateQuiz=async()=>{

const response=await axios.post(

"https://aiexamtool-production.up.railway.app/quiz",

{
topic
},

{
headers:{

"session-id":
localStorage.getItem(
"session_id"
)

}
}

);

const fullQuiz=response.data.quiz;

const splitText=fullQuiz.split("ANSWERS:");

setQuestions(
splitText[0]
);

setAnswers(
splitText[1] || "No answers generated."
);

setShowAnswers(false);

};

const downloadQuiz=()=>{

const content=`

${questions}

ANSWERS:

${answers}

`;

const blob=new Blob(

[content],

{
type:"text/plain"
}

);

const url=
window.URL.createObjectURL(
blob
);

const a=
document.createElement("a");

a.href=url;

a.download="quiz.txt";

a.click();

window.URL.revokeObjectURL(
url
);

};

return(

<div className="card">

<h3>Quiz</h3>

<input
type="text"
placeholder="Enter topic"
value={topic}
onChange={(e)=>setTopic(e.target.value)}
/>

<button onClick={generateQuiz}>

🎯 Generate Quiz

</button>

{questions && (

<>

<div className="response">

<ReactMarkdown>

{questions}

</ReactMarkdown>

</div>

<button
onClick={()=>
setShowAnswers(
!showAnswers
)
}
>

{showAnswers
? "Hide Answers"
: "Show Answers"}

</button>

{showAnswers && (

<div className="response">

<ReactMarkdown>

{answers}

</ReactMarkdown>

</div>

)}

<button onClick={downloadQuiz}>

⬇ Download Quiz

</button>

</>

)}

</div>

);

}

export default Quiz;