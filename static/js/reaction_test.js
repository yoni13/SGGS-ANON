const message = document.getElementsByClassName("message")[0];
const reaction_bar = document.getElementById("reaction");


// This handler will be executed every time the cursor
// is moved over a different list item

function reaction_handler(event){
  var rect = message.getBoundingClientRect();
  reaction_bar.style.position = "absolute";
  reaction_bar.style.display = "block";
  reaction_bar.style.left = rect.left + "px";
  reaction_bar.style.top = rect.bottom - 150 + "px";
 
}


message.addEventListener("mouseover", reaction_handler);
message.addEventListener("mouseout", function(){
  reaction_bar.style.display = "none";
});




var messages = document.getElementsByClassName("reaction_emotes");
console.log('here');
for (var i = 0; i < messages.length; i++) {
      messages[i].addEventListener("mouseover", function() {
          this.style.fontSize = "50px";
      });

      messages[i].addEventListener("mouseout", function() {
          this.style.fontSize = "30px";
      });

      messages[i].addEventListener("click", function() {
          fetch('/api/v1/reaction', {
              method: 'POST',
              body: JSON.stringify({
                  reaction: this.innerHTML
              })
          })
      });
  }
