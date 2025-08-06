import { useState, useEffect } from "react";
import { StyleSheet, View, Text } from "react-native";
//import { BlurView } from "expo-blur";
import Svg, { Defs, Stop, RadialGradient, Rect } from "react-native-svg";
import { DeviceMotion } from "expo-sensors";

export default function MainScreen () {

  const [orientation, setOrientation] = useState({ alpha: 0, beta: 0, gamma: 0 });

  useEffect(() => {
    const subscription = DeviceMotion.addListener((motion) => {
      if (motion.rotation) {
        setOrientation({
          alpha: motion.rotation.alpha, // z-axis (yaw)
          beta: motion.rotation.beta,   // x-axis (pitch)
          gamma: motion.rotation.gamma, // y-axis (roll)
        });
      }
    });

    return () => subscription.remove();
  }, []);

  function getScreenNormalVector(alpha: number, beta: number, gamma: number) {
  // Rotation matrices
  const cA = Math.cos(alpha);
  const sA = Math.sin(alpha);
  const cB = Math.cos(beta);
  const sB = Math.sin(beta);
  const cG = Math.cos(gamma);
  const sG = Math.sin(gamma);

  // Apply Z (alpha), X (beta), Y (gamma) rotation in order
  // The forward vector of the screen in device coordinates is [0, 0, -1]
  // We rotate that vector using the combined rotation matrix

  const x = -cG * sA - sG * sB * cA;
  const y = -sG * sA + cG * sB * cA;
  const z = cB * cA;

  return { x, y, z };
}

function getInterpolatedColor(value: number, invert: boolean = false) {
  // Clamp between -1.5 and 1.5
  const clamped = Math.max(-1.5, Math.min(1.5, value));

  // Map -1.5 → 0 (black), +1.5 → 1 (white)
  const brightness = invert? 1 - (clamped + 1.5) / 3 : (clamped + 1.5) / 3;  // range: 0 to 1

  const colorValue = Math.round(brightness * 255);
  const hex = colorValue.toString(16).padStart(2, '0');

  return `#${hex}${hex}${hex}`; // grayscale color
}

const screenVector = getScreenNormalVector(orientation.alpha, orientation.beta, orientation.gamma);

  return (
    <View style={styles.container}>
        <View style={styles.widgetWrapper}>
          <View style={[StyleSheet.absoluteFill, styles.widget]}>
            <Text>{orientation.alpha.toFixed(2)}</Text>
            <Text>{orientation.beta.toFixed(2)}</Text>
            <Text>{orientation.gamma.toFixed(2)}</Text>
            <View style={{borderWidth: 1, height: 100, width: 100, margin: 100, borderRadius: 4,
              borderTopColor: getInterpolatedColor(orientation.beta),
              borderBottomColor: getInterpolatedColor(orientation.beta, true),
              borderRightColor: getInterpolatedColor(orientation.gamma, true),
              borderLeftColor: getInterpolatedColor(orientation.gamma)}}/>
          </View>
          {/*
          <View style={{ borderRadius: 200, backgroundColor: 'yellow', position: 'absolute', height: 200, width: 200, top: '40%', right: '40%'}}/>
          <View style={{ borderRadius: 200, backgroundColor: 'black', position: 'absolute', height: 200, width: 200, top: '10%', right: '0%'}}/>
          <View style={{ borderRadius: 200, backgroundColor: 'red', position: 'absolute', height: 200, width: 200, top: '60%', right: '0%'}}/>
          */}
          {/*<Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
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
            rx="4"
            ry="4"
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
            rx="40"
            ry="40"
          />
          </Svg>*/}
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
    marginHorizontal: 20,
    marginVertical: 60,
    flex: 1,
    overflow: 'hidden',
    backgroundColor: "#dddddd"
  }
})