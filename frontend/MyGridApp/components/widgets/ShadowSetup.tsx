import { Constants } from "@/theme";
import { View, StyleSheet } from "react-native";
import { Shadow } from "@/components/widgets";

/**
 * Top, left, right, bottom shadow setup for buttons and other widgets
 * 
 */

export function ShadowSetup() {
  return (
    <View style={[StyleSheet.absoluteFill]}>
      <Shadow orientation="top" thickness={Constants.shadow.topThickness}/>
      <Shadow orientation="left" thickness={Constants.shadow.leftThickness}/>
      <Shadow orientation="right" light={true} thickness={Constants.shadow.rightThickness} opacityStart={Constants.shadow.lightOpacity}/>
      <Shadow orientation="bottom" light={true} thickness={Constants.shadow.bottomThickness} opacityStart={Constants.shadow.lightOpacity}/>
    </View>
  )
}