reaction_emotes = document.getElementsByClassName('reaction_emotes');

for (var i = 0; i < reaction_emotes.length; i++) {
    reaction_emotes[i].addEventListener('mouseover', function() {
        this.style.cursor = 'pointer';
        this.style.fontSize = '50px';
    })

    reaction_emotes[i].addEventListener('mouseout', function() {
        this.style.fontSize = '30px';
    })
    reaction_emotes[i].addEventListener('click', function() {
        fetch('/api/v1/reaction', {
            method: 'POST',
            body: JSON.stringify({
                reaction: this.innerHTML,
                post_id: this.parentElement.id
            })
        })
        .catch((error) => {
            alert('Error:', error);
          }
    )}
    )
}