import store from './store.js';
import { router } from './routes.js';
import navs from './components/navs.js';

const app = Vue.createApp({
    data(){
        return {
            message: 'Hehehe',
            st: store.gettestStoreText()
        }
    },
    components: {        
        'navMenus': navs,
    },
    
    template: /*html*/`
    <div>
        <navMenus></navMenus>
    </div>
    <div class="container-fluid">
        <router-view></router-view>
    </div>
    
    `
})
app.use(router).mount('#app')