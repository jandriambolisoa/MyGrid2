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
  },
  tabBar: {
    position: 'absolute',
    bottom: 0,
    flexDirection: 'row',
    width: '100%',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingTop: 10,
    borderWidth: 0,
    borderTopWidth: 1,
    borderColor: '#fff'
  }
});