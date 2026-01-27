import { GlobalStyles, Constants } from "@/theme";
import { TouchableOpacity, type TouchableOpacityProps } from "react-native";

/**
 * Simple button without glass effect
 * 
 */

export function LiteButton({ style, ...otherProps }: TouchableOpacityProps) {
  return (
    <TouchableOpacity style={[GlobalStyles.button, style, { padding: Constants.spacing.buttonPadding}]} {...otherProps}>
      {otherProps.children}
    </TouchableOpacity>
  )
}