export const addKnowledgeByData = (data) => {
    return axios.post('/knowledgeFromData/', data)
        .then((response) => {
            return response
        }).catch((e) => {
            return e
        })
}
export const listKnowledges = () => {    
    return axios.get('/knowledges/')
        .then((response) => {
            return response
        }).catch((e) => {
            return ''
        })
}

export const deleteKnowledge = (knowledge_id) => {
    return axios.delete('/knowledges/'+knowledge_id)
        .then((response) => {
            return response
        }).catch((e) => {
            return e
        })
}