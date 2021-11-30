stream = io.connect(STREAM_URL);

function on_set(iaddr) {
  DS("setiaddr");
  update_iaddr(iaddr);
} stream.on('setiaddr', on_setiaddr);

function on_setoperand(msg) { DS("setoperand");
  var operand = msg['operand']; 
  var forknum = msg['forknum'];
  var clnum = msg['clnum'];
  Session.set('forknum', forknum);
  Session.set('clnum', clnum);
  push_history('rempte setoperand;)
} stream.on('setoperand', iaddr);
