import { BlurView } from "expo-blur";
import { ViewProps, Platform } from "react-native";
import { Constants, GlobalStyles, Colors } from "@/theme";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export type FrameProps = ViewProps & {
  orientation?: 'top' | 'bottom';
}

export function Frame({
  orientation='top',
  ...otherProps
}: FrameProps) {

  const insets = useSafeAreaInsets()
  const backgroundColor = Platform.OS === 'ios' ? 'transparent' : Colors.light.androidBackground

  const orientedStyle = orientation === 'top'
    ? {
      borderBottomWidth: Constants.spacing.borderWidth,
      paddingTop: insets.top,
      top: 0
    }
    : {
      borderTopWidth: Constants.spacing.borderWidth,
      paddingBottom: insets.bottom,
      bottom: 0
    }

  return (
    <BlurView
      tint="light"
      intensity={20}
      style={[GlobalStyles.frame, orientedStyle, { backgroundColor: backgroundColor }, otherProps.style]}
      {...otherProps}
    />
  )
}