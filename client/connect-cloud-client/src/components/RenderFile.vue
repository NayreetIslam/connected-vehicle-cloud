<template>
  <div v-if="uri">
    <img v-if="type === 'image'" :src="uri" width=300 />
    <video v-if="type === 'video'" :src="uri" autoplay controls :type="'video/' + ext" />
    <audio v-if="type === 'audio'" :src="uri" autoplay controls />
  </div>
</template>

<script>
export default {
  name: 'RenderFile',
  props: ['type', 'uri'],

  computed: {
    ext () { return this.uri ? this.uri.split('.').slice(-1)[0] : undefined }
  }
}
</script>
