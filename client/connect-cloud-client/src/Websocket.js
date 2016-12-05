var WebSocket = window.WebSocket

const factory = onmessage => {
  let websocket = new WebSocket('ws://localhost:8765')
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

    if (pingMS) {
      onmessage({
        ping: pingMS
      })
      pingMS = 0
      pingStart = undefined
    }
  }

  const read = filename => {
    const data = {
      type: 'read',
      payload: filename
    }
    send(data)
  }

  const uploadFile = file => {
    var reader = new FileReader()
    var rawData = new ArrayBuffer()

    reader.loadend = () => {

    }
    reader.onload = (e) => {
      rawData = e.target.result
      console.log(rawData)
      websocket.send(rawData)
      alert('the File has been transferred.')
    }

    reader.readAsArrayBuffer(file)
  }

  const write = (filename, content, file) => {
    if (file) return uploadFile(file)
    const data = {
      type: 'write',
      payload: content,
      filename
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

  return {
    read,
    write,
    ping
  }
}

// export default websocket
export default factory
