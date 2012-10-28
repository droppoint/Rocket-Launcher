// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import "signals.js" as Signals

Rectangle {
    id: root
    width: 300
    height: 560
    color: "#e6e6e6"
    focus:true
    //
	
	//Сигнал испускается при инициации соединения.
	//В себе содержит логин и пароль из соответствующих
	//полей
	signal cmd_connect(string login, string password);
	
	//Сигнал испускается при прекращении соединения
	signal cmd_disconnect();
	
	
	function include(arr, obj) {
		return (arr.indexOf(obj) != -1);
	}
	
	// эта функция принимает сигнал от 
	// модуля коннектор и в зависимости
	// от сигнала реализует поведение 
	// интерфейса
    function signal(status) { 
    	console.log("signal")
        if (status=="200"){
        	console.log('Connected signal recieved')
        	console.log(Signals.signal_hash[status])
        	root.state = "connected"
        }
        else if ( include(Signals.error_signals, status) ){
        	console.log("Error signal recieved")
        	console.log(Signals.signal_hash[status])
        	root.state = ""
        }
        else if ( include(Signals.connecting_signals, status) ){
        	console.log("Connecting signal recieved")
        	root.state = "connecting"
        	con_status.text = Signals.signal_hash[status]
        }
    }
	Keys.onPressed: {
        console.log('button pressed')
        console.log(event.key)
        if((event.key === Qt.Key_Enter) || (event.key === Qt.Key_Return)){
            if(root.state === ""){
                console.log('connect')
        	    cmd_connect(login_edit.text, password_edit.text)
            }
            else {
                console.log('disconnect')
                cmd_disconnect()
            }
        } else if (event.key === Qt.Key_Tab){
            login_edit.focus = true
        }
        event.accepted = true;
    }
    
    
    MouseArea {
        id: mousearea1
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
           // Qt.quit();
        }

        Flickable {
            id: control_flick
            height: 270
            contentWidth: 900
            contentHeight: 270
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            interactive: false

            Small_button {
                id: pref_button
                width: 28
                anchors.left: parent.left
                anchors.leftMargin: 20
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 15
            }
                
            Login_input {
                id: login_edit
                anchors.left: parent.left
                anchors.leftMargin: 40
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 150
                KeyNavigation.tab: password_edit
                KeyNavigation.down: password_edit
            }

            Login_input {
                id: password_edit
                anchors.left: parent.left
                anchors.leftMargin: 40
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 100
                password: true
                image_path: "images/password_input.svg"
                default_string: "Password"
                KeyNavigation.tab: login_edit
                KeyNavigation.up: login_edit
                //password: true
            }

            Button {
                id: connect_button
                default_string: "Подключение"
                anchors.horizontalCenterOffset: -300
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 28
                onBtnClicked: {
                	//root.state = "connecting"
                    cmd_connect(login_edit.text, password_edit.text)
                }
            }

            Text {
                id: rocket_one
                color: "#424242"
                text: qsTr("Rocket One")
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 14
                font.weight: Font.Light
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
                font.pixelSize: 40
            }

            Text {
                id: connecting
                color: "#424242"
                text: qsTr("Подключение")
                anchors.left: parent.left
                anchors.leftMargin: 310
                anchors.top: parent.top
                anchors.topMargin: 14
                font.weight: Font.Light
                font.pixelSize: 40
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
            }

            Text {
                id: online
                color: "#424242"
                text: qsTr("В сети")
                anchors.left: parent.left
                anchors.leftMargin: 610
                anchors.top: parent.top
                anchors.topMargin: 14
                font.pixelSize: 40
                font.weight: Font.Light
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
            }

            Text {
                id: con_status
                color: "#424242"
                text: qsTr("Соединение с сервером")
                anchors.left: parent.left
                anchors.leftMargin: 310
                anchors.top: parent.top
                anchors.topMargin: 80
                font.pixelSize: 20
                font.weight: Font.Light
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
            }

            Progressbar {
                id: progress_wheel
                anchors.left: parent.left
                anchors.leftMargin: 420
                anchors.top: parent.top
                anchors.topMargin: 140
                opacity: 0
            }

            Button {
                id: cancel_button
                x: 380
                anchors.horizontalCenter: parent.horizontalCenter
                top_color: "#EE5F5B"
                bottom_color: "#BD362F"
                default_string: "Отмена"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 28
                onBtnClicked: { cmd_disconnect()
                                root.state = ""}

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
                onBtnClicked: { cmd_disconnect()
                                root.state = ""}
            }

            Text {
                id: con_status1
                color: "#424242"
                text: qsTr("Запомнить")
                anchors.top: parent.top
                anchors.topMargin: 180
                anchors.left: parent.left
                anchors.leftMargin: 65
                font.pixelSize: 14
                font.weight: Font.Light
                font.italic: false
                font.bold: false
                font.family: "Ubuntu"
            }

            // Sw {
                // id: sw1
                // x: 40
                // y: 184
            // }

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
            color: "#424242"
            text: qsTr("Powered by Alfa & Pacha @ 2009")
            anchors.right: parent.right
            anchors.rightMargin: 20
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            font.family: "DejaVu Sans"
            font.pixelSize: 10
        }
    }
    
    states: [
        State {
            name: "connecting"
            PropertyChanges{ target: control_flick; contentX: "300" }
            PropertyChanges{ target: background_flick; contentX: "150" }
            PropertyChanges{ target: progress_wheel; opacity: 1 }
        },
        State {
            name: "connected"
            PropertyChanges{ target: control_flick; contentX: "600" }
            PropertyChanges{ target: background_flick; contentX: "300" }
        }
        
    ]

    transitions: Transition {
        reversible: true
        PropertyAnimation {
			id: slider
            targets: [control_flick, background_flick]
            property: "contentX"
            duration: 400
            easing.type: Easing.InSine
        }
    }

}
