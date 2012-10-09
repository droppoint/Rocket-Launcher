// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: rectangle1
    width: 14
    height: 14
    radius: 2
    border.color: "#c3c3c3"
    gradient: Gradient {
        GradientStop {
            position: 0
            color: "#ffffff"
        }

        GradientStop {
            position: 1
            color: "#e6e6e6"
        }
    }
    smooth: true
    clip: true
    state: "off"

    Image {
        id: image1
        x: 1
        y: 1
        width: 13
        height: 12
        smooth: true
        sourceSize.height: 12
        sourceSize.width: 13
        source: "images/check.svg"
    }

    states: [
        State{
            name: "on"
            when: mouse_area1.pressed
            PropertyChanges {target: flickable1; contentX: 48}
        },
        State {
            name: "off"
            PropertyChanges {target: flickable1; contentX: 0}

            PropertyChanges {
                target: rectangle1
                visible: true
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        }
    ]

}
