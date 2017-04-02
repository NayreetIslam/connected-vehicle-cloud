<template>
  <div id='app'>
    <!-- <CommandWizard v-bind:websocket='websocket' /> -->
    <!-- <ServerLog v-bind:log='log'></ServerLog> -->
    <RenderFile
      :uri='file ? file.uri : undefined'
      :type='file ? file.type : undefined'
    />
    <LineChartComponent
      :chartData="accelerationData"
      :options="chartOptions()"
    />
  </div>
</template>

<script>
import ServerLog from './ServerLog'
import CommandWizard from './CommandWizard'
import Websocket from '../Websocket'
import RenderFile from './RenderFile'
import LineChartComponent from './LineChartComponent'

export default {
  name: 'ServerStats',
  props: ['server'],
  components: {
    ServerLog,
    CommandWizard,
    RenderFile,
    LineChartComponent
  },

  data () {
    return {
      log: '',
      websocket: undefined,
      file: undefined,
      accelerationData: {
        labels: [],
        datasets: [
          {
            label: 'Acceleration',
            data: [],
            fill: false
          }
        ]
      }
    }
  },

  created () {
    this.log += '\nConnecting to ' + this.server.ws + '\n'
    this.websocket = Websocket(this.onMessageReceive, this.server.ws)
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

      if (data.data && data.data.type === 'sensor_data') {
        // process sensor data
        const { payload } = data.data
        const sensorData = payload[0].split(',')

        let labels = [...this.accelerationData.labels]
        // set the timestamp, remove the year
        const maxPointCoint = 30
        labels.push(sensorData.slice(-1)[0].replace(/\d{4}-\d{2}-\d{2} /, ''))
        labels = labels.slice(-maxPointCoint)

        // add data
        const accX = sensorData[5]
        // const accY = sensorData[6]
        // const accZ = sensorData[7]

        const dataset = {
          label: 'Acceleration',
          data: [...this.accelerationData.datasets[0].data],
          fill: false
        }
        dataset.data.push(parseFloat(accX).toFixed(2))
        dataset.data = dataset.data.slice(-maxPointCoint)
        this.accelerationData = { labels, datasets: [dataset] }
      }
    },

    chartOptions () {
      const dataPoints = this.accelerationData.datasets[0].data.map(v => parseFloat(v))
      return {
        animation: false,
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            ticks: {
              min: dataPoints.length ? (Math.min(...dataPoints) - 0.5) : 0,
              max: dataPoints.length ? (Math.max(...dataPoints) + 0.5) : 0,
              stepSize: 0.05
            }
          }]
        }
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
