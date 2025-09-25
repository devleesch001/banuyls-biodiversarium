import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import mitt from 'mitt';
import { loadFonts } from './plugins/webfontloader'

loadFonts()
export const bus = createApp(null);

let app = createApp(App);
app.config.globalProperties.bus = mitt();
app.use(vuetify)
  .mount('#app')
