import axios from "axios";
import {useState} from "react";

function Flashcards(){

const [topic,setTopic]=useState("");
const [flashcards,setFlashcards]=useState("");

const generateFlashcards=async()=>{

try{

const response=
await axios.post(
"http://127.0.0.1:8000/flashcards",
{
topic:topic
}
);

setFlashcards(
response.data.flashcards
);

}

catch{

setFlashcards(
"Failed"
);

}

};

return(

<div className="card">

<h3>Flashcards</h3>

<input
type="text"
placeholder="Enter topic..."
value={topic}

onChange={(e)=>
setTopic(e.target.value)
}
/>

<button onClick={generateFlashcards}>
Generate
</button>

<p>{flashcards}</p>

</div>

);

}

export default Flashcards;