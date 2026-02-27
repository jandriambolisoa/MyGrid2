import { BlurView } from "expo-blur";
import { ViewProps } from "react-native";
import { Constants, GlobalStyles } from "@/theme";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export type FrameProps = ViewProps & {
  orientation?: 'top' | 'bottom';
}

export function Frame({
  orientation='top',
  ...otherProps
}: FrameProps) {

  const insets = useSafeAreaInsets()

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
      intensity={10}
      style={[GlobalStyles.frame, orientedStyle, otherProps.style]}
      {...otherProps}
    >

    </BlurView>
  )
}