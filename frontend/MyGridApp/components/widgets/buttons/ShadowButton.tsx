import { GlobalStyles, Constants } from "@/theme";
import { StyleSheet, TouchableOpacity, View, type TouchableOpacityProps } from "react-native";
import { ShadowSetup } from "@/components/widgets";

/**
 * Simple button with glass effect
 * 
 */

export function ShadowButton({ innerStyle, absoluteChild, style, ...otherProps }: TouchableOpacityProps & { innerStyle?: any; absoluteChild?: any;}) {
  return (
    <TouchableOpacity style={[GlobalStyles.button, style]} {...otherProps}>
      <View style={[StyleSheet.absoluteFill, { borderRadius: 3, overflow: 'hidden' }]}>
        <ShadowSetup />
      </View>
      <View style={[{ padding: Constants.spacing.buttonPadding }, innerStyle]}>
        {otherProps.children}
      </View>
      {absoluteChild}
    </TouchableOpacity>
  )
}