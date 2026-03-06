import { Constants, GlobalStyles } from "@/theme";
import { TouchableOpacity, StyleProp, ViewStyle, View } from "react-native";
import { ShadowSetup, MainText, SpotLight } from '@/components/widgets';
import { useRouter } from "expo-router";

export function RankingsWidget ({
  title,
  subtitle,
  color1,
  color2,
  mode='diagonal',
  path,
  style,
}: {
  title?: string;
  subtitle?: string;
  color1?: string | null;
  color2?: string | null;
  mode?: 'diagonal' | 'horizontal';
  path?: string;
  style?: StyleProp<ViewStyle>; 
}) {

  const router = useRouter()

  function handlePress () {
    if (path) {
      router.push(path as any)
    }
  }

  return (
    <TouchableOpacity
      style={[GlobalStyles.button, { flex: 1 }, style]}
      onPress={handlePress}
    >
      {color1 && mode === 'diagonal' && <SpotLight color={color1} cx="35%" cy="35%" fx="5%" fy="5%" radius="60%"/>}
      {color2 && mode === 'diagonal' && <SpotLight color={color2} cx="70%" cy="70%" fx="95%" fy="95%" radius="60%"/>}
      {color1 && mode === 'horizontal' && <SpotLight color={color1} cx="35%" cy="35%" fx="5%" fy="5%" radius="60%"/>}
      {color2 && mode === 'horizontal' && <SpotLight color={color2} cx="70%" cy="70%" fx="95%" fy="95%" radius="60%"/>}
      <ShadowSetup/>
      <View style={{ padding: Constants.spacing.mainWidgetMargin }}>
        {title && <MainText fontSize='header' style={{ marginBottom: Constants.spacing.mainWidgetMargin}}>{title}</MainText>}
        {subtitle && <MainText>{subtitle}</MainText>}
      </View>
    </TouchableOpacity>
  )
}