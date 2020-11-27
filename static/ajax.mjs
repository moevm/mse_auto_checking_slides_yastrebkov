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

export function post(url, object, {onProgress} = {}) {
    // Old realization without onProgress support
    // return handleResponse(
    //     fetch(url, {
    //         method: 'POST',
    //         headers: addAuthorization({
    //             'Accept': 'application/json',
    //             'Content-Type': 'application/json',
    //         }),
    //         body: JSON.stringify(data),
    //     })
    // );

    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();

        xhr.open('POST', url);

        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300)
                resolve(JSON.parse(xhr.response));
            else
                resolve(null);
        };
        xhr.onerror = () => {
            reject(xhr.status,xhr.statusText);
        };
        if (onProgress)
            xhr.upload.onprogress = progressEvent =>
                onProgress(progressEvent.loaded / progressEvent.total);

        let headers = addAuthorization({'Content-Type': 'application/json'});
        for (let [headerName, headerValue] of Object.entries(headers))
            xhr.setRequestHeader(headerName, headerValue);

        xhr.send(JSON.stringify(object));
    })
    .catch(error => console.error(error));
}

export function get(url) {
    return handleResponse(
        fetch(url, {
            headers: addAuthorization({})
        })
    );
}
