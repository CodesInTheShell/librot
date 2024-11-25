import store from "../store.js"
import chatCol from '../components/chatCol.js'
import { createNewMessageThread } from "../apiCalls/messages.js";
import { listMessageThreads, listMessageHistory, deleteMessageThread } from "../apiCalls/messages.js"

export default {
    data(){
        return {
            selectedChatThreadId: null,
            selectedChatThreadName: '',
            threadNameInput: '',
            messageThreads: [],
            chatHistory: [],
            chatReferences: [],
        }
    },
    mounted(){
        this.loadMessageThreads()
        
    },
    computed: {
    },
    methods: {
        createNewMessageThreadBtn() {
            var params = { 'name': this.threadNameInput}
            createNewMessageThread(JSON.stringify(params))
            .then(function(response){
                if (response){
                    console.log('response: ', response.data )
                    this.selectedChatThreadId = response.data.message_thread_id
                    this.selectedChatThreadName = response.data.message_thread_name
                    this.loadMessageThreads()
                    this.loadChatHistory(this.selectedChatThreadId)
                }
            }.bind(this)
        )},

        loadMessageThreads () {
            listMessageThreads().then(function (response) {
                this.messageThreads = response.data.data
            }.bind(this))
        },

        showCreateThread() {
            this.selectedChatThreadId = null
            this.threadNameInput = ''
        },

        setThreadId(id, name) {
            this.selectedChatThreadId = id
            this.selectedChatThreadName = name
            this.chatReferences = []
            this.loadChatHistory(id)
        },

        loadChatHistory(id){
            console.log('loadChatHistory: ', id)
            listMessageHistory(id).then(function (response) {
                this.chatHistory = response.data.data
            }.bind(this))
        },

        reponseWasReceived(responseData){
            console.log('reponseWasReceived: ', responseData)
            if ('referencesResponse' in responseData) {
                this.chatReferences = responseData.referencesResponse
            }
            this.loadChatHistory(this.selectedChatThreadId)
        },

        deleteThread(threadId){
            deleteMessageThread(threadId).then(function (response) {
                this.showCreateThread()
                this.loadMessageThreads()
            }.bind(this))
        }

    },
    components: {        
        'chat-col': chatCol,
    },

    template: /*html*/`
        <div class="row pe-4">
            <div class="col-md-2 py-4 bg-light">
                <button type="button" class="btn btn-success my-2" @click="showCreateThread">Create new chat <span class="material-icons ms-2">add_box</span></button>
                <hr>
                <p v-for="(thread, index) in messageThreads" :key="index" @click="setThreadId(thread.id, thread.name)" :class="{ 'border border-2 border-success rounded':thread.id === this.selectedChatThreadId }">{{thread.name}} <span class="material-icons float-end text-danger" @click="deleteThread(thread.id)">delete</span></p>
            </div>
            <div class="col-md-10">
                <div v-if="selectedChatThreadId === null" class="row">
                    <div class="col-md-6">
                        <div class="input-group input-group-lg">
                            <span class="input-group-text" id="inputGroup-sizing-lg">Thread name</span>
                            <input v-model="threadNameInput" type="text" class="form-control" aria-label="" aria-describedby="inputGroup-sizing-lg">
                        </div>
                        <p class="text-muted">Select message thread on the left pane or create a new one.</p>
                        <button type="button" class="btn btn-primary mt-2" @click="createNewMessageThreadBtn">Create and start a new chat</button>
                    </div>
                    <div class="col-md-6"></div>
                </div>
                <div v-else class="row">
                    <div class="col-md-4 border rounded border-dark scrollable-div-chat-history-col p-4">
                        <strong>Chat history</strong>
                        <hr>
                        <div v-for="(chat, index) in chatHistory" :key="index" class="border rounded bg-light m-2 p-2 scrollable-div-chat-box" :class="{ 'border-info me-4':chat.role === 'user', 'border-warning ms-4':chat.role === 'bot'}">{{chat.message}}</div>
                    </div>
                    <div class="col-md-4 border rounded border-dark">
                        <chat-col
                        :selectedChatThreadId="selectedChatThreadId"
                        @reponse-received="reponseWasReceived"
                        >
                        </chat-col>
                    </div>
                    <div class="col-md-4 border rounded border-dark scrollable-div-chat-history-col p-4">
                        <strong>Knowledge references</strong>
                        <hr>
                        <p v-for="(chatReference, index) in chatReferences" :key="index" class="border border-2 border-success rounded me-4 p-2">{{chatReference.text}}</p>
                    </div>
                </div>
            </div>
        </div>



        
    `
}



   