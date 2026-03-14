const Walker = require("../src/cube/walker")

const walker = new Walker(3)

const seq = walker.walk(50)

console.log("Sequence:")
console.log(seq.join(" "))
