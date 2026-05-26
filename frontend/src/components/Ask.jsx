import axios from "axios";
import {useState} from "react";

function Ask(){

const [question,setQuestion]=useState("");

const [answer,setAnswer]=useState("");

const askQuestion=async()=>{

const response=await axios.post(

"https://aiexamtool-production.up.railway.app/ask",

{
question
},

{
headers:{

session_id:
localStorage.getItem(
"session_id"
)

}
}

);

setAnswer(
response.data.answer
);

};

return(

<div className="card">

<h3>Ask Questions</h3>

<input
type="text"
placeholder="Ask anything..."
value={question}
onChange={(e)=>setQuestion(e.target.value)}
/>

<button onClick={askQuestion}>

Ask

</button>

<p>

{answer}

</p>

</div>

);

}

export default Ask;