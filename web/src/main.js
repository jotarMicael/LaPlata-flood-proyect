import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router/index.js' 
import VueSweetalert2 from 'vue-sweetalert2'
import BootstrapVue3 from 'bootstrap-vue-3'

import "leaflet/dist/leaflet.css";
//import "bootstrap/dist/css/bootstrap.min.css"
//import "bootstrap"
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'


createApp(App).use(router).use(VueSweetalert2).use(BootstrapVue3).mount('#app')