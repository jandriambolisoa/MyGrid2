import { StyleSheet } from "react-native";
import { Colors } from "@/theme"

export const GlobalStyles = StyleSheet.create({
  button: {
    borderColor: Colors.light.borders,
    borderWidth: 1,
    borderRadius: 4,
    overflow: 'hidden'
  },
  container: {
    flex: 1,
    backgroundColor: Colors.light.background,
    justifyContent: 'center',
    alignItems: 'center'
  }
});