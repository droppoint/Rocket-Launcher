// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

 Item {
     id: toggleswitch
     width: background.width; height: background.height

     property bool on: false

     function toggle() {
         if (toggleswitch.state == "on")
             toggleswitch.state = "off";
         else
             toggleswitch.state = "on";
     }

     function releaseSwitch() {
         if (knob.x == 1) {
             if (toggleswitch.state == "off") return;
         }
         if (knob.x == 78) {
             if (toggleswitch.state == "on") return;
         }
         toggle();
     }

     Image {
         id: background
         source: "images/background.svg"
         MouseArea { anchors.fill: parent; onClicked: toggle() }
     }

     Image {
         id: knob
         x: 1; y: 2
         source: "images/knob.svg"

         MouseArea {
             anchors.fill: parent
             drag.target: knob; drag.axis: Drag.XAxis; drag.minimumX: 1; drag.maximumX: 78
             onClicked: toggle()
             onReleased: releaseSwitch()
         }
     }

     states: [
         State {
             name: "on"
             PropertyChanges { target: knob; x: 78 }
             PropertyChanges { target: toggleswitch; on: true }
         },
         State {
             name: "off"
             PropertyChanges { target: knob; x: 1 }
             PropertyChanges { target: toggleswitch; on: false }
         }
     ]

     transitions: Transition {
         NumberAnimation { properties: "x"; easing.type: Easing.InOutQuad; duration: 200 }
     }
 }
