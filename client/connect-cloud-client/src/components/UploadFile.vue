<template>
  <div id="uploadFile">
    <div v-if="!file">
      <h2>Select a file</h2>
      <input type="file" @change="onFileChange">
    </div>
  </div>
</template>

<script>

export default {
  name: 'UploadFile',
  data () {
    return {
      file: undefined,
    }
  },

  props: ['uploadFile'],

  methods: {
    onFileChange (e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      this.handleUpload(files[0])
    }
  }
}

</script>
