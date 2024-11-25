import { addKnowledgeByData } from "../apiCalls/knowledges.js" 
import { listKnowledges, deleteKnowledge } from "../apiCalls/knowledges.js"

export default {
    data(){
        return {
            addByForm: '',
            knowledgeName: '',
            knowledgeDescription: '',
            knowledgeDataText: '',
            showLoading: false,
            showLoadingFileSend: false,
            botKnowledges: [],
            knowledgeNameFromFile: '',
            knowledgeDescriptionFromFile: '',
            fileToUpload: null,
        }
    },
    mounted(){
        this.addByForm = 'byDATA'
        this.loadKnowledges()
    },
    computed: {
    },
    methods: {
        sendKnowledge () {
            console.log('send')
            this.showLoading = true
            var params = { 'name': this.knowledgeName, 'description': this.knowledgeName, 'data': this.knowledgeDataText}
            params['advanceOptions'] = {
                    words_per_chunk: 50
                }
            console.log('params: ', params)
            addKnowledgeByData(JSON.stringify(params))
            .then(function(response){
                if (response){
                    console.log('response: ', response.data )
                    this.showLoading = false,
                    this.addByForm = 'byDATA'
                    this.knowledgeName = ''
                    this.knowledgeDescription = ''
                    this.knowledgeDataText = ''
                    this.loadKnowledges()
                }
            }.bind(this)
        )},

        loadKnowledges () {
            listKnowledges().then(function (response) {
                this.botKnowledges = response.data.data
            }.bind(this))
        },

        deleteKnowledge(knowledgeId){
            deleteKnowledge(knowledgeId).then(function (response) {
                this.loadKnowledges()
            }.bind(this))
        },

        selectAddBy (byWhat) {
            this.addByForm = byWhat
        },

        handleFileChange(event) {
            const file = event.target.files[0];
            this.fileToUpload = file;
        },

        async sendKnowledgeFromFile() {
            if (!this.fileToUpload) {
              console.error('No file selected');
              return;
            }
            this.showLoadingFileSend = true
      
            // Create a FormData object to store the file data
            const formData = new FormData();
            formData.append('knowledgeNameFromFile', this.knowledgeNameFromFile);
            formData.append('knowledgeDescriptionFromFile', this.knowledgeDescriptionFromFile);
            formData.append('file', this.fileToUpload);
      
            try {
              // Send a POST request to the Django backend with the file data
                const response = await axios.post('/add_knowledge_from_data_file/', formData, {
                    headers: {
                    'Content-Type': 'multipart/form-data'
                    }
                });
                console.log('Upload successful:', response.data);

                this.addByForm = 'byFILE'
                this.knowledgeNameFromFile = ''
                this.knowledgeDescriptionFromFile = ''
                this.$refs.knowledgeFileInputRef.value = null;
                this.loadKnowledges()
                
                this.showLoadingFileSend = false
            } catch (error) {
                this.showLoadingFileSend = false
              console.error('Upload failed:', error);
            }
          }
    },

    template: /*html*/`
    <div class="row pe-4">
        <div class="col-md-2 py-4 bg-light">
            <h4>Manage knowledges</h4>
            <hr>
            <p v-for="(botKnowledge, index) in botKnowledges" :key="index" >{{botKnowledge.name}} <span class="material-icons float-end text-danger" @click="deleteKnowledge(botKnowledge.id)">delete</span></p>
        </div>
        <div class="col-md-10">
            <h3>Add knowledge</h3>
            <p class="text-muted">Add and augment knowledge, Librot will use it as references on reponse</p>
            <hr>
            <p>Please select how you want to add knowledge.</p>
            <div class="my-4">
                <button type="button" @click="selectAddBy('byDATA')" class="btn btn-primary me-2">Data</button>
                <button type="button" @click="selectAddBy('byFILE')" class="btn btn-primary me-2">File upload</button>
                <button type="button" @click="selectAddBy('byURL')" class="btn btn-primary">URL</button>
            </div>
            <div v-if="addByForm === 'byDATA'">
                <h6>Adding knowledge by <span class="badge bg-info text-dark">Data</span></h6>
            </div>
            <div v-if="addByForm === 'byFILE'">
                <h6>Adding knowledge by <span class="badge bg-info text-dark">File</span></h6>
            </div>
            <div v-if="addByForm === 'byURL'">
                <h6>Adding knowledge by <span class="badge bg-info text-dark">Url</span></h6>
            </div>

            <div v-if="addByForm === 'byDATA'">
                <div class="p4 w-75">
                    <div class="input-group my-3">
                        <span class="input-group-text" id="basic-addon1">Name</span>
                        <input v-model="knowledgeName" type="text" class="form-control" aria-label="Knowledge" aria-describedby="basic-addon1">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">Description</span>
                        <textarea v-model="knowledgeDescription" class="form-control" aria-label="Description" rows="3"></textarea>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">Data article</span>
                        <textarea v-model="knowledgeDataText" class="form-control" aria-label="Data article" rows="10" placeholder="Paste your text here..."></textarea>
                    </div>
                    <div v-if="showLoading" class="float-end m-3">
                        <div class="spinner-border text-danger" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <span >Please wait...</span>
                    </div>
                    <button v-else @click="sendKnowledge" type="button" class="btn btn-success float-end ">Send</button>
                    
                </div>
            </div>
            <div v-if="addByForm === 'byFILE'">
                <div class="p4 w-75">
                    <div class="input-group my-3">
                        <span class="input-group-text" id="basic-addon2">Name</span>
                        <input v-model="knowledgeNameFromFile" type="text" class="form-control" aria-label="Knowledge" aria-describedby="basic-addon2">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">Description</span>
                        <textarea v-model="knowledgeDescriptionFromFile" class="form-control" aria-label="Description" rows="3"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="formFileSm" class="form-label">Please upload a file (txt or pdf )</label>
                        <input class="form-control form-control-sm" id="formFileSm" type="file" accept=".pdf,.txt" @change="handleFileChange" ref="knowledgeFileInputRef">
                    </div>
                    <div v-if="showLoadingFileSend" class="float-end m-3">
                        <div class="spinner-border text-danger" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <span >Please wait...</span>
                    </div>
                    <button v-else @click="sendKnowledgeFromFile" type="button" class="btn btn-success float-end ">Send</button>
                </div>
            </div>
            <div v-if="addByForm === 'byURL'">
                <div class="mb-3">
                    <label for="urlDataSource" class="form-label">Data will be fetched from the given url. As long as the site is publicly available.</label>
                    <input type="text" class="form-control" id="urlDataSource" placeholder="Paste here a url..." >
                </div>
            </div>
        </div>
    </div>
    `
}



   