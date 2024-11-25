import store from "../store.js"
import { sendPromptApi } from "../apiCalls/messages.js"

export default {
    props: ['selectedChatThreadId'],
    emits: ['reponse-received'],
    data(){
        return {
            promptInput: '',
            showLoading: false,
            knowledgeOnly: false,
            referencesResponse: [],
        }
    },
    mounted(){
        
    },
    computed: {
    },
    methods: {
        sendPrompt() {
            this.showLoading = true
            var params = { user_prompt: this.promptInput, threadId: this.selectedChatThreadId, knowledgeOnly: this.knowledgeOnly }
            console.log('sendPrompt: ', params )
            if (this.promptInput === '') {
                console.log('sendPrompt error: Please input a question ')
                return false
            }
            sendPromptApi(JSON.stringify(params))
            .then(function(response){
                if (response) {
                    console.log('response: ', response.data )
                    this.promptInput = ''
                    this.referencesResponse = response.data.references
                }
            }.bind(this))
            .finally(function() {
                this.showLoading = false
                this.$emit('reponse-received', {referencesResponse: this.referencesResponse})
            }.bind(this))
        }


        // )},

        
    },
    template: /*html*/`
        <div>
            <div class="mx-3 my-4">
                <textarea v-model="promptInput" class="form-control" id="promptTextarea1" rows="7" placeholder="Type in your question here..">
                </textarea>
            </div>
            

            <div v-if="showLoading" class="float-end m-3">
                <div class="spinner-border text-danger" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <span >Please wait...</span>
            </div>
            <div v-else class="float-end">
                <div class="form-check">
                    <input v-model="knowledgeOnly" class="form-check-input" type="checkbox" value="" id="cbKnowledgeOnly">
                    <label class="form-check-label" for="cbKnowledgeOnly">
                        Knowledge base only
                    </label>
                </div>

                <button type="button" class="btn btn-success my-2 " @click="sendPrompt">Send</button>
            </div>
        </div>
    `
}



   