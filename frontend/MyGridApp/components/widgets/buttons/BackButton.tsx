import { useRouter } from "expo-router"
import { TouchableOpacity, TouchableOpacityProps } from "react-native"
import { Colors, Constants } from "@/theme"
import { Feather } from "@expo/vector-icons"

export function BackButton ({
  style,
  ...otherProps
} : TouchableOpacityProps) {

  const router = useRouter()

  return (
    <TouchableOpacity
      style={[{ position: 'absolute', width: Constants.spacing.backButtonSize, height: Constants.spacing.backButtonSize, left: 0, top: 0, alignItems: 'center', justifyContent: 'center' }, style]}
      onPress={router.back}
      {...otherProps}
    >
      <Feather name="arrow-left" size={34} color={Colors.light.lightText}/>
    </TouchableOpacity>
  )
}