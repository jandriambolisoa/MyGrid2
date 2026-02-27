import { FrameProps, Frame, MainText } from "@/components/widgets"
import { GlobalStyles, Constants } from "@/theme"
import { View } from "react-native"
import { scopedI18n } from "@/translations/i18n"

export type ResultsFooterProps = FrameProps & {
  score?: number,
  potentialScore?: number,
}

export function ResultsFooter ({
  score=0,
  potentialScore=0,
  ...otherProps
}: ResultsFooterProps) {

  const t = scopedI18n('widgets.resultsFooter')

  return (
    <Frame orientation='bottom' {...otherProps}>
      <View style={GlobalStyles.header}>
        <MainText style={{ fontSize: Constants.fontSizes.header, margin: 2 }} bold={true}>{t('totalScore')}+ {score} {t('pts')}</MainText>
        <MainText>{t('potentialScore')}+ {potentialScore} {t('pts')}</MainText>
      </View>
    </Frame>
  )
}