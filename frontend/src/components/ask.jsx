import axios from "axios";
import { useState } from "react";

function Ask(){

const [question,setQuestion]=useState("");

const [answer,setAnswer]=useState("");

const [loading,setLoading]=useState(false);


const askQuestion=async()=>{

setLoading(true);

try{

const response=
await axios.post(

"https://aiexamtool-production.up.railway.app/ask",

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
"Failed to generate answer"
);

}

setLoading(false);

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

disabled={loading}

>

{

loading

?

"⏳ Generating..."

:

"❓ Ask"

}

</button>


<div className="response-box">

<pre>

{answer}

</pre>

</div>

</div>

);

}

export default Ask;