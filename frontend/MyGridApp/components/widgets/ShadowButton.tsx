import { GlobalStyles, Spacing } from "@/theme";
import { TouchableOpacity, View, type TouchableOpacityProps } from "react-native";
import { ShadowSetup } from "@/components/widgets";

/**
 * Simple button with glass effect
 * 
 */

export function ShadowButton({ style, ...otherProps }: TouchableOpacityProps) {
  return (
    <TouchableOpacity style={[GlobalStyles.button, style]} {...otherProps}>
        <View style={{padding: Spacing.buttonPadding, zIndex: 1}}>
          {otherProps.children}
        </View>
        <ShadowSetup />
    </TouchableOpacity>
  )
}