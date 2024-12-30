import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// Font Awesome Imports
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

const app = createApp(App)

library.add(
    faPaperPlane,
);

app.component('font-awesome-icon', FontAwesomeIcon)


app.use(router)

app.mount('#app')
