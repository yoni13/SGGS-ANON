reaction_emotes = document.getElementsByClassName('reaction_emotes');

for (var i = 0; i < reaction_emotes.length; i++) {
    reaction_emotes[i].addEventListener('mouseover', function () {
        this.style.cursor = 'pointer';
        // if screen < 700px, change font size to 36
        if (window.innerHeight < 400) {
            this.style.fontSize = '35px';
        }
        else { this.style.fontSize = '50px'; }
    })

    reaction_emotes[i].addEventListener('mouseout', function () {
        this.style.fontSize = '30px';
    })
    reaction_emotes[i].addEventListener('click', function () {
        fetch('/api/v1/reaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.parentElement.children[0].value
            },
            body: JSON.stringify({
                reaction: this.id,
                post_id: this.parentElement.id
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data['err'] === 1) {
                    alert(data['desc']);
                    return;
                }
                this.parentElement.children[1].innerHTML = '👍' + data['reaction'][0]
                this.parentElement.children[2].innerHTML = '👎' + data['reaction'][1]
                this.parentElement.children[3].innerHTML = '🤣' + data['reaction'][2]
            })
            .catch((error) => {
                alert(`Error:請稍後再試一次`);
            });
    })
}
