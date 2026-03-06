import { useRouter } from "expo-router"
import { TouchableOpacity, TouchableOpacityProps } from "react-native"
import { Colors } from "@/theme"
import { Feather } from "@expo/vector-icons"

export function BackButton ({
  style,
  ...otherProps
} : TouchableOpacityProps) {

  const router = useRouter()

  return (
    <TouchableOpacity
      style={[{ position: 'absolute', width: 60, left: 0, bottom: 0, top: 0, alignItems: 'center', justifyContent: 'center' }, style]}
      onPress={router.back}
      {...otherProps}
    >
      <Feather name="arrow-left" size={34} color={Colors.light.lightText}/>
    </TouchableOpacity>
  )
}