import chatPage from "./pages/chatPage.js"
import knowledges from "./pages/knowledges.js"
import notFound from "./pages/notFound.js"

export const app_routes = [
    { path: '/chapp', name: "chatPage", component: chatPage },
    { path: '/chapp/knowledges', name: "knowledges", component: knowledges },
    { path: '/chapp/:pathMatch(.*)*', name: 'notFound', component: notFound },
]

export const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes: app_routes, 
})