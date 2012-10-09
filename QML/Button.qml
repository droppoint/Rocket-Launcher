// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: root
    width: 140
    height: 30
    radius: 6
    signal btnClicked()
    property color top_color: "#0088cc"
    property color bottom_color: "#0044cc"
    property string default_string: "Text"
    gradient: Gradient {
        GradientStop {
            id: gradientstop1
            position: 0
            color: root.top_color
        }

        GradientStop {
            id: gradientstop2
            position: 1
            color: root.bottom_color
        }
    }
    border.color: "#64000000"
    smooth: true

    Text {
        id: button_text
        x: 0
        y: 0
        width: 140
        height: 30
        color: "#ffffff"
        text: qsTr(root.default_string)
        smooth: true
        style: Text.Normal
        styleColor: "#ffffff"
        font.family: "Arial"
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        font.pixelSize: 15
    }

    MouseArea {
        id: button_area
        x: 0
        y: 0
        width: 140
        height: 30
        hoverEnabled: true
        onClicked: btnClicked()

    }
    states: [
        State {
            name: "pressed"
            when: button_area.pressed
            PropertyChanges {
                target: gradientstop1
                color: root.bottom_color
            }
        },
        State {
            name: "hover"
            when: button_area.containsMouse
            PropertyChanges {
                target: gradientstop2
                position: 0.5
            }
        }
    ]
    transitions: [
        Transition {
            from: "hover"; to: "pressed"; reversible: true
            ColorAnimation { duration: 100 }
        },
        Transition {
            from: ""; to: "hover"; reversible: true
            PropertyAnimation { target: gradientstop2
                                      properties: "position"; duration: 100 }
         }

    ]
}
