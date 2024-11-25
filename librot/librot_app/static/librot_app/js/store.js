const store = {
    
    //States
    state: Vue.reactive({
        testStoreText: "Froms store",
    }), 

    gettestStoreText() {
        return this.state.testStoreText
    },
}
export default store