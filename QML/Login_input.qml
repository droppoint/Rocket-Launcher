// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: root
    width: 220
    height: 34
    radius: 6
    smooth: true
    border.color: "#cccccc"
    property url image_path: "images/login_input.svg"
    property string default_string: "Login"
    property bool edited: false
    // property bool focused: false
    property bool password: false
    property string text: text_input.text


    TextInput {
        id: text_input
        x: 43
        y: 5
        width: 177
        height: 26
        focus: root.focus
        color: "#999999"
        text: qsTr(default_string)
        echoMode: TextInput.Normal
        smooth: true
        selectByMouse: true
        horizontalAlignment: TextInput.AlignLeft
        font.family: "DejaVu Sans"
        font.pixelSize: 20
        onFocusChanged: if (root.state != 'edit') { root.state = 'edit'}
                        else { root.text = text_input.text }
    }
    Image {
        id: image
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
                target: text_input
                text: qsTr("")
                color: "#424242"
                echoMode: root.password ? TextInput.Password : TextInput.Normal
            }
        }
    ]
}
