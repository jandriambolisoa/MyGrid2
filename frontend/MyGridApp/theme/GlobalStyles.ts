import { StyleSheet } from "react-native";
import { Colors } from "./Colors";
import { Constants } from "./Constants";

export const GlobalStyles = StyleSheet.create({
  loginButton: {
    padding: Constants.spacing.buttonPadding,
    fontSize: 16
  },
  button: {
    borderColor: Colors.light.borders,
    borderWidth: 1,
    borderRadius: 4,
    overflow: 'hidden',
    alignItems: 'center',
    justifyContent: 'center'
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
  },
  tabBarSlider: {
    position: 'absolute',
    height: 1,
    backgroundColor: Colors.light.borders,
    width: Constants.spacing.sliderWidth,
    transform: [{ translateX: -Constants.spacing.sliderWidth / 2 }]
  },
  mainWidget: {
    alignSelf: 'stretch',
    marginHorizontal: Constants.spacing.mainWidgetMargin,
    marginBottom: Constants.spacing.mainWidgetMargin,
    alignItems: 'center'
  },
  rowWidget: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    alignSelf: 'stretch'
  },
  profilePicture: {
    width: 200,
    height: 200,
    borderRadius: 500,
    borderWidth: 1,
    borderColor: Colors.light.borders,
    marginVertical: 36
  },
  eye: {
      position: 'absolute',
      justifyContent: 'center',
      alignItems: 'center',
      end: 0,
      width: 40,
      height: '100%'
  }
});