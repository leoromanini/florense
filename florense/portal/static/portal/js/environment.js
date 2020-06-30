async function setEnvironment(cidade){
    const data = {
        'environment': cidade,
        }
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(data)
        };
    const response = await fetch('/set_environment', options);
    const json = await response.json();
    window.location.href = json['href'];
}

function setEnvironmentf(){
    const data = {
        'environment': 'brasilia',
        }
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(data)
    };
    fetch('/set_environment', options).then(response => {
        console.log(response.href);
    });
}