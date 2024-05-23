window.onload = () => {
    sessionStorage.setItem('page', 1);
    
}
let trigger_ = false
document.getElementsByTagName('body')[0].onscroll = () => {
    // console.log('scrolled');
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight){
        console.log('bottom of page');
        let page = parseInt(sessionStorage.getItem('page')) + 1;
        if (trigger_ === false){
        trigger_ = true
        fetch(`/api/v1/mb_board/?page=${page}&reverse=1`).then((response) => {
            return response.json();
        }).then((data) => {
            console.log(data);
                
            for (let i = 0; i < data.length; i++){
                let mb = document.createElement('div');
                mb.innerHTML = `
                <div class="message">
                <a class="messagelink" href="messages_replys?post_id=${data[i].post_id}">
                <div><img src="/static/img/default.png" class="profileimg"><span class="uname">${data[i].uname}</span>
                <br><br>
                <span class="pub_time">${data[i].pub_time}</span></div>
                <p class="content">${data[i].content}</p>
                <p class="reply">回覆數:${data[i].replys_count}</p>
                </a>
                </div>`;
                document.getElementById('message_area').appendChild(mb);
            }
            if (data.length === 0){
                document.getElementById('loading_text').innerHTML = '沒有更多東西了；('
                document.getElementsByTagName('body')[0].onscroll = () => {}
            }
            else{
                sessionStorage.setItem('page',page)
            }
            trigger_ = false
        
    })}
}
}