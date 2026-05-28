import axios from "axios";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

function Flashcards(){

const [topic,setTopic]=useState("");
const [flashcards,setFlashcards]=useState("");

const generateFlashcards=async()=>{

const response=await axios.post(

"https://aiexamtool-production.up.railway.app/flashcards",

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

setFlashcards(
response.data.flashcards
);

};

const downloadFile=()=>{

const blob=new Blob(

[flashcards],

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

a.download="flashcards.txt";

a.click();

window.URL.revokeObjectURL(
url
);

};

return(

<div className="card">

<h3>Flashcards</h3>

<input
type="text"
placeholder="Enter topic"
value={topic}
onChange={(e)=>setTopic(e.target.value)}
/>

<button onClick={generateFlashcards}>

Generate

</button>

<div className="response">

<ReactMarkdown>

{flashcards}

</ReactMarkdown>

</div>

{flashcards && (

<button onClick={downloadFile}>

⬇ Download

</button>

)}

</div>

);

}

export default Flashcards;