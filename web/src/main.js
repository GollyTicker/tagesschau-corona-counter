import {createApp} from 'vue'
import App from './App.vue'

const app = createApp(App)
app.productionTip = false;
app.mount('#app')
