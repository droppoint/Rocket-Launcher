// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: root
    width: 300
    height: 560
    color: "#e6e6e6"
    MouseArea {
        id: mousearea1
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
           // Qt.quit();
        }

        Flickable {
            id: control_flick
            x: 0
            y: 290
            height: 270
            contentWidth: 900
            contentHeight: 270
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.right: parent.right
            anchors.rightMargin: 0
            interactive: false

            Small_button {
                id: pref_button
                x: 18
                y: 227
                width: 28
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 15
            }

            Login_input {
                id: password_edit
                x: 40
                y: 130
                image_path: "images/password_input.svg"
                default_string: "Password"
                password: true
            }

            Login_input {
                id: login_edit
                x: 40
                y: 80
            }

            Button {
                id: connect_button
                x: 80
                y: 215
                default_string: "Подключение"
                anchors.horizontalCenterOffset: -300
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 28
                onBtnClicked: root.state = "connecting"
            }

            Text {
                id: rocket_one
                x: 10
                y: 14
                color: "#424242"
                text: qsTr("Rocket One")
                font.weight: Font.Light
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
                font.pixelSize: 40
            }

            Text {
                id: connecting
                x: 310
                y: 14
                color: "#424242"
                text: qsTr("Подключение")
                font.weight: Font.Light
                font.pixelSize: 40
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
            }

            Text {
                id: online
                x: 610
                y: 14
                color: "#424242"
                text: qsTr("В сети")
                font.pixelSize: 40
                font.weight: Font.Light
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
            }

            Text {
                id: con_status
                x: 310
                y: 80
                color: "#424242"
                text: qsTr("Соединение с сервером")
                font.pixelSize: 20
                font.weight: Font.Light
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
            }

            Progressbar {
                id: progress_wheel
                x: 420
                y: 139
                opacity: 0
            }

            Button {
                id: cancel_button
                x: 380
                y: 215
                top_color: "#EE5F5B"
                bottom_color: "#BD362F"
                default_string: "Отмена"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.horizontalCenterOffset: 0
                anchors.bottomMargin: 28
            }

            Button {
                id: cancel_button1
                x: 670
                y: 212
                top_color: "#EE5F5B"
                bottom_color: "#BD362F"
                default_string: "Отключить"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.horizontalCenterOffset: 290
                anchors.bottomMargin: 28
            }

            Text {
                id: con_status1
                x: 63
                y: 182
                color: "#424242"
                text: qsTr("Запомнить")
                font.pixelSize: 14
                font.weight: Font.Light
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
            }

            Sw {
                id: sw1
                x: 40
                y: 184
            }

        }

        Flickable {
            id: background_flick
            height: 380
            z: -2
            contentHeight: 380
            contentWidth: 600
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.right: parent.right
            anchors.rightMargin: 0

            Image {
                id: background
                x: 0
                y: 0
                width: 600
                height: 380
                z: -1
                source: "images/background2.svg"
            }
        }

        Text {
            id: credits
            x: 109
            y: 548
            width: 191
            height: 12
            color: "#424242"
            text: qsTr("Powered by Alfa & Pacha @ 2009")
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            font.family: "DejaVu Sans"
            font.pixelSize: 10
        }
    }
    states: [
        State {
            name: "connecting"
//            when: mousearea1.containsMouse
            PropertyChanges{
                target: control_flick
                contentX: "300"
            }
            PropertyChanges {
                target: background_flick
                contentX: "150"
            }

            PropertyChanges {
                target: progress_wheel
                x: 420
                y: 125
                opacity: 1
            }

        },
        State {
            name: "connected"
            PropertyChanges {
                target: control_flick
                contentX: "600"
            }
            PropertyChanges {
                target: background_flick
                contentX: "300"
            }
        }
    ]
    transitions: [
        Transition {
            from: ""; to: "connecting"; reversible: true
            PropertyAnimation {
                target: control_flick
                property: "contentX"
                duration: 400
                easing.type: Easing.InSine
            }
            PropertyAnimation {
                target: background_flick
                property: "contentX"
                duration: 400
                easing.type: Easing.InSine
            }
        }
    ]

}
