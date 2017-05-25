const WebSocket = window.WebSocket
import FileUploader from './FileUploader'

const factory = (onmessage, address) => {
  let websocket = new WebSocket(address)
  websocket.letUserKnow = onmessage
  const fileUploader = FileUploader(websocket)
  let pingMS = 0
  let pingStart

  function send (data) {
    onmessage({
      direction: 'out',
      data
    })
    websocket.send(JSON.stringify(data))
  }

  websocket.onmessage = e => {
    const data = JSON.parse(e.data)
    if (data.payload === 'pong') {
      pingMS = Date.now() - pingStart
    }
    onmessage({
      direction: 'in',
      data
    })

    // Check for command type to see if client is required to execute anything
    if (data.payload && data.payload.command_type) {
      if (data.payload.command_type === 'FILE_UPLOAD_COMPLETE') {
        // Save the file extension of the file
        fileUploader.finishUpload(data.payload)
      }
    }

    if (pingMS) {
      onmessage({
        ping: pingMS
      })
      pingMS = 0
      pingStart = undefined
    }
  }
  websocket.onclose = () => {
    setTimeout(() => factory(onmessage, address), 1000)
  }

  const read = filename => {
    const data = {
      type: 'read',
      payload: filename
    }
    send(data)
  }

  const write = (filename, content, file) => {
    if (file) return fileUploader.upload(file)
    const data = {
      type: 'write',
      payload: content,
      filename
    }
    send(data)
  }

  const listdir = () => {
    const data = {
      type: 'listdir'
    }
    send(data)
  }

  const ping = () => {
    const data = {
      type: 'ping'
    }
    pingMS = 0
    pingStart = Date.now()
    send(data)
  }

  const carController = (payload) => {
    const data = {
      type: 'car_controller',
      timestamp: Date.now(),
      level: 'CRITICAL',
      payload
    }

    send(data)
  }

  return {
    read,
    write,
    ping,
    listdir,
    carController
  }
}

// export default websocket
export default factory
