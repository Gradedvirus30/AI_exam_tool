import axios from "axios";
import { useState } from "react";

function Quiz() {

const [topic,setTopic]=useState("");

const [quiz,setQuiz]=useState("");

const generateQuiz=async()=>{

try{

const response=
await axios.post(
"http://127.0.0.1:8000/quiz",
{
topic:topic
}
);

let text=response.data.quiz;

text=text

.replace(/MCQ\s*\d+/g,"\n\n$&")

.replace(/Short Question\s*\d*/g,"\n\n$&")

.replace(/Long Question/g,"\n\nLong Question")

.replace(/A\)/g,"\nA)")

.replace(/B\)/g,"\nB)")

.replace(/C\)/g,"\nC)")

.replace(/D\)/g,"\nD)");

setQuiz(text);

}

catch{

setQuiz(
"Failed"
);

}

};


return(

<div className="card">

<h3>Quiz</h3>

<input

type="text"

placeholder="Enter topic..."

value={topic}

onChange={(e)=>
setTopic(
e.target.value
)
}

/>

<button
onClick={askQuestion}
disabled={loading}
>

{loading
?
"⏳ Generating..."
:
"❓ Ask"}

</button>


<div className="response-box">

<pre>

{quiz}

</pre>

</div>

</div>

);

}

export default Quiz;