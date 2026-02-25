import { View, StyleSheet } from "react-native";
import { SpotLight } from "@/components/widgets";
import { Colors } from "@/theme";

export function MyGridBackground () {
  return (
    <View style={[StyleSheet.absoluteFill]}>
      <SpotLight color={Colors.light.orangeLogo} cx="90%" cy="20%" fx="90%" fy="20%" radius="60%"/>
      <SpotLight color={Colors.light.cyanLogo} cx="10%" cy="80%" fx="10%" fy="80%" radius="60%"/>
    </View>
  )
}