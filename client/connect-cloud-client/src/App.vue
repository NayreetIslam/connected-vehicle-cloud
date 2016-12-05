<template>
  <div id="app">
    <CommandWizard v-bind:websocket="websocket" />
    <ServerLog v-bind:log="log"></ServerLog>
    <RenderFile
      :uri="file ? file.uri : undefined"
      :type="file ? file.type : undefined"
    />
  </div>
</template>

<script>
import ServerLog from './components/ServerLog'
import CommandWizard from './components/CommandWizard'
import Websocket from './Websocket'
import RenderFile from './components/RenderFile'
import ping from './ping'

const servers = [
  {
    ws: 'ws://connected-vehicle-cloud-server.cloudapp.net:8765',
    http: 'http://connected-vehicle-cloud-server.cloudapp.net:8766'
  },
  {
    ws: 'ws://localhost:8765',
    http: 'http://localhost:8766'
  }
]

export default {
  name: 'app',
  components: {
    ServerLog,
    CommandWizard,
    RenderFile
  },

  data () {
    return {
      log: '',
      websocket: undefined,
      file: undefined
    }
  },

  created () {
    const promises = servers.map(server => {
      return new Promise((resolve, reject) => {
        ping(server.http, responseTime => {
          this.log += server.http + ' ' + responseTime + 'ms\n'
          return resolve({ws: server.ws, time: responseTime})
        })
      })
    })

    Promise.all(promises)
    .then(responseTimes => {
      let closestServer
      responseTimes.forEach(server => {
        if (!closestServer) {
          closestServer = server
          return
        }
        if (server.time < closestServer.time) {
          closestServer = server
          return
        }
      })

      this.log += '\nConnecting to ' + closestServer.ws
      this.websocket = Websocket(this.onMessageReceive, closestServer.ws)
    })
  },

  methods: {
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

      if (data.data && data.data.payload && data.data.payload.uri) {
        this.file = data.data.payload
      }
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
