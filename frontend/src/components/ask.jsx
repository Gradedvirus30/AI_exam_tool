import axios from "axios";
import {useState} from "react";

function Ask(){

const [question,setQuestion]=useState("");

const [answer,setAnswer]=useState("");


const askQuestion=async()=>{

try{

const response=
await axios.post(

"http://127.0.0.1:8000/ask",

{

question:question

}

);

setAnswer(
response.data.answer
);

}

catch{

setAnswer(
"Failed"
);

}

};


return(

<div className="card">

<h3>Ask Question</h3>

<input

type="text"

placeholder="Ask from notes..."

value={question}

onChange={(e)=>
setQuestion(
e.target.value
)
}

/>

<button
onClick={askQuestion}
>

Ask

</button>

<p>

{answer}

</p>

</div>

);

}

export default Ask;