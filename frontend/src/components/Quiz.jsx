import axios from "axios";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

function Quiz(){

const [topic,setTopic]=useState("");
const [quiz,setQuiz]=useState("");

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

setQuiz(
response.data.quiz
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

🎯 Generate

</button>

<div className="response">

<ReactMarkdown>

{quiz}

</ReactMarkdown>

</div>

</div>

);

}

export default Quiz;