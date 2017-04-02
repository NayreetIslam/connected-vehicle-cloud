<script>
import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

const assignProps = (object, props) => {
  Object.keys(props).map((key) => {
    const prop = props[key]
    if (prop instanceof Array) {
      object[key] = prop
    } else if (prop instanceof Object) {
      assignProps(object[key], prop)
    } else {
      object[key] = prop
    }
  })
  return object
}

export default Line.extend({
  mixins: [reactiveProp],
  props: ['options'],
  mounted () {
    this.renderChart(this.chartData, this.options)
  },
  watch: {
    options: function (newOptions) {
      const yAxes = JSON.parse(JSON.stringify(newOptions.scales.yAxes[0]))
      assignProps(this._chart.options.scales.yAxes[0], yAxes)
      this._chart.update()
    }
  }
})
</script>

<style scoped>
canvas {
  width: 100% !important;
  max-width: 1600px;
}
</style>
