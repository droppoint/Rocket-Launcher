// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1


Item {
     id: progressbar
     width: 60; height: 60
     Image{
              id: rect
              width: 60; height: 60
              source: "images/progress.svg"
              smooth: true
              RotationAnimation on rotation{
                  running: true
                  from: 0
                  to: 360
                  loops: Animation.Infinite
                  duration: 1500
                  easing.type: Easing.InOutQuad

              }
          }
 }
