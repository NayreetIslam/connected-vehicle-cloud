<template>
  <div id="app">
    <CommandWizard v-bind:websocket="websocket" />
    <ServerLog v-bind:log="log"></ServerLog>
  </div>
</template>

<script>
import ServerLog from './components/ServerLog'
import CommandWizard from './components/CommandWizard'
import Websocket from './Websocket'

export default {
  name: 'app',
  components: {
    ServerLog,
    CommandWizard
  },

  data () {
    return {
      log: '',
      websocket: undefined
    }
  },

  created () {
    this.websocket = Websocket(this.onMessageReceive)
    setTimeout(this.websocket.ping, 2000)
  },

  methods: {
    ping () {
      this.log += 'pinging 192.168.1.1\n'
    },
    onMessageReceive (data) {
      if (data.ping) {
        this.log += `\n\n>>>> Server Response Time: ${data.ping}ms <<<<\n\n`
        return
      } else if (data.direction === 'in') {
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
  display: flex;
}
</style>
