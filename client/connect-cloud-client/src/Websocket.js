var WebSocket = window.WebSocket

const factory = onmessage => {
  var websocket = new WebSocket('ws://localhost:8765')

  function send (data) {
    onmessage({
      direction: 'out',
      data
    })
    websocket.send(JSON.stringify(data))
  }

  websocket.onmessage = e => {
    onmessage({
      direction: 'in',
      data: JSON.parse(e.data)
    })
  }

  const read = filename => {
    const data = {
      type: 'read',
      payload: filename
    }
    send(data)
  }

  const write = (filename, content) => {
    const data = {
      type: 'write',
      payload: content,
      filename
    }
    send(data)
  }

  return {
    read,
    write
  }
}

// export default websocket
export default factory
