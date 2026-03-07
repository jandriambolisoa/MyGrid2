import { View, ActivityIndicator, StyleSheet } from "react-native"
import { Colors } from "@/theme"

export function MainLoading ({
  color='light',
  loading=false
} : {
  color?: 'light' | 'orange';
  loading?: boolean;
}) {

  if (!loading) return null;

  const loadingColor = color === 'light' ? Colors.light.lightText : Colors.light.orangeLogo

  return (
    <View style={[StyleSheet.absoluteFill, { justifyContent: 'center', alignItems: 'center', backgroundColor: Colors.light.background }]}>
      <ActivityIndicator color={loadingColor}/>
    </View>
  )
}