<template>
  <div id="app">
    <ServerLog v-bind:log="log"></ServerLog>
  </div>
</template>

<script>
import ServerLog from './components/ServerLog'

export default {
  name: 'app',
  components: {
    ServerLog
  },

  data () {
    return {
      log: ''
    }
  },

  created () {
    setInterval(this.ping, 1000)
  },

  methods: {
    ping () {
      this.log += 'pinging 192.168.1.1\n'
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
