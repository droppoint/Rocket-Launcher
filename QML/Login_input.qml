// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: root
    width: 220
    height: 34
    color: "#ffffff"
    radius: 6
    smooth: true
    border.color: "#cccccc"
    property url image_path: "images/login_input.svg"
    property string default_string: "Login"
    property bool edited: false
    property bool password: false


    TextInput {
        id: text_input2
        x: 43
        y: 5
        width: 177
        height: 26
        color: "#999999"
        text: qsTr(default_string)
        smooth: true
        selectByMouse: true
        horizontalAlignment: TextInput.AlignLeft
        font.family: "DejaVu Sans"
        font.pixelSize: 20
        onFocusChanged: if (root.state != 'edit') { root.state = 'edit'}

    }

    Image {
        id: image1
        x: 0
        y: 0
        width: 35
        height: 35
        smooth: true
        source: root.image_path
    }
    states: [
        State {
            name: "edit"
            PropertyChanges {
                target: text_input2
                text: qsTr("")
                color: "#424242"
                echoMode: if( root.password ) {TextInput.Password}

            }
            PropertyChanges{
                target: root
                edited: true
            }
        }
    ]
}
