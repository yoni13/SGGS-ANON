HideBtn = document.getElementsByClassName('HideBtn')[0];

HideBtn.onclick = function () {
    fetch(location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-csrf-token': document.getElementById('csrf_token').value
        },
        body: JSON.stringify({
            'action': 'hide'
        })
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        if (data['err'] == 0) {
            alert('修改成功');
            location.reload();
        } else {
            alert('修改失敗');
            alert(data['desc']);
        }
    });
}

markBtn = document.getElementsByClassName('MarkMightFakeBtn')[0];

markBtn.onclick = function () {
    fetch(location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-csrf-token': document.getElementById('csrf_token').value
        },
        body: JSON.stringify({
            'action': 'mark'
        })
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        if (data['err'] == 0) {
            alert('修改成功');
            location.reload();
        } else {
            alert('修改失敗');
            alert(data['desc']);
        }
    });
}