import Vue from 'vue'
import App from './App.vue'
import VueWamp from 'vue-wamp'

Vue.config.productionTip = false

Vue.use(VueWamp, {
  url: 'ws://localhost:8000/ws',
  realm: 'realm1',

  // change this in case of naming conflict
  namespace: 'wamp',
  // automatically re-registers and re-subscribes after reconnection (on by default)
  auto_reestablish: true,
  // automatically closes WS connection after amount of idle milliseconds (off by default)
  auto_close_timeout: -1
});

new Vue({
  render: h => h(App),
}).$mount('#app')
