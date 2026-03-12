import { StyleSheet } from "react-native";
import { Colors } from "./Colors";
import { Constants } from "./Constants";

export const GlobalStyles = StyleSheet.create({

  // Lists
  driverWidget: {
    height: Constants.spacing.driverWidgetHeight,
    flexDirection: 'row',
    justifyContent: 'space-between'
  },

  // Buttons
  loginButton: {
    padding: Constants.spacing.buttonPadding,
    fontSize: 16,
    width: '70%',
    alignSelf: 'center',
    marginBottom: Constants.spacing.buttonMargin,
    color: Colors.light.lightText
  },
  button: {
    borderColor: Colors.light.borders,
    borderWidth: 1,
    borderRadius: 4,
    overflow: 'hidden',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 44
  },
  backButton: {
    position: 'absolute',
    width: 60,
    left: 0,
    bottom: 0,
    top: 0,
    alignItems: 'center',
    justifyContent: 'center'
  },

  // Layout
  container: {
    flex: 1,
    backgroundColor: Colors.light.background,
    justifyContent: 'center',
    alignItems: 'center'
  },
  frame: {
    position: 'absolute',
    width: '100%',
    borderWidth: 0,
    borderColor: Colors.light.borders
  },
  header: {
    padding: Constants.spacing.buttonPadding,
    alignItems: 'center'
  },

  // TabBar
  tabBar: {
    bottom: 0,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingTop: 10,
    borderTopWidth: 1,
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
    borderRadius: 1000,
    borderColor: Colors.light.borders
  },

  eye: {
    position: 'absolute',
    justifyContent: 'center',
    alignItems: 'center',
    end: '15%',
    width: 40,
    bottom: Constants.spacing.buttonMargin,
    top: 0
  },
  authLink: {
    padding: 10,
    marginTop: Constants.spacing.buttonMargin,
    position: 'absolute',
    bottom: Constants.spacing.wideMargin,
    alignSelf: 'center'
  },
  warning: {
    marginTop: Constants.spacing.wideMargin,
    color: Colors.light.warning,
    textAlign: 'center'
  },

  mainWidgetButton: {
    alignSelf: "stretch",
    flexDirection: "row",
    justifyContent: "space-between",

  },

  toast: {
    alignSelf: 'stretch',
    padding: Constants.spacing.buttonPadding,
    marginHorizontal: Constants.spacing.buttonMargin - 6
  }
});