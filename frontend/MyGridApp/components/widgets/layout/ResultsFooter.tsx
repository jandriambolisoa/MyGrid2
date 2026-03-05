import { FrameProps, Frame, MainText, SpotLight } from "@/components/widgets"
import { GlobalStyles, Constants } from "@/theme"
import { View, StyleSheet } from "react-native"
import { scopedI18n } from "@/translations/i18n"
import { performance } from "@/utils"

export type ResultsFooterProps = FrameProps & {
  score?: number,
  potentialScore?: number,
  spotColor?: string | null
}

export function ResultsFooter ({
  score=0,
  potentialScore=0,
  spotColor=null,
  ...otherProps
}: ResultsFooterProps) {

  const t = scopedI18n('widgets.resultsFooter')

  return (
    <Frame orientation='bottom' {...otherProps}>
      {spotColor && <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={spotColor} cx="60%" cy="60%" fx="90%" fy="90%" radius="70%" opacityStart="0.5"/>
      </View>}
      <View style={GlobalStyles.header}>
        <MainText style={{ fontSize: Constants.fontSizes.header, margin: 2 }} bold={true}>{t('totalScore')}+ {score} {t('pts')}</MainText>
        <MainText>{t('performance')}{performance(score, potentialScore)} %</MainText>
      </View>
    </Frame>
  )
}