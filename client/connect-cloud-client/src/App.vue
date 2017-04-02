<template>
  <div id='app'>
    <ServerStats v-for="server in servers" :server="server" :key="server.ws" />
  </div>
</template>

<script>
import ServerStats from './components/ServerStats'
import ping from './ping'

const servers = [
  {
    ws: 'ws://192.168.0.103:8765',
    http: 'http://192.168.0.103:8766',
    ping: 'http://192.168.0.103:8767'
  }
]

export default {
  name: 'app',
  components: {
    ServerStats
  },

  data () {
    return {
      servers
    }
  },

  methods: {
    pingAvailableServers () {
      return Promise.all(servers.map(server => {
        return new Promise((resolve, reject) => {
          ping(server.ping, responseTime => {
            this.log += server.ping + ' ' + responseTime + 'ms\n'
            return resolve({ws: server.ws, time: responseTime})
          })
        })
      }))
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
