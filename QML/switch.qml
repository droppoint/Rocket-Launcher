// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item {
	id: root
    width: 80
    height: 28
    clip: false
    state: "off"
    property bool checked: false
	
	MouseArea {
		id: mousearea
		anchors.fill: parent
		onClicked: {
			if (root.state === "on"){	
				root.state = "off"
			} else {
				root.state = "on"
			}
		}
		
		
	    Image {
	        id: mask
	        x: 0
	        y: 0
	        width: 80
	        height: 28
         fillMode: Image.Stretch
	        z: 1
            source: "mask.png"
	    }
	
	    Flickable {
	        id: background
	        contentWidth: 128
            contentHeight: 28
	        interactive: false
	        x: 0
	        y: 0
	        width: parent.width
	        height: parent.height
            clip: true
	
	        Image {
	            id: background_image
	            x: 0
	            y: 0
	            width: 128
	            fillMode: Image.Stretch
	            source: "switch.svg"
                height: 28
                smooth: true
                z: 0
	        }
        }

        Item {
            id: knob
            x: 48
            y: -1.5
            width: 36
            height: 32
            z: 2

            Image {
                id: knob_image
                x: 0
                y: 0
                width: parent.width
                height: parent.height
                smooth: true
                source: "knob.png"
            }
        }
	
	    
	 }
	 states: [
        State { 
        	name: "on"
            PropertyChanges{ target: background; contentX: "0"}
            PropertyChanges{ target: knob; x: 48 }
            PropertyChanges{ target: root; checked: true }
        },
        State {
        	name: "off"
        	PropertyChanges{ target: background; contentX: "48"}
            PropertyChanges{ target: knob; x: -2 }
            PropertyChanges{ target: root; checked: false }
        }
     ]
     transitions: Transition {
     	reversible: true
     	PropertyAnimation {
     		target: background
     		property: "contentX"
     		duration: 200
     		easing.type: Easing.InSine
        }
        PropertyAnimation {
            target: knob
            property: "x"
            duration: 200
            easing.type: Easing.InSine
        }
     }
	

}
