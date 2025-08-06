import { StyleSheet, View } from "react-native";
import { BlurView } from "expo-blur";
import Svg, { Defs, Stop, RadialGradient, Rect } from "react-native-svg";

export default function MainScreen () {
  return (
    <View style={styles.container}>
        <View style={styles.widgetWrapper}>
          {/*
          <View style={{ borderRadius: 200, backgroundColor: 'yellow', position: 'absolute', height: 200, width: 200, top: '40%', right: '40%'}}/>
          <View style={{ borderRadius: 200, backgroundColor: 'black', position: 'absolute', height: 200, width: 200, top: '10%', right: '0%'}}/>
          <View style={{ borderRadius: 200, backgroundColor: 'red', position: 'absolute', height: 200, width: 200, top: '60%', right: '0%'}}/>
          */}
          <Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
            <Defs>
            <RadialGradient
              id="grad1"
              cx="40%"
              cy="50%"
              r="100%"
              fx="50%"
              fy="10%"
            >
              <Stop offset="0%" stopColor="red" stopOpacity="0.8" />
              <Stop offset="100%" stopColor="#dddddd" stopOpacity="0" />
            </RadialGradient>
          </Defs>
          <Rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="url(#grad1)"
          />
          </Svg>
          <Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
            <Defs>
            <RadialGradient
              id="grad2"
              cx="50%"
              cy="50%"
              r="75%"
              fx="100%"
              fy="100%"
            >
              <Stop offset="0%" stopColor="yellow" stopOpacity="0.8" />
              <Stop offset="100%" stopColor="#dddddd" stopOpacity="0" />
            </RadialGradient>
          </Defs>
          <Rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="url(#grad2)"
          />
          </Svg>
        </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#dddddd"
  },
  widget: {
    borderColor: "white",
    borderWidth: 0.5,
    borderRadius: 4,
    height: "100%",
    width: "100%"
  },
  widgetWrapper: {
    shadowColor: '#000000',
    shadowOffset: { width: 1, height: 1 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    marginHorizontal: 20,
    marginVertical: 60,
    flex: 1,
    overflow: 'hidden',
    backgroundColor: "#dddddd"
  }
})