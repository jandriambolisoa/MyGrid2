import { Constants, GlobalStyles } from "@/theme";
import { TouchableOpacity, StyleProp, ViewStyle, View } from "react-native";
import { ShadowSetup, MainText, SpotLight } from '@/components/widgets';
import { useRouter } from "expo-router";
import { scopedI18n } from "@/translations/i18n";
import { rankNumber } from "@/utils";

export function RankingsWidget ({
  title,
  subtitle,
  rank=0,
  score=0,
  color1,
  color2,
  mode='diagonal',
  path,
  style,
}: {
  title?: string;
  subtitle?: string;
  rank?: number;
  score?: number;
  color1?: string | null;
  color2?: string | null;
  mode?: 'diagonal' | 'horizontal';
  path?: string;
  style?: StyleProp<ViewStyle>; 
}) {

  const router = useRouter()
  const t = scopedI18n('rankings')

  function handlePress () {
    if (path) {
      router.push(path as any)
    }
  }

  return (
    <TouchableOpacity
    
      style={[GlobalStyles.button, style]}
      onPress={handlePress}
    >
      {color1 && mode === 'diagonal' && <SpotLight color={color1} cx="35%" cy="35%" fx="5%" fy="5%" radius="60%"/>}
      {color2 && mode === 'diagonal' && <SpotLight color={color2} cx="70%" cy="70%" fx="95%" fy="95%" radius="60%"/>}
      {color1 && mode === 'horizontal' && <SpotLight color={color1} cx="35%" cy="35%" fx="5%" fy="5%" radius="60%"/>}
      {color2 && mode === 'horizontal' && <SpotLight color={color2} cx="70%" cy="70%" fx="95%" fy="95%" radius="60%"/>}
      <ShadowSetup/>
      <View style={{ padding: Constants.spacing.mainWidgetMargin }}>
        {title && <MainText fontSize='title' style={{ marginBottom: Constants.spacing.wideMargin}}>{title}</MainText>}
        {rank > 0 && <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 6, alignSelf: 'center' }}>
          <MainText fontSize="header" style={{ marginEnd: 6 }}>{self ? t('yourRank') : t('rank')}</MainText>
          <MainText fontSize="title" bold={true}>{rankNumber(rank)}</MainText>
        </View>}
        {score > 0 && <View style={{ flexDirection: 'row', alignItems: 'center', alignSelf: 'center', marginBottom: Constants.spacing.wideMargin }}>
          <MainText fontSize="main" style={{ marginEnd: 6 }}>{self ? t('yourScore') : t('score')}</MainText>
          <MainText fontSize="header" bold={true}>{score} {t('pts')}</MainText>
        </View>}
        {score < 1 && <MainText style={{ marginBottom: Constants.spacing.wideMargin }} fontSize="header">{t('notRankedYet')}</MainText>}
        {subtitle && <MainText style={{ maxWidth: '80%' }}>{subtitle}</MainText>}
      </View>
    </TouchableOpacity>
  )
}