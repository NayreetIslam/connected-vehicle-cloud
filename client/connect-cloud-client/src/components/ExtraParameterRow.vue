<template>
  <div class="extra-parameter-row">
    <input v-on:input="onInput" :name="'key-' + index" placeholder="Key" type="text" />
    <input v-on:input="onInput" :name="'value-' + index" placeholder="Value" type="text" />
  </div>
</template>

<script>
export default {
  name: 'ExtraParameterRow',
  props: ['pkey', 'value', 'index', 'handleInput'],

  methods: {
    onInput (e) {
      this.handleInput(e, this.index)
    }
  }
}
</script>
