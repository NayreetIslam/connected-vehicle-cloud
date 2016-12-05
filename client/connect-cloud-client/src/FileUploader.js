let filesInProgress = []

const FileUploader = websocket => {
  return {
    upload: file => {
      let reader = new FileReader()
      let rawData = new ArrayBuffer()
      filesInProgress.push(file)

      reader.loadend = () => {}
      reader.onload = (e) => {
        rawData = e.target.result
        websocket.letUserKnow({
          direction: 'out',
          data: 'Uploading file...'
        })
        websocket.send(rawData)
      }

      reader.readAsArrayBuffer(file)
    },

    finishUpload: command => {
      if (!filesInProgress.length) {
        return console.error('[ERROR] received ' + command.command_type + ', but filesInProgress is empty.')
      }
      const payload = {
        ext: `.${filesInProgress.splice(0, 1)[0].name.split('.').pop()}`
      }

      const data = {
        type: 'update',
        payload,
        filepath: command.filepath
      }

      websocket.letUserKnow({
        direction: 'out',
        data
      })
      websocket.send(JSON.stringify(data))
    }
  }
}

export default FileUploader
