// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: rectangle1
    width: 28
    height: 28
    radius: 6
    smooth: true
    border.width: 1
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

    MouseArea {
        id: mouse_area1
        anchors.fill: parent
    }

    Image {
        id: image1
        x: 0
        y: 0
        width: 20
        height: 20
        smooth: true
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        source: "images/gear.svg"
    }
}
