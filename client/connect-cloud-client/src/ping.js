const ping = (address, callback) => {
  var xmlHttp = new XMLHttpRequest()
  var start = Date.now()
  xmlHttp.onreadystatechange = () => {
    if (xmlHttp.readyState === 4) {
      callback(Date.now() - start)
    }
  }
  xmlHttp.open('GET', address, true)
  xmlHttp.send(null)
}

export default ping
