import { StyleSheet, View } from "react-native";
import { Frame, MainText, SpotLight } from "@/components/widgets";
import { GlobalStyles } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { rankNumber } from "@/utils";

export function RankingsFooter ({
  datas=null,
  spotColor=null,
  ...otherProps
} : {
  datas?: any;
  spotColor?: string | null;
}) {

  if (!datas) {
    return null;
  }

  const t = scopedI18n('rankings')

  return (
    <Frame orientation='bottom' {...otherProps}>
      {spotColor && <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={spotColor} cx="60%" cy="60%" fx="90%" fy="90%" radius="80%" opacityStart="0.6"/>
      </View>}
      <View style={GlobalStyles.header}>
        <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 6 }}>
          <MainText fontSize="header" style={{ marginEnd: 6 }}>{t('yourRank')}</MainText>
          <MainText fontSize="title" bold={true}>{rankNumber(datas?.rank)}</MainText>
        </View>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <MainText fontSize="main" style={{ marginEnd: 6 }}>{t('yourScore')}</MainText>
          <MainText fontSize="header" bold={true}>{datas?.score} {t('pts')}</MainText>
        </View>
      </View>
    </Frame>
  )
}