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
        if (data['err'] == 0) {
            alert('驗證碼已發送到您的郵箱，請查收');
        } else {
            alert('發送失敗');
        }
    });
}