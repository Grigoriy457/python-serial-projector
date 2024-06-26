var is_clicked_in_menu = false;


function set_settings() {
     var elem = document.getElementById("wrap");
     elem.style.fontSize = settings["font-size"];
     elem.style.color = settings["text-color"];
     elem.style.backgroundColor = settings["bg-color"];
}

function reset_settings() {
     settings = Object.assign({}, main_settings);
     document.getElementById("font-size").value = settings["font-size"].slice(0, -2);
     document.getElementById("text-color").value = settings["text-color"];
     document.getElementById("bg-color").value = settings["bg-color"];
     set_settings();
}

function clicked_on_menu() {
     is_clicked_in_menu = true;
}

function open_close_modal_settings(btn) {
     if (btn == null) {
          console.log(is_clicked_in_menu)
          if (is_clicked_in_menu) {
               is_clicked_in_menu = false;
               return;
          }
          for (var i of ["connection", "settings", "about"]) {
               document.getElementById(i).style.display = "none";
          }
          return;
     }
     is_clicked_in_menu = true;
     var name = btn.getAttribute("btn-name");
     
     var now_selected = null;
     for (var i of ["connection", "settings", "about"]) {
          if (document.getElementById(i).style.display == "block") {
               now_selected = i;
          }
          document.getElementById(i).style.display = "none";
     }

     if (now_selected == name) {
          document.getElementById(now_selected).style.display = "none";
          return;
     }

     if (name == "fullscreen") {

     } else if (name == "connection") {
          check_ports();
          document.getElementById("connection").style.display = "block";
     } else if (name == "settings") {
          document.getElementById("settings").style.display = "block";
     } else if (name == "about") {
          document.getElementById("about").style.display = "block";
     }
}

function check_ports() {
     eel.get_com_list()(function (ports) {
          var ports_elem = document.getElementById("port");
          ports_elem.disabled = false;
     
          for (var i of ports_elem.getElementsByTagName("option")) { i.remove(); }
          if (ports.length == 0) {
               var option = document.createElement("option")
               option.text = "No devices";
               option.value = "";
               ports_elem.add(option, null);
               ports_elem.disabled = true;
          } else {
               for (var i of ports) {
                    var option = document.createElement("option")
                    option.text = i;
                    option.value = i;
                    ports_elem.add(option, null);
               }
          }
     });
}

function connect() {
     port = document.getElementById("port").value;
     bitrate = document.getElementById("bitrate").value;
     dataBits = document.getElementById("dataBits").value;
     parityBit = document.getElementById("parityBit").value;
     stopBits = document.getElementById("stopBits").value;
     eel.py_connect(port, bitrate, dataBits, parityBit, stopBits)(function(ret) {
          if (ret == 1) {
               document.getElementById("connect").style.display = "none";
               document.getElementById("stop-connection").style.display = "block";
               for (var i of ["port", "bitrate", "dataBits", "parityBit", "stopBits"]) {
                    document.getElementById(i).disabled = true;
               }
          }
     });
}

function disconnect() {
     eel.py_disconnect()(function(ret) {
          if (ret == 1) {
               document.getElementById("connect").style.display = "block";
               document.getElementById("stop-connection").style.display = "none";
               document.getElementById("wrap").innerHTML = "<h1>disconnected</h1>"
               for (var i of ["port", "bitrate", "dataBits", "parityBit", "stopBits"]) {
                    document.getElementById(i).disabled = false;
               }
               check_ports();
          }
     });
}

eel.expose(device_lost);
function device_lost() {
     document.getElementById("connect").style.display = "block";
     document.getElementById("stop-connection").style.display = "none";
     document.getElementById("wrap").innerHTML = "<h1>device_lost</h1>";
     for (var i of ["port", "bitrate", "dataBits", "parityBit", "stopBits"]) {
          document.getElementById(i).disabled = false;
     }
     check_ports();
}

eel.expose(cant_connect);
function cant_connect(com_port) {
     document.getElementById("connect").style.display = "block";
     document.getElementById("stop-connection").style.display = "none";
     document.getElementById("wrap").innerHTML = `<h1>Connection failed</h1><h6>Can't open serial port ${com_port}.</h6><h6>Possibly it is already in use by another application.</h6>`;
     for (var i of ["port", "bitrate", "dataBits", "parityBit", "stopBits"]) {
          document.getElementById(i).disabled = false;
     }
     check_ports();
}

eel.expose(set_text);
function set_text(string) {
     document.getElementById("wrap").innerHTML = `<h1>${string}</h1>`;
}

eel.expose(close_window)
function close_window() {
    window.close()
}