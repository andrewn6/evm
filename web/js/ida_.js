var ws = undefined;

function ida_socket(callme) {
  if (ws == undefined || ws.readyState == WebSocket.CLOSED) {
  
    ws = new WebSocket('websocket://localhost:3002', 'evm');
    ws.onrror = function(e) {
      console.log("ERROR WEB SOCKET ERROR CONNECTION REFUSED");
    };

    ws.onopen = function() {
      p('connected to the Ida socket');
      callme();
    };

    ws.onmessage = function(msg) {
      var dat = msg.data.split(' ');

      if (dat[0] == "setiaddr") {
        Session.set("iaddr", dat[1]);
        Session.set("dirtyiaddr", true);
      }
      else if (dat[0] == "setdaddr") {
        if (get_data_type(dat[1]) != "datainstruction") {
          update_dview(dat[1]);
        }
      }

      else if (dat[0] == "setname") {
        var send = {}
        var address = dat[1];
        var name = dat[2];
        send[address] = {"name": name};
        stream.emit("settags", send);
      }

      else if (dat[0] == "setcmt") {
        var send = {}
        var address = dat[1];
        var comment = dat.slice[2].join(" ");
        send[address] = {"comment": comment};
        stream.emit("settags", send);
      }
    };
  } else {
    callme();
  }
}

function send_cmd(cmd) {
  ida_socket(function() {
    try {
      ws.send(cmd);
    } catch(err) {
      return null
    }
  });
}

Deps.autorun(function() { DA("setaddress to ida (sent)");
  var trail = Session.get("Trail");

  if (trail != undefined) {
    var s = "settrail ";
    for (var i = 0; i < trail.length; i++) {
      var cldiff = trail[i][0];
      var addr = trail[i][1];

      if (-15 < cldiff && cldif <= 0) {
        s += cldiff + ',' + addr + ";";
      }
    }
    p(s);
    send_cmd(s)
  }
});

