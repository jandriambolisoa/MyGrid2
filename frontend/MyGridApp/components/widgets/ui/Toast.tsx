import { Colors, GlobalStyles } from "@/theme";
import { MainText } from "@/components/widgets";
import { BlurView } from "expo-blur";
import { StyleSheet, TouchableOpacity, Platform } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export function Toast ({
  title,
  subtitle,
  type='info',
} : {
  title?: string;
  subtitle?: string;
  type?: 'info' | 'error' | 'success'
}) {

  const insets = useSafeAreaInsets();
  const android = Platform.OS === 'android';
  const borderColor = type === 'error' ? Colors.light.toastErrorBorders : type === 'success' ? Colors.light.toastSuccessBorders : Colors.light.borders;
  const backgroundColor = type === 'error' ? Colors.light.toastError : type === 'success' ? Colors.light.toastSuccess : Colors.light.borders;

  return (
    <TouchableOpacity style={[GlobalStyles.toast, GlobalStyles.button, {
      marginTop: insets.top + 6,
      backgroundColor: backgroundColor,
      borderColor: borderColor
    }]} disabled={true}>
      {!android && <BlurView intensity={30} tint='light' style={StyleSheet.absoluteFill}/>}
        {title && <MainText fontSize='header' bold={true}>{title}</MainText>}
        {subtitle && <MainText>{subtitle}</MainText>}
    </TouchableOpacity>
  )
}