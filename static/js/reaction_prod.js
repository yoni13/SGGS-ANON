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
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                reaction: this.id,
                post_id: this.parentElement.id
            })
        })
        .then((response) => response.json())
        .then((data) => {
            this.parentElement.children[0].innerHTML = '👍' + data['reaction'][0]
            
            this.parentElement.children[1].innerHTML = '👎' + data['reaction'][1]
            
            this.parentElement.children[2].innerHTML = '🤣' + data['reaction'][2]
        })
        // .catch((error) => {
        //     alert('Error:', error);
        //   
    })}
    