function addAuthorization(headers) {
    if (localStorage.authToken)
        headers['Authorization'] = 'Bearer ' + localStorage.authToken;
    return headers;
}

function handleResponse(responsePromise) {
    return responsePromise
    .then(response => {
        if (response.ok)
            return response.json();
        else
            return null;
    })
    .catch(error => console.error(error));
}

export function post(url, data) {
    return handleResponse(
        fetch(url, {
            method: 'POST',
            headers: addAuthorization({
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }),
            body: JSON.stringify(data),
        })
    );
}

export function get(url) {
    return handleResponse(
        fetch(url, {
            headers: addAuthorization({})
        })
    );
}
