const message = document.getElementsByClassName("message")[0];
const reaction_bar = document.getElementById("reaction");
// This handler will be executed every time the cursor
// is moved over a different list item

function reaction_handler(event){
  var rect = message.getBoundingClientRect();
  console.log(rect.top, rect.right, rect.bottom, rect.left);
 // https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect
 // we use left bottom
 // https://stackoverflow.com/questions/6802956/how-to-position-a-div-at-specific-coordinates
}


message.addEventListener("mouseover", reaction_handler);
