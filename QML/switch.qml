// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item {
    width: 80
    height: 28
    clip: false

    Image {
        id: mask
        x: 0
        y: 0
        width: 80
        height: 28
        z: 1
        source: "mask.svg"
    }

    Flickable {
        id: background
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
            height: 30
            fillMode: Image.Stretch
            source: "switch.svg"
            smooth: true
        }
    }

    Item {
        id: knob
        x: 47
        y: -0.500
        width: 33
        height: 30

        Image {
            id: knob_image
            x: 0
            y: 0
            width: parent.width
            height: parent.height
            smooth: true
            source: "knob.svg"
        }
    }




}
