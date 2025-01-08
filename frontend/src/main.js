import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';

// Font Awesome Imports
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPaperPlane, faMicrophone, faMicrophoneSlash, faChevronRight, faChevronLeft, faChartBar, faComments, faVial, faHouse, faUserMd } from '@fortawesome/free-solid-svg-icons';

const app = createApp(App)

library.add(
    faPaperPlane,
    faMicrophone,
    faMicrophoneSlash,
    faChevronRight,
    faChevronLeft,
    faChartBar,
    faComments,
    faVial,
    faHouse,
    faUserMd
);

app.component('font-awesome-icon', FontAwesomeIcon)

app.use(createPinia())
app.use(router)

app.mount('#app')
