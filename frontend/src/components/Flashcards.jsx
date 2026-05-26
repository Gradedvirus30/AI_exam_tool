import axios from "axios";
import { useState } from "react";

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

🗂 Generate

</button>

<p>{flashcards}</p>

</div>

);

}

export default Flashcards;