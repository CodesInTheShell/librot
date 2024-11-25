import store from "../store.js"
import { sendPromptApi } from "../apiCalls/messages.js"

export default {
    props: [],
    emits: [],
    data(){
        return {
            navChoices: [
                {
                    menuName: 'Chapp',
                    menuKey: 'chatPage',
                    idx: 1,
                },
                {
                    menuName: 'Knowledges',
                    menuKey: 'knowledges',
                    idx: 2,
                },
            ],
        }
    },
    mounted(){
        
    },
    computed: {
    },
    methods: {
    },
    template: /*html*/`
        <div>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="container-fluid">
                    <a class="navbar-brand" href="#">Librot</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item" v-for="menu in navChoices" :key="menu.idx">
                            <router-link :to="{ name: menu.menuKey }" class="nav-link"> {{ menu.menuName }} </router-link>
                        </li>
                    </ul>
                    <form class="d-flex">
                        <a href="/logout" class="btn btn-outline-danger">Logout</a>
                    </form>
                    </div>
                </div>
            </nav>
        </div>
    `
}



   