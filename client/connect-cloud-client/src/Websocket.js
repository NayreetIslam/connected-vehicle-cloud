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

  const write = (filename, content) => {
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
