export const createNewMessageThread = (data) => {
    return axios.post('/message_threads/', data)
        .then((response) => {
            return response
        }).catch((e) => {
            return e
        })
}

export const deleteMessageThread = (threadId) => {
    return axios.delete('/message_threads/'+threadId)
        .then((response) => {
            return response
        }).catch((e) => {
            return e
        })
}

export const listMessageThreads = () => {    
    return axios.get('/message_threads/')
        .then((response) => {
            return response
        }).catch((e) => {
            return ''
        })
}

export const sendPromptApi = (data) => {
    return axios.post('/receive_prompt/', data)
        .then((response) => {
            return response
        }).catch((e) => {
            return e
        })
}

export const listMessageHistory = (threadId) => {    
    return axios.get('/message/'+threadId)
        .then((response) => {
            return response
        }).catch((e) => {
            return ''
        })
}