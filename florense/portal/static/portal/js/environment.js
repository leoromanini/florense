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