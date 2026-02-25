import { GlobalStyles, Constants } from "@/theme";
import { TouchableOpacity, View, type TouchableOpacityProps } from "react-native";
import { ShadowSetup } from "@/components/widgets";

/**
 * Simple button with glass effect
 * 
 */

export function ShadowButton({ style, ...otherProps }: TouchableOpacityProps) {
  return (
    <TouchableOpacity style={[GlobalStyles.button, style]} {...otherProps}>
      <ShadowSetup />
      <View style={{padding: Constants.spacing.buttonPadding, zIndex: 1}}>
        {otherProps.children}
      </View>
    </TouchableOpacity>
  )
}