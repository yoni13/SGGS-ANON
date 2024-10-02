window.onload = () => {
    sessionStorage.setItem('page', 1);
}
let trigger_ = false
let addedmessage = 0


if (location.href.includes('mod')) {
    var mod = true
    var Hereurl = '/mod/moderation_posts?post_id='
}
else {
    var mod = false
    var Hereurl = '/messages_replys?post_id='
}


document.getElementsByTagName('body')[0].onscroll = () => {
    // console.log('scrolled');
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        console.log('bottom of page');
        let page = parseInt(sessionStorage.getItem('page')) + 1;
        if (trigger_ === false) {
            trigger_ = true
            fetch(`/api/v1/mb_board/?page=${page}&reverse=1`).then((response) => {
                return response.json();
            }).then((data) => {
                for (let i = 0; i < data.length; i++) {
                    let mb = document.createElement('div');
                    meselement = `
                        <div class="message">
                        <a class="messagelink" href="${Hereurl}${data[i].post_id}">
                        <div><img src="/static/img/default.png" class="profileimg"><span class="uname">${data[i].uname}</span>
                        <br><br>
                        <span class="pub_time">${data[i].pub_time}</span></div>
                        <div class="content">${data[i].content}</div>
                        <p class="reply">回覆數:${data[i].replys_count}</p>`;
                    if (data[i].might_fake === true) {
                        meselement += `<p class="reply">管理員:此留言有部分可能具有爭議</p>`;
                    }
                    if (data[i].hidden === true) {
                        meselement += `<p class="reply">此回覆已被管理員隱藏</p>`;
                    }

                    meselement += '</a>';
                    if (mod === false) {
                        ractionelement = `
                <div class="reaction" id="${data[i].post_id}">
                <a class="reaction_emotes new${addedmessage.toString()}" id="like">👍${data[i].like}</a>
                <a class="reaction_emotes new${addedmessage.toString()}" id="dislike">👎${data[i].dislike}</a>
                <a class="reaction_emotes new${addedmessage.toString()}" id="laugh">🤣${data[i].laugh}</a>
                </div>
                `}
                    else {
                        ractionelement = ''
                    }

                    mb.innerHTML = meselement + ractionelement + `</div>`;


                    document.getElementById('message_area').appendChild(mb);

                    reaction_emotes = document.getElementsByClassName(`reaction_emotes new${addedmessage.toString()}`);
                    if (!mod) {
                        for (var r = 0; r < reaction_emotes.length; r++) {
                            reaction_emotes[r].addEventListener('mouseover', function () {
                                this.style.cursor = 'pointer';
                                this.style.fontSize = '50px';
                            })

                            reaction_emotes[r].addEventListener('mouseout', function () {
                                this.style.fontSize = '30px';
                            })
                            reaction_emotes[r].addEventListener('click', function () {
                                fetch('/api/v1/reaction', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'x-csrf-token': document.getElementById('csrf_token').value
                                    },
                                    body: JSON.stringify({
                                        reaction: this.id,
                                        post_id: this.parentElement.id
                                    })
                                })
                                    .then((response) => response.json())
                                    .then((data) => {
                                        if (data['err'] === 1) {
                                            alert(data['desc']);
                                            return;
                                        }
                                        this.parentElement.children[0].innerHTML = '👍' + data['reaction'][0]

                                        this.parentElement.children[1].innerHTML = '👎' + data['reaction'][1]

                                        this.parentElement.children[2].innerHTML = '🤣' + data['reaction'][2]
                                    })
                            })
                            addedmessage += 1
                        }
                    }


                }
                if (data.length === 0) {
                    document.getElementById('loading_text').innerHTML = '沒有更多東西了；('
                    document.getElementsByTagName('body')[0].onscroll = () => { }
                }
                else {
                    sessionStorage.setItem('page', page)
                }
                trigger_ = false

            })
        }
    }
}