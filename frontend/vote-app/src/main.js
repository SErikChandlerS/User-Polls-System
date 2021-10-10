import Vue from 'vue'
import App from './App.vue'
import router from "./router";

import BootstrapVue from "bootstrap-vue";
// import VeeValidate from "vee-validate";
import vuetify from '@/plugins/vuetify' // path to vuetify export

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
// Vue.use(VeeValidate);
Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  render: h => h(App),
}).$mount('#app')
