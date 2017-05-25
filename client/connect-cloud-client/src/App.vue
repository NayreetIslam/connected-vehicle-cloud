<template>
  <v-app id="sidebar-example-2" class="elevation-1" top-toolbar left-fixed-sidebar sidebar-under-toolbar>
    <v-toolbar class="secondary">
      <v-toolbar-side-icon @click.native.stop="sidebar2 = !sidebar2" />
      <v-toolbar-title>Connected Vehicle Cloud</v-toolbar-title>
    </v-toolbar>
    <div id='app' style="margin-top:0; padding: 20px;">
      <ServerStats v-for="server in servers" :server="server" :key="server.ws" />
    </div>
  </v-app>
</template>

<script>
import ServerStats from './components/ServerStats'
import ping from './ping'

const servers = [
  {
    ws: 'ws://192.168.0.115:8765',
    http: 'http://192.168.0.115:8766',
    ping: 'http://192.168.0.115:8767'
  }
]

export default {
  name: 'app',
  components: {
    ServerStats
  },

  data () {
    return {
      servers,
      items: [
        {
          title: 'Command Wizard'
        }
      ]
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
