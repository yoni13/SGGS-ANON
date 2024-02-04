send_email_code = document.getElementById('send_email_code');


send_email_code.onclick = function() {
    fetch('/send_email_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'email': document.getElementById('email').value,
        })
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        if (data['status'] == 200) {
            alert('验证码发送成功');
        } else {
            alert(data['msg']);
        }
    });
}