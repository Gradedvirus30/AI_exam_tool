import axios from "axios";
import {useState} from "react";

function Quiz(){

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

setQuiz(
response.data.quiz
);

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
setTopic(e.target.value)
}
/>

<button onClick={generateQuiz}>
Generate
</button>

<p>{quiz}</p>

</div>

);

}

export default Quiz;