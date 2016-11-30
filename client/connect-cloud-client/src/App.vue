<template>
  <div id="app">
    <ServerLog v-bind:log="log"></ServerLog>
  </div>
</template>

<script>
import ServerLog from './components/ServerLog'
import Websocket from './Websocket'

export default {
  name: 'app',
  components: {
    ServerLog
  },

  data () {
    return {
      log: '',
      websocket: undefined
    }
  },

  created () {
    this.websocket = Websocket(this.onMessageReceive)
    setTimeout(() => this.websocket.write('helloooo.txt', 'bye.'), 2000)
    setTimeout(() => this.websocket.read('helloooo.txt'), 3000)
    // setInterval(this.ping, 1000)
  },

  methods: {
    ping () {
      this.log += 'pinging 192.168.1.1\n'
    },
    onMessageReceive (data) {
      if (data.direction === 'in') {
        this.log += '>>> Received response\n'
      } else if (data.direction === 'out') {
        this.log += '<<< Send request\n'
      }
      this.log += JSON.stringify(data.data, null, 2) + '\n\n'
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
