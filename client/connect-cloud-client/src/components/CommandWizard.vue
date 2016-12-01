<template>
  <div class="command-wizard">
    <div>
      <h4>Type</h4>
      <input type="radio" id="read" value="read" v-model="type">
      <label for="one">Read</label>
      <br>
      <input type="radio" id="write" value="write" v-model="type">
      <label for="two">Write</label>
    </div>
    <div>
      <h4>Payload</h4>
      <textarea cols="40" rows="10" id="payload" v-model="payload" />
    </div>
    <div>
      <h4>Extra parameters</h4>
      <div v-for="(item, index) in parameters">
        <ExtraParameterRow
          :value="item.value"
          :pkey="item.key"
          :index="index"
          :handleInput="handleExtraParamInput"
        />
      </div>
      <span class="add-row" v-on:click="addRow">+</span>
    </div>
    <button v-on:click="sendRequest">Send</button>
  </div>
</template>


<script>
import ExtraParameterRow from './ExtraParameterRow'

export default {
  name: 'CommandWizard',
  components: {
    ExtraParameterRow
  },

  props: ['websocket'],

  data () {
    return {
      type: 'write',
      payload: '',
      parameters: [{
        key: undefined,
        value: undefined
      }]
    }
  },

  methods: {

    // Sends a request to the connected server
    sendRequest () {
      let data = {
        type: this.type,
        payload: this.payload
      }
      this.parameters.forEach(param => {
        if (param.key !== 'payload' && param.key !== 'type') {
          data[param.key] = param.value
        }
      })

      if (this.type === 'write') {
        this.websocket.write(data.filename, data.payload)
      } else if (this.type === 'read') {
        this.websocket.read(data.payload)
      }
    },

    // Adds another Extra Parameter row
    addRow () {
      this.parameters.push([{
        key: undefined,
        value: undefined
      }])
    },

    // Handles extra parameter input for key and value for every single row
    handleExtraParamInput (e, index) {
      const inputFieldName = e.target.name
      const fieldValue = e.target.value
      if (inputFieldName.indexOf('key') > -1) {
        // update the key
        this.parameters[index].key = fieldValue
      } else if (inputFieldName.indexOf('value') > -1) {
        // update the value
        this.parameters[index].value = fieldValue
      }
    }
  }
}
</script>

<style>
.command-wizard {
  text-align: left;
  max-width: 400px;
  min-width: 320px;
  margin: 20px;
}

.add-row {
  cursor: pointer;
  float: right;
  top: -22px;
  position: relative;
}
</style>
