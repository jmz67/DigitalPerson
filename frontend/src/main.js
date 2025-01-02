import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// Font Awesome Imports
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPaperPlane, faMicrophone, faMicrophoneSlash } from '@fortawesome/free-solid-svg-icons';

const app = createApp(App)

library.add(
    faPaperPlane,
    faMicrophone,
    faMicrophoneSlash
);

app.component('font-awesome-icon', FontAwesomeIcon)


app.use(router)

app.mount('#app')
